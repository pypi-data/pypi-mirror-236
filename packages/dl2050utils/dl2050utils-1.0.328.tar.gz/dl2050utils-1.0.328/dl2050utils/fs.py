import asyncio
import os
import shutil
from pathlib import Path
import requests
import subprocess
from py7zr import unpack_7zarchive
import orjson
import pickle
import numpy as np
import pandas as pd
import aiofiles
import io
from dl2050utils.core import listify

Path.ls = lambda x: list(x.iterdir())

# ################################################################################
# pickle_save (pickle_dump), pickle_load
# np_save, np_load, np_load_async
# df_save, df_load
# json_load (json_parse), json_dump, read_json
# json_saves, json_loads
# ################################################################################

def pickle_save(p, d):
    p = Path(p)
    p = p.with_suffix('.pickle')
    try:
        with open(p, 'wb') as f:
            pickle.dump(d, f)
        return 0
    except Exception:
        return 1

# Deprecated
def pickle_dump(p, d): return pickle_save(p, d)
    
def pickle_load(p):
    p = Path(p)
    p = p.with_suffix('.pickle')
    if not p.is_file():
        return None
    try:
        with open(p, 'rb') as f:
            d = pickle.load(f)
        return d
    except Exception:
        return None
    
def np_save(p, d, allow_pickle=True):
    p = Path(p)
    p = p.with_suffix('.npy')
    try:
        np.save(p, d, allow_pickle=allow_pickle)
        return 0
    except Exception:
        return 1
    
def np_load(p, allow_pickle=True):
    p = Path(p)
    p = p.with_suffix('.npy')
    if not p.is_file():
        return None
    try:
        if allow_pickle:
            d = np.load(p, allow_pickle=allow_pickle)
            if d is None: return None
            return d.item()
        else:
            return np.load(p)
    except Exception:
        return None
    
async def np_load_async(p, allow_pickle=False):
    p = Path(p)
    p = p.with_suffix('.npy')
    if not p.is_file():
        return None
    try:
        async with aiofiles.open(p, mode='rb') as f:
            buffer = await f.read()
        f = io.BytesIO(buffer)
        if allow_pickle:
            d = np.load(f, allow_pickle=allow_pickle)
            if d is None: return None
            return d.item()
        else:
            return np.load(f, allow_pickle=allow_pickle)
    except Exception:
        return None
    
def df_save(p, df):
    p = Path(p)
    p = p.with_suffix('.feather')
    try:
        df.to_feather(p)
        return 0
    except Exception:
        return 1
    
def df_load(p):
    p = Path(p)
    p = p.with_suffix('.feather')
    if not p.is_file():
        return None
    try:
        df = pd.read_feather(p)
        return df
    except Exception:
        return None

def json_save(p, d):
    p = Path(p)
    p = p.with_suffix('.json')
    try:
        with open(p, 'wb') as f:
            f.write(orjson.dumps(d))
        return 0
    except Exception:
        return 1
    
def json_load(p):
    p = Path(p)
    p = p.with_suffix('.json')
    if not p.is_file():
        return None
    try:
        with open(p, 'rb') as f:
            return orjson.loads(f.read())
    except Exception:
        return None

def json_dumps(o):
    try:
        return orjson.dumps(o, option=orjson.OPT_SERIALIZE_NUMPY).decode()
    except:
        return None

def json_loads(s):
    if s is None or s=='': return None
    try:
        o = orjson.loads(s)
        if o=={}: return None
        return o
    except:
        return None

# To be reviwed (used in PW) and renamed to json_load
def read_json(p): return json_load(p)

# ################################################################################
# cp, rm
# ################################################################################

def cp(p1, p2):
    """ Copies recursively p1 to p2 with overwrite. If p1 is a directory, copies recursively. """
    p1,p2 = Path(p1),Path(p2)
    if not p1.exists():
        print(f'File {p1} not found')
        return 1
    try:
        if p1.is_file():
            shutil.copyfile(p1, p2)
            return 0
        if p2.is_dir():
            shutil.rmtree(p2)
        shutil.copytree(p1, p2)
    except Exception:
        return 1
    
def rm(p):
    " Removes file or directory p. If p is a directory, removes recursively. "
    try: 
        p = Path(p)
        if p.is_file():
            p.unlink()
            return 0
        if p.is_dir():
            return shutil.rmtree(p)
    except Exception:
        return 1

# ################################################################################
# sh_run, run_asyc
# ################################################################################

