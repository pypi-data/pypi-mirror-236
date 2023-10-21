import datetime
import random
import urllib
import json
import hashlib
import orjson
import jwt
import asyncpg
import uuid
import numpy as np
from starlette.responses import JSONResponse
from dl2050utils.core import oget
from dl2050utils.fs import read_json

# ####################################################################################################
# REST Responses and Exceptions
# ####################################################################################################

# class OrjsonSerializer(orjson.JSONSerializable):
#     def default(self, obj):
#         if isinstance(obj, asyncpg.pgproto.pgproto.UUID):
#             return str(obj)
#         raise TypeError
    
def orjson_serialize(obj):
    if isinstance(obj, asyncpg.pgproto.pgproto.UUID):
        return str(obj)
    raise TypeError

class OrjsonResponse(JSONResponse):
    def render(self, content):
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY, default=orjson_serialize)

def rest_ok(d=None):
    if d is None: d = {}
    if type(d)!=dict: d = {'result':d}
    if 'status' not in d: d['status'] = 'OK'
    return OrjsonResponse(d)

class HTTPException(Exception):
    def __init__(self, status_code, detail, error_type='APP'):
        self.status_code,self.detail,self.error_type = status_code,detail or '',error_type
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(status_code={self.status_code!r}, detail={self.detail!r})'

def log_and_raise(LOG, status_code=400, error_type='APP', label='', label2='', msg=''):
    if LOG is not None:
        LOG(4, 0, label=label, label2=label2, msg=msg)
    raise HTTPException(status_code, msg, error_type=error_type)

def log_and_raise_exception(LOG, label='', label2='', msg=''):
    return log_and_raise(LOG, error_type='EXCEPTION', label=label, label2=label2, msg=msg)

def log_and_raise_rest(LOG, label='', label2='', msg=''):
    return log_and_raise(LOG, error_type='REST', label=label, label2=label2, msg=msg)

def log_and_raise_service(LOG, label='', label2='', msg=''):
    return log_and_raise(LOG, error_type='SERVICE', label=label, label2=label2, msg=msg)

def log_and_raise_app(msg=''):
    return log_and_raise(None, error_type='APP', msg=msg)

def rest_exception(LOG, label, label2, msg):
    LOG(4, 0, label=label, label2=label2, msg=msg)
    raise HTTPException(400, detail=f'EXCEPTION: {msg}')

# ####################################################################################################
# Args
# ####################################################################################################

def enforce_required_args(LOG, payload, args, label='', label2='', as_list=False):
    """ Returns dict (or list is as_list is True) with args present in payload. Raises REST exception if any arg is missing """
    args2,miss = {},[]
    if payload is None:
        return args2
    for e in args:
        if e not in payload:
            miss.append(e)
        else:
            args2[e] = payload[e]
    if len(miss):
        msg = f'Missing required args: {", ".join(miss)}'
        log_and_raise_rest(LOG, label=label, label2=label2, msg=msg)
    if as_list:
        return [args2[e] for e in args2]
    return args2

def get_optional_args(payload, args, as_list=False):
    """ Returns dict (or list is as_list is True) with args present in payload """
    if as_list:
        return [payload[e] for e in args if e in payload] if payload is not None else []
    return {e:payload[e] for e in args if e in payload} if payload is not None else {}

# ####################################################################################################
# Meta
# ####################################################################################################

async def get_meta(path, db, model):
    meta = read_json(f'{path}/{model}/{model}.json')
    if meta is not None:
        return meta
    row = await db.select_one('models', {'model': model})
    if row is not None:
        return json.loads(row['meta'])
    return None

def sync_get_meta(path, db, model):
    meta = read_json(f'{path}/{model}/{model}.json')
    if meta is not None:
        return meta
    row = db.sync_select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None

# ####################################################################################################
# Etc
# ####################################################################################################

def mk_key(n=4):
    return ''.join([chr(48+i) if i<10 else chr(65-10+i) for i in [random.randint(0, 26+10-1) for _ in range(n)]])
    # return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def get_hash(o, secret):
    o1 = {**o}
    o1['secret']=secret
    return hashlib.sha224(json.dumps(o1).encode()).hexdigest()

def check_hash(o, h, secret):
    o1 = {**o}
    o1['secret']=secret
    return get_hash(o1,secret)==h

def get_upload_url(secret, bucket, fname, size, timeout=7*24*3600):
    payload = {
        'bucket': bucket,
        'fname': fname,
        'size': size,
        'ts': datetime.datetime.now().isoformat(),
        'timeout': timeout
    }
    payload['h'] = get_hash(payload, secret)
    url = f'/upload?{urllib.parse.urlencode(payload)}'
    return url

def get_download_url(secret, bucket, fname, timeout=7*24*3600):
    payload = {
        'bucket': bucket,
        'fname': fname,
        'ts': datetime.datetime.now().isoformat(),
        'timeout': timeout
    }
    payload['h'] = get_hash(payload, secret)
    url = f'/download?{urllib.parse.urlencode(payload)}'
    return url

def mk_jwt_token(uid, email, secret):
    JWT_EXP_DELTA_SECONDS = 30*24*3600
    payload = {
        'uid':uid,
        'email':email,
        'username':'',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, secret, 'HS256') # .decode('utf-8')

def s3_urls(s3, bucket_name, prefix):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1024)['Contents']
    return [f'http://{bucket_name}.s3-eu-west-1.amazonaws.com/{e["Key"]}' for e in response]

# ####################################################################################################
# Utils for testing REST service requests from from client:
#       rest_request, do_login: 
# ####################################################################################################

async def rest_request(session, url, headers, host, port, payload=None, method='POST', json=True):
    print(f'{method} url: http://{host}:{port}{url}')
    if method not in ['POST', 'GET']:
        print('Invalid HTTP method')
        return
    if method=='POST':
        payload = payload or {}
        r = await session.post(f'http://{host}:{port}{url}', headers=headers, json=payload)
    else:
        r = await session.get(f'http://{host}:{port}{url}', headers=headers)
    print(f'HTTP response status: {r.status}')
    if r.status==500:
        trace = await r.text()
        print('Server EXCEPTION trace: :', trace)
        return None
    else:
        if r.status==403:
            print(r)
            return None
        if r.status>=400:
            text = await r.text()
            print(text)
        if json:
            res = await r.json()
            return res
        else:
            return None
        
async def do_login(session, host, port, url, email, passwd):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    payload = {'email': email, 'passwd': passwd}
    res = await rest_request(session, url, headers, host, port, payload=payload, method='POST', json=True)
    jwt_token = oget(res,['jwt_token'])
    if jwt_token is None:
        print('ERROR: ', res)
        return None
    return {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':f"Bearer {jwt_token}"}

# ####################################################################################################
# Etc - to review
# ####################################################################################################

# def mk_weeks(ds1='2018-01-01', ds2=None, weekday=6):
#     d1 = datetime.datetime.strptime(ds1, '%Y-%m-%d').date()
#     delta = 5 - d1.weekday()
#     if delta<0: delta+=7
#     d1 += datetime.timedelta(days=delta)
#     d2 = datetime.datetime.now().date() if ds2 is None else datetime.datetime.strptime(ds2, '%Y-%m-%d').date()
#     ds = [d.strftime("%Y-%m-%d") for d in rrule.rrule(rrule.WEEKLY, dtstart=d1, until=d2)]
#     return ds[::-1]

# def get_week2(weeks, week): return weeks[weeks.index(week)+1] if weeks.index(week)+1<len(weeks) else None

