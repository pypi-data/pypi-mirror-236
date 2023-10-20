"""
    mq.py

    Class MQ to manage jobs.
    Jobs are used to coordinate cooperation between services through message queues, with client and server roles.
    MQ can be run as a server or used as client to request jobs.

    The server() method waits for incoming job request on the Queue qname forever.
    For every request for that Queue a callback is called.
    The call back ha 3 parameters: the mq object, the job id and the received payload.

    The publish method requests a new job, passing the qname, email and payload.

    Jobs lifecycle are stored on in the jobs db tables. All jobs have an id (jid) a owner (email).
    The lifecycle can be managed both by the MQ server and the callback.
    Lifecycle methods include: job_start, job_update_eta, job_done, job_error.
"""
import sys
import asyncio
import time
from datetime import datetime
from uuid import UUID
import json
from aio_pika import connect_robust, Message, DeliveryMode
from dl2050utils.core import oget, listify

JOB_CREATE = 0
JOB_START = 1
JOB_DONE = 2
JOB_NOTIFY = 3  # ??
JOB_DELIVER = 4  # ??
JOB_ERROR = 99

class MQ():
    def __init__(self, log, db, qnames, cfg):
        self.LOG,self.db,self.qnames = log,db,listify(qnames)
        user = oget(cfg, ['mq','user'], 'admin')
        passwd = oget(cfg, ['mq','passwd'], 'password')
        self.cfg,self.url = cfg,f'amqp://{user}:{passwd}@mq:5672/'

    # ##########################################################################################
    # startup
    # ##########################################################################################

    async def startup(self, loop=None):
        try:
            self.con = await connect_robust(self.url, loop=loop)
            self.ch = await self.con.channel()
            for qname in self.qnames:
                await self.ch.declare_queue(qname, durable=True, auto_delete=False)
        except Exception as e:
            self.LOG(4, 0, label='MQ', label2='connect', msg=str(e))
            return True
        self.LOG(2, 0, label='MQ', label2='STARTUP', msg='OK')
        return False

    def sync_startup(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.startup(loop=loop))
    
    # ##########################################################################################
    # Server methods
    # ##########################################################################################
    
    def server(self, qname, cb):
        """
            Run MQ as a server, waiting forever on queue qname.
            Calls the async method mq_server inside an async loop to start the server.
        """
        if qname not in self.qnames:
            self.LOG(4, 0, label='MQ', label2='EXCEPTION', msg=f'Invalid qname {qname}')
            raise f'MQ server: invalid qname {qname}'
        self.LOG(2, 0, label='MQ', label2='SERVER', msg='Started')
        loop = asyncio.get_event_loop()
        err = loop.run_until_complete(self.mq_server(qname, cb))
        if err:
            self.LOG(4, 0, label='MQ', label2='EXCEPTION', msg='Exit')
            sys.exit(1)
    
    async def mq_server(self, qname, cb):
        """
            Async server that awaits forever for messages.
            All messages are dispached to the process_msg method.
        """
        q = await self.ch.declare_queue(qname, durable=True, auto_delete=False)
        async with q.iterator() as it:
            async for msg in it:
                async with msg.process():
                    await self.process_msg(msg, cb)

    async def process_msg(self, msg, cb):
        """
            Processes an incoming message.
            The msg arguments are: MQ server, job id, payload.
        """
        t0 = time.time()
        payload = json.loads(msg.body.decode())
        email,jid = payload['email'],payload['jid']
        self.LOG(2, 0, label='MQ', label2=f'JOB SCHEDULED', msg={'email':email, 'jid':jid})
        try:
            err = cb(self, jid, payload)
        except Exception as exc:
                self.LOG(4, time.time()-t0, label='MQ', label2=f'JOB EXCEPTION', msg={'email':email, 'jid':jid, 'exception':str(exc)})
                await self.job_error(jid)
                return True
        if err:
            await self.job_error(jid)
            self.LOG(4, time.time()-t0, label='MQ', label2=f'JOB ERROR', msg={'email':email ,'jid':jid})
            return True
        await self.job_done(jid)
        # msg.ch.basic_ack(delivery_tag = msg.method.delivery_tag)
        self.LOG(2, time.time()-t0, label='MQ', label2=f'JOB EXECUTED', msg={'email':email, 'jid':jid})
        return False

    # ##########################################################################################
    # Client method
    # ##########################################################################################

    async def publish(self, qname, email, payload):
        """
            Publishes a new message to the queue qname.
            Returns the qid or None if error
        """
        d = {'email':email, 'qname':qname, 'payload':payload, 'jstatus':JOB_CREATE, 'eta':0, 'ts_create':datetime.now()}
        jid = await self.db.insert('jobs', d, return_key='jid')
        if jid is None:
            return None
        try:
            payload['email'],payload['jid'] = email,str(jid)
            msg = Message(body=json.dumps(payload).encode(), delivery_mode=DeliveryMode.PERSISTENT)
            await self.ch.default_exchange.publish(msg, routing_key=qname)
        except Exception as e:
            self.LOG(4, 0, label='MQ', label2='publish', msg=str(e))
            return None
        return str(jid)
    
    # ##########################################################################################
    # Jobs management methods 
    # ##########################################################################################

    async def job_select(self, jid=None, qname=None, email=None, pending=False):
        if jid is None and email is None:
            return None
        if jid is not None:
            return await self.db.select_one('jobs', {'jid':jid})
        d = [{'col':'email', 'val':email}]
        if pending:
            d.append({'col':'jstatus', 'val':2, 'op':'<'})
        if qname is not None:
            d.append({'col':'qname', 'val':qname})
        return await self.db.select('jobs', filters=d)
        
    async def job_update(self, jid, status=None, eta=None, result=None):
        job = {'jid': jid}
        if status is not None:
            job['jstatus'] = status
            if status==JOB_START: job['ts_start'] = datetime.now()
            if status==JOB_DONE: job['ts_done'] = datetime.now()
        if eta is not None: job['eta']=eta
        if result is not None and type(result)==dict: job['result']=result
        self.LOG(1, 0, label='MQ', label2='job_update', msg=job)
        res = await self.db.update('jobs', 'jid', job)
        if res is None or res==0: return True
        return False

    # Lifecycle functions
    async def get_jobs(self, email, qname=None): return await self.job_select(email=email, qname=qname)
    async def get_pending_jobs(self, email, qname=None): return await self.job_select(email=email, pending=True, qname=qname)
    async def get_job(self, jid): return await self.job_select(jid=jid)
    async def job_start(self, jid, eta=None): return await self.job_update(jid, status=JOB_START, eta=eta)
    async def job_update_eta(self, jid, eta): return await self.job_update(jid, eta=eta)
    async def job_done(self, jid, result=None): return await self.job_update(jid, status=JOB_DONE, result=result)
    async def job_error(self, jid): return await self.job_update(jid, status=JOB_ERROR, eta=0)
    async def job_notify(self, jid): return await self.job_update(jid, status=JOB_NOTIFY)
    async def job_deliver(self, jid): return await self.job_update(jid, status=JOB_DELIVER)
    async def job_result(self, jid, result): return await self.job_update(jid, result=result)

    # Sync verions of the lifecycle functions
    def sync_get_jobs(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.get_jobs(*args, **kwargs))
    def sync_get_pending_jobs(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.get_pending_jobs(*args, **kwargs))
    def sync_get_job(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.get_job(*args, **kwargs))
    def sync_job_start(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_start(*args, **kwargs))
    def sync_job_update_eta(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_update_eta(*args, **kwargs))
    def sync_job_done(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_done(*args, **kwargs))
    def sync_job_error(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_error(*args, **kwargs))
    def sync_job_notify(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_notify(*args, **kwargs))
    def sync_job_deliver(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_deliver(*args, **kwargs))
    def sync_job_result(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.job_result(*args, **kwargs))