def sh_run(cmd):
    """ Executas a shell command and return a tuple with exit code and stdout. """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdout, stderr) = proc.communicate()
    stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")
    if proc.returncode!=0: raise RuntimeError(f'sh_run command \n{cmd}\n exit with error code {proc.returncode}:\n{stderr}')
    return (proc.returncode, stdout)

async def run_asyc(*args):
    try:
        process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()
    except:
        return -1, '', 'Command not found'
    
# ################################################################################
# get_all_files, get_dir_files, get_dir_dirs
# ################################################################################

def get_all_files(p, filetypes=None):
    p = Path(p)
    filetypes = [e.lower() for e in listify(filetypes)]
    filetypes = [f'.{e}' if e[0]!='.' else e for e in filetypes]
    files = [p1 for p1 in p.rglob('*')]
    if len(filetypes): files = [f for f in files if f.suffix.lower() in filetypes]
    return files

# Draft
def get_dir_files(path, types=None):
    return [f for f in path.glob('**/*') if f.is_file() and (types==None or f.suffix[1:] in types)]

# Draft
def get_dir_dirs(path):
    return [d for d in path.glob('**/*') if d.is_dir()]
    
# ###################################################################################
# zip_get_registered_formats, zip_register_formats, iszip, dozip, unzip, unzip_tree
# ###################################################################################

def zip_get_registered_formats():
    return sum([e[1] for e in shutil.get_unpack_formats()], [])
    
def zip_register_formats():
    zips = zip_get_registered_formats()
    if '.7z' not in zips:
        print('Registering .7z')
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    if '.hsz' not in zips:
        print('Registering .hsz')
        shutil.register_unpack_format('7zip', ['.hsz'], unpack_7zarchive)

def dozip(p, remove=False):
    p = Path(p)
    if not p.exists():
        print(f'dozip: file not found: {p}')
        return 1
    try: 
        shutil.make_archive(p, 'zip', p)
        if remove:
            if rm(p): return 1
        return 0
    except Exception:
        return 1
    
def iszip(p):
    zipext = zip_get_registered_formats()
    archext = ['.rar']
    return (Path(p)).suffix in zipext+archext
    
def unzip(p, remove=False):
    """ Unzip or untar a file. If it is not an archive does nothing. """
    p = Path(p)
    if not p.exists():
        print(f'unzip: file not found: {p}')
        return 1
    if p.is_dir():
        return 0
    if not iszip(p):
        return 0
    if p.suffix in ['.rar']:
        code,stdout = sh_run(f'unrar x {p} {p.parent}')
        if code!=0:
            print(f'unrar error: {stdout}')
            return 1
        if remove:
            if rm(p): return 1
        print(f'File {p} extracted from archive')
        return 0
    p_dir = p.with_suffix('')
    try: 
        shutil.unpack_archive(p, p_dir)
        if remove:
            if rm(p): return 1
        print(f'File {p} unzipped')
        return 0
    except Exception as exc:
        print(f'Exception: {exc}')
        return 1
    
def unzip_tree(p):
    """ Get all subfolders and files from and unzip/untar if needed. """
    for p1 in [p1 for p1 in get_all_files(p)]:
        if unzip(p1, remove=True):
            print(f'unzip_tree: error unzipping {p1}')
    
# ################################################################################
# download_url, download
# ################################################################################

def download_url(url, dest, overwrite=False, pbar=None, show_progress=True, chunk_size=1024*1024, timeout=4, retries=5):
    "Download `url` to `dest` unless it exists and not `overwrite`."
    # wget -c <url> && tar -zxvf <fname>
    if os.path.exists(dest) and not overwrite: return
    s = requests.Session()
    s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
    u = s.get(url, stream=True, timeout=timeout)
    try: file_size = int(u.headers["Content-Length"])
    except: show_progress = False

    with open(dest, 'wb') as f:
        nbytes = 0
        # if show_progress: pbar = progress_bar(range(file_size), auto_update=False, leave=False, parent=pbar)
        try:
            for chunk in u.iter_content(chunk_size=chunk_size):
                nbytes += len(chunk)
                if show_progress: pbar.update(nbytes)
                f.write(chunk)
        except requests.exceptions.ConnectionError as e:
            print(f'\n Download of {url} has failed after {retries} retries.\nError: {e}')
            return False
    return True

def download(url, fname=None, ext='.tgz'):
    "Download `url` to destination `fname`."
    if fname is None:
        fname = Path(f"{url.split('/')[-1]}{ext}")
    os.makedirs(fname.parent, exist_ok=True)
    if not fname.exists():
        print(f'Downloading {url}')
        if not download_url(f'{url}{ext}', fname):
            return None
    return fname
