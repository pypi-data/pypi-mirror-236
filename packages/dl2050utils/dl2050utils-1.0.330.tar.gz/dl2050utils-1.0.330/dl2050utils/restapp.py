"""
restapp.py
App Class

Defines the logic for the REST App, including startup, shudown, Auth routes, downstream services routes and Custom Application routes.

The Auth routes are defined in the Auth module.

The downstream services routes include:
    /api/contact:
    /api/get_meta:
    /api/download_private
    /api/download_workfile/{fname}
    /api/download_req'
    /api/upload_req
    /api/publish_job
    /api/get_jobs
    /api/get_pending_jobs
    /api/get_job

The Custom Application are defined in the routes dict with the following structure:
    routes = {
        <route_path_string>: <route_defenition>,
        ...
    }
    <route_defenition> is a dict with keys 'f','args' and 'kwargs', with the function name implementing the route along with
    corresponding args and kwargs as lists of strings.

    For example:
        routes = {
            '/api/health': {'f': health, 'args':[], 'kwargs':[]},
            ...
        }

Every custom function implementing the route must observe the following:
    1) All inputs parsed from the Request as function parametes that must be defined in the lists args and kwargs above;
    2) All returns should be a dict with the format {status:<status>, ...}:
        - <status> should be either 'OK' or 'ERROR'
        - If 'status':'OK' extra attributes may be present and will be sent to the client
        - If 'status':'ERROR', attribute 'error_msg' should be present, optionally along with 'error_code'
        - If status is not present, 'status':'OK' is automatically inserted;
        - If the return is not a dict, a dict is created with {'status':'OK', 'result':<return>}
        - If None is returned, a dict is created with only {'status':'OK'}
        Examples:
            return {'status':'ERROR', 'error_msg':'Error message', 'error_code':'Error code'} # Client gets what is returned
            return {'data':[arg1, kwarg1]} # Client gets {'status':'OK', 'data':[arg1, kwarg1]}
            return [1,2,3] # Client gets {'status':'OK', 'result':[1, 2, 3]}
            return None # Client gets {'status':'OK'}
            return {'status':'ERROR', 'error_msg':'Error message', 'error_code':'Error code'} # Client gets what is returned
    3) All normal returns are converted into HTTP responses with HTTP status 200 and the return data as JSON

    4) It is possible to raise an exception through log_and_raise_app(msg), that is converted in an error return
       of the form {'status':'ERROR', 'error_type':'APP', 'error_msg':<msg>} and then sent as an HTTP response
       with HTTP status 400 and the error data as JSON

    5) If the function has an uncatched exception (bug), the App catches it and converts in the following response:
       {'status':'ERROR', 'error_type':'EXCEPTION', 'error_msg': <exception_details>} and then sent as an HTTP response
       with HTTP status 400 and the error data as JSON


"""

import time
from datetime import datetime, timezone
from pathlib import Path
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.authentication import requires
from dl2050utils.core import oget
from dl2050utils.restutils import HTTPException, log_and_raise_exception, log_and_raise_rest, log_and_raise_service, rest_ok,\
                                  enforce_required_args, get_optional_args, get_meta, get_upload_url, get_download_url

class App():

    def __init__(self, cfg, LOG, NOTIFY, db, mq, auth, path, routes=[], appstartup=None, perm=None):
        self.service = cfg['service']
        self.path = path
        self.cfg,self.LOG,self.NOTIFY,self.db,self.mq,self.auth = cfg,LOG,NOTIFY,db,mq,auth
        self.routes,self.appstartup,self.perm = routes,appstartup,perm
        self.d = {'LOG':LOG, 'path':path, 'db':db, 'mq':mq}
        self.fs_secret = oget(self.cfg,['fs','secret'])
        if self.fs_secret is None:
            self.LOG(3, 0, label='APP', label2='REST',  msg='fs_secret not found')

    async def startup(self):
        model,meta = oget(self.cfg,['app','model']),None
        if model is not None: meta = await get_meta(self.path, self.db, model)
        self.d['meta'] = meta
        if self.appstartup is None: return False
        return await self.appstartup(self.d)

    def shutdown(self):
        self.LOG(2, 0, label='APP', label2='shutdown', msg='OK')
        return False   

    def get_routes(self):
        BASE_ROUTES = [
            Route('/api/contact', endpoint=self.contact, methods=['POST']),
            Route('/api/get_meta', endpoint=self.get_meta, methods=['GET']),
            Route('/api/download_private', endpoint=self.download_private, methods=['GET']),
            Route('/api/download_workfile/{fname}', endpoint=self.download_workfile, methods=['GET']),
            Route('/api/download_req', endpoint=self.download_req, methods=['POST']),
            Route('/api/upload_req', endpoint=self.upload_req, methods=['POST']),
            Route('/api/publish_job', endpoint=self.publish_job, methods=['POST']),
            Route('/api/get_jobs', endpoint=self.get_jobs, methods=['POST']),
            Route('/api/get_pending_jobs', endpoint=self.get_pending_jobs, methods=['POST']),
            Route('/api/get_job', endpoint=self.get_job, methods=['POST']),
        ]
        APP_ROUTES = [Route(e, endpoint=self.app_route, methods=['POST']) for e in self.routes]
        return BASE_ROUTES + APP_ROUTES

    async def db_increase(self, tbl, k, kv, c, prefix=''):
        row = await self.db.select_one(tbl, {k: kv})
        if row is None or len(row)==0:
            log_and_raise_service(self.LOG, label='AUTH', label2=prefix, msg='DB increase error: select')
        row[c] += row[c]+1
        res = await self.db.update(tbl, row)
        if res:
            log_and_raise_service(self.LOG, label='AUTH', label2=prefix, msg='DB increase error: update')

    async def contact(self, request):
        data = await request.json()
        d = enforce_required_args(self.LOG, data, ['email','name','msg'], label='AUTH', label2='check_user')
        d['ts']: datetime.now(timezone.utc)
        err = await self.db.insert('contacts', d)
        if err:
            log_and_raise_service(self.LOG, label='REST', label2='contact', msg='DB access error')
        html = '<h1>Name</h1><p>{d["email"]</p><h1>Email</h1><p>{d["email"]</p><h1>Message</h1><p>{d["msg"]</p>}'
        self.notify.send_mail_async(d['email'], subject='Contact from Website (cardiolife.global)', html=html)
        return rest_ok()

    @requires('authenticated')
    async def get_meta(self, request):
        """
            Return the meta information.
        """
        u = await self.auth.check_auth(request)
        return rest_ok(self.d['meta'])

    @requires('authenticated')
    async def download_private(self, request):
        """
            Download a private file fname belonging to a registered user.
            User files are stores under the f'/data/{service}/downloads/{email}/' subfolder.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        fname = request.path_params['fname']
        p = Path(f'/data/{self.service}/downloads/{email}/{fname}')
        if not p.is_file():
            log_and_raise_service(self.LOG, label='REST', label2='download_private', msg='File not found')
        media_type = None  # 'application/vnd.ms-excel'
        return FileResponse(str(p), media_type=media_type, filename=fname)

    @requires('authenticated')
    async def download_workfile(self, request):
        """
            Downloads a workfile file fname belonging to a registered user.
            Workfiles are usually results produced by workers (usually trought MQ).
            Workfiles are stored in the f'/data/{self.service}/workfiles/' folder.
            Assumes the file was created with a security prefix including the user email.
            This way and only the user can access the file.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        fname = request.path_params['fname']
        p = Path(f'/data/{self.service}/workfiles/{email}-{fname}')
        if not p.is_file():
            log_and_raise_service(self.LOG, label='REST', label2='download_workfile', msg=f'File not found: {p}')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=fname)

    @requires('authenticated')
    async def download_req(self, request):
        """
            Prepares a download request for the fs. The request must specify the bucket and fname.
            A link is prepared to be user for the file download. A 24h default timeout is set.
        """
        if not self.fs_secret:
            log_and_raise_service(self.LOG, label='REST', label2='download_req', msg='Upload secret not defined')
        u = await self.auth.check_auth(request)
        # self.db_increase('users', 'uid', u['uid'], 'downloads', 'download_req')
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['bucket','fname'], label='REST', label2='download_req')
        self.perm(self.d, u, request.url.path, args)
        res = {'url': get_download_url(self.fs_secret, args['bucket'], args['fname'], timeout=7*24*3600)}
        return rest_ok(res)

    @requires('authenticated')
    async def upload_req(self, request):
        """
            Prepares a download request for the fs. The request must specify the bucket, fname and size.
            A link is prepared to be user for the file download. A 24h default timeout is set.
        """
        if not self.fs_secret:
            log_and_raise_service(self.LOG, label='REST', label2='upload_req', msg='Upload secret not defined')
        u = await self.auth.check_auth(request)
        # self.db_increase('users', 'uid', u['uid'], 'uploads', 'upload_req')
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['bucket','fname','size'], label='REST', label2='upload_req')
        self.perm(self.d, u, request.url.path, args)
        res = {'url': get_upload_url(self.fs_secret, args['bucket'], args['fname'], args['size'], timeout=7*24*3600)}
        return rest_ok(res)

    @requires('authenticated')
    async def publish_job(self, request):
        """
            Publishes a new job, calling mq.publish after checking permissions.
            Jobs require the user email as an attribute.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['q','payload'], label='REST', label2='publish_job')
        q,payload = args['q'],args['payload']
        self.perm(self.d, u, request.url.path, args)
        jid = await self.mq.publish(q, email, payload)
        if jid is None :
            log_and_raise_service(self.LOG, label='REST', label2='publish_job', msg='MQ publish error')
        self.LOG(2, 0, label='APP', label2='publish_job', )
        return rest_ok({'jid': jid})

    @requires('authenticated')
    async def get_jobs(self, request):
        """
            Gets all jobs from a user.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        jobs = await self.mq.get_jobs(email)
        return rest_ok(jobs)

    @requires('authenticated')
    async def get_pending_jobs(self, request):
        """
            Gets all pending jobs from a user.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        jobs = await self.mq.get_pending_jobs(email)
        return rest_ok(jobs)

    @requires('authenticated')
    async def get_job(self, request):
        """
            Gets a job details, identified by jid.
        """
        u = await self.auth.check_auth(request)
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['jid'], label='REST', label2='get_job')
        job = await self.mq.get_job(args['jid'])
        return rest_ok(job)

    @requires('authenticated')
    async def app_route(self, request):
        """
            Implements all the custom app routes.
        """
        if request.url.path not in self.routes:
            log_and_raise_rest(self.LOG, label='REST', label2=f'app_route {request.url.path}', msg='url path not found')
        d = self.routes[request.url.path]
        cb,args,kwargs = d['f'],d['args'],d['kwargs']
        u = await self.auth.check_auth(request)
        data = await request.json()
        args2 = enforce_required_args(self.LOG, data, args, label='REST', label2='app_route')
        kwargs2 = get_optional_args(data, kwargs)
        self.perm(self.d, u, request.url.path, {**args2, **kwargs2})
        try:
            res = await cb(self.d, u, *[args2[e] for e in args2], **kwargs2)
        except HTTPException as exc:
            raise
        except Exception as exc:
            log_and_raise_exception(self.LOG, label='REST', label2='app_route', msg=str(exc))
        return rest_ok(res)
