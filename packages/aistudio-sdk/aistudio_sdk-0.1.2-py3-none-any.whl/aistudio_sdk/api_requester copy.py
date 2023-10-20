# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件实现了请求过程

Authors: xiangyiqing(xiangyiqing@baidu.com)
Date:    2023/07/24
"""
import os
import json
import requests
from urllib.parse import quote
from aistudio_sdk import err_code
from aistudio_sdk import config, log
from aistudio_sdk.util import err_resp
from aistudio_sdk.util import gen_ISO_format_datestr
from aistudio_sdk.util import gen_base64
from aistudio_sdk.util import gen_MD5
from aistudio_sdk.util import create_sha256_file_and_encode_base64
from aistudio_sdk.version import VERSION

CONNECTION_RETRY_TIMES = config.CONNECTION_RETRY_TIMES
CONNECTION_TIMEOUT = config.CONNECTION_TIMEOUT


def _request(method, url, headers, data):
    """
    Params
        :url: http url
        :headers: dictionary of HTTP Headers to send
        :json_data: json data to send in the body
        :data: dictionary, list of tuples, bytes, or file-like object to send in the body
    Returns
        response data in json format
    """
    for _ in range(CONNECTION_RETRY_TIMES):
        try:
            err_msg = ''
            response = requests.request(method, url, headers=headers, data=data, timeout=CONNECTION_TIMEOUT)
            return response.json()
        except requests.exceptions.JSONDecodeError:
            err_msg = "Response body does not contain valid json: {}".format(response)
        except Exception as e:
            err_msg = 'Error occurred when request for "{}": {}.'.format(url, str(e))

    log.debug(err_msg)
    return err_resp(err_code.ERR_FAILED, 
                    err_msg[:500])


#################### AIStudio API ####################
def _post_aistudio(model_url, **kwargs):
    """请求AIStudio API"""
    url = "{}{}".format(
        os.getenv("STUDIO_MODEL_API_URL_PREFIX", default=config.STUDIO_MODEL_API_URL_PREFIX_DEFAULT),
        model_url
    )
    authorization = kwargs.pop("authorization", "")
    body = {k: v for k, v in kwargs.items()}
    log.debug(body)
    
    payload = json.dumps(body)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization,
        'SDK-Version': str(VERSION),
    }
    resp = _request('POST', url, headers, payload)

    def extract_ernie_response(resp):
        """
        extract ernie bot response from aistudio response
        Param
            :resp: {'logId': '67635a456177a8665cc5e4060e4b7f76', 'errorCode': 0, 'errorMsg': 'success', 'result': <ernie_bot_response_info...>}
        Return
            <ernie_bot_response_info>
        """
        # no response
        if not resp:
            return err_resp(err_code.ERR_FAILED,
                            "Ernie response is empty.")
        
        # not aistudio-formatted
        if "logId" not in resp:
            return resp
        
        error_code = resp.get("errorCode", None)
        # success
        if error_code == err_code.ERR_OK:
            return resp.get("result", None)
        # error
        log.debug(resp)
        error_msg = resp.get("errorMsg", None)
        return err_resp(error_code, error_msg)

    return extract_ernie_response(resp)


def request_aistudio_completion(**kwargs):
    """
    请求AIStudio chat completion
    """
    url = config.COMPLETION_URL
    kwargs.update({'authorization': 'token {} {}'.format(kwargs.pop("user_id", ""), kwargs.pop("token", ""))})
    return _post_aistudio(url, **kwargs)


def request_aistudio_embedding(**kwargs):
    """
    请求AIStudio embed
    """
    url = config.EMBEDDING_URL
    kwargs.update({'authorization': 'token {} {}'.format(kwargs.pop("user_id", ""), kwargs.pop("token", ""))})
    return _post_aistudio(url, **kwargs)


#################### 文心千帆官方API ####################
def _post_wenxinworkshop(url, **kwargs):
    """
    请求文心千帆官方API
    Params
        url: http url后缀
    """
    url = "{}{}".format(config.WENXIN_URL_PREFIX, url)
    body = {k: v for k, v in kwargs.items()}
    payload = json.dumps(body)
    headers = {
        'Content-Type': 'application/json'
    }
    return _request('POST', url, headers, payload)


def request_wenxin_ernie_bot(**kwargs):
    """
    请求文心千帆 ERNIE-Bot 模型
    - doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/jlil56u11
    """
    url = config.WENXIN_ERNIE_BOT_URL
    return _post_wenxinworkshop(url, **kwargs)


def request_wenxin_embedding_v1(**kwargs):
    """
    请求文心千帆 Embedding-V1 模型
    - doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/alj562vvu
    """
    url = config.WENXIN_EMBEDDING_V1_URL
    return _post_wenxinworkshop(url, **kwargs)


#################### AIStudio 云端模型库 API ####################
def _request_aistudio_hub(method, url, headers, data):
    """
    request aistudio hub
    """
    for _ in range(CONNECTION_RETRY_TIMES):
        try:
            err_msg = ''
            response = requests.request(method, url, headers=headers, data=data, timeout=CONNECTION_TIMEOUT)
            #print(response.content)
            return response.json()
        except requests.exceptions.JSONDecodeError:
            err_msg = "Response body does not contain valid json: {}".format(response)
            biz_code = response.status_code

    log.debug(err_msg)
    return err_resp(err_code.ERR_FAILED, 
                    err_msg[:500],
                    biz_code)


def request_aistudio_hub(**kwargs):
    """
    请求AIStudio hub
    """
    headers = _header_fill()

    url = "{}{}".format(
        os.getenv("STUDIO_MODEL_API_URL_PREFIX", default=config.STUDIO_MODEL_API_URL_PREFIX_DEFAULT), 
        config.HUB_URL
    )

    body = {k: v for k, v in kwargs.items()}
    log.debug(body)

    payload = json.dumps(body)
    resp = _request_aistudio_hub('POST', url, headers, payload)

    return resp


#################### AIStudio Gitea API ####################
def _request_gitea(method, url, headers, data):
    """
    request gitea
    """
    for _ in range(CONNECTION_RETRY_TIMES):
        try:
            err_msg = ''

            #from http.client import HTTPConnection
            #HTTPConnection.debuglevel=1
            session = requests.Session()
            response = session.request(method, url, headers=headers, data=data, timeout=CONNECTION_TIMEOUT)
            session.close()

            #response = requests.request(method, url, headers=headers, data=data, #timeout=CONNECTION_TIMEOUT)
            
            #print(response.content)
            #print(response.status_code)
            if response.status_code not in (200,201):
                return err_resp(err_code.ERR_GITEA_UPLOAD_FILE_FAILED, 
                                response.content[:500],
                                biz_code=response.status_code)
            else:
                return response.json()
        except requests.exceptions.JSONDecodeError:
            err_msg = "Response body does not contain valid json: {}".format(response)

    return err_resp(err_code.ERR_FAILED, 
                    err_msg[:500],
                    biz_code=response.status_code)

def _download(url, download_path, headers):
    """
    Params
        :url: http url
        :download_path: download path
        :headers: headers
    Returns
        file
    """
    for _ in range(CONNECTION_RETRY_TIMES):
        try:
            response = requests.request('GET', url, headers=headers, timeout=CONNECTION_TIMEOUT)
            if response.status_code == 200:
                with open(download_path, 'wb') as file:
                    file.write(response.content)
                ret = {}
            elif response.status_code == 404:
                res_json = response.json()
                ret = err_resp(err_code.ERR_FILE_NOT_FOUND, 
                               res_json['message'],
                               response.status_code)
            else:
                ret = err_resp(err_code.ERR_GITEA_DOWNLOAD_FILE_FAILED, 
                               f'Download failed, response code: {response.status_code}',
                               response.status_code)

        except requests.exceptions.JSONDecodeError:
            err_msg = "Response body does not contain valid json: {}".format(response.status_code)
            ret = err_resp(err_code.ERR_GITEA_DOWNLOAD_FILE_FAILED, 
                           err_msg,
                           response.status_code)
            log.debug(err_msg)

    return ret

def request_aistudio_git_download(url, download_path):
    """
    请求AIStudio gitea文件下载
    """
    headers = _header_fill()
    res = _download(url, download_path, headers)
    return res

def request_aistudio_git_file_info(url):
    """
    请求AIStudio gitea 文件info
    """
    headers = _header_fill()
    res = _request_gitea('GET', url, headers, "")
    if 'errors' in res:
        error_msg = str(res)[:500]
        if "The target couldn't be found." in error_msg:
            error_code = err_code.ERR_FILE_NOT_FOUND
        else:
            error_code = err_code.ERR_GITEA_GET_FILEINFO_FAILED
        res = err_resp(error_code, 
                       error_msg, 
                       None)
    return res


def stub_request_aistudio_git_file_type(func):
    def wrapper(*args, **kwargs):
        return {'is_lfs': True}  # 这里返回固定结果
    return wrapper
# TODO
#@stub_request_aistudio_git_file_type
def request_aistudio_git_file_type(call_host, user_name, repo_name, revision, file_size, path_in_repo):
    """
    请求AIStudio gitea 确认文件类型
    """
    headers = _header_fill()

    url = f"{call_host}/{quote(user_name, safe='')}/{quote(repo_name, safe='')}/preupload/{quote(revision, safe='')}"
    params = {
        "files": [{
            #"size": file_size, # 单位byte
            "path": path_in_repo # 远程文件路径（相对于仓库根路径）
        }]
    }
    payload = json.dumps(params)
    res = _request_gitea('POST', url, headers, data=payload)

    if 'errors' in res:
        error_msg = str(res)[:500]
        if "The target couldn't be found." in error_msg:
            error_code = err_code.ERR_FILE_NOT_FOUND
        else:
            error_code = err_code.ERR_GITEA_GET_FILEINFO_FAILED
        res = err_resp(error_code, 
                       error_msg, 
                       None)
    else:
        res = {
            'is_lfs': res['files'][0]['lfs']
        }

    return res


def stub_request_aistudio_git_upload_access(func):
    def wrapper(*args, **kwargs):
        
        return {
            'action': {
                'upload': {'href': 'http://s3.bj.bcebos.com/gitea-dev/lfs/ef/f5/aad94d8225d7df501ff774199a9f7bb52ae3b41654703ef71b087654cb69?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ALTAKhghJFNJOsGEYB0doZXmIm%2F20230914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230914T095322Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=d6ef605f1f7961684eed1850ed3390ffc36d6e26df07349af31abfd9689dc7b4'}
            }
        }  # 这里返回固定结果
    return wrapper

#@stub_request_aistudio_git_upload_access
def request_aistudio_git_upload_access(call_host, user_name, repo_name, revision, file_size, sha256):
    """
    请求AIStudio gitea 申请上传LFS文件
    """
    params = {
        'Content-Type': 'application/vnd.git-lfs+json; charset=utf-8',
        'Accept': 'application/vnd.git-lfs+json'
    }
    headers = _header_fill_with_params(params)

    url = f"{call_host}/{quote(user_name, safe='')}/{quote(repo_name, safe='')}.git/info/lfs/objects/batch"

    params = {
        "operation": "upload", # 申请动作为上传
        "objects": [
            {
                "oid": sha256, # SHA256哈希
                "size": file_size  # 单位byte
            }
        ],
        "transfers": [
            "lfs-standalone-file", "basic"
        ],
        "ref": {
            "name": f"refs/heads/{revision}" # 分支
        },
        "hash_algo": "sha256"
    }
    
    payload = json.dumps(params)
    res = _request_gitea('POST', url, headers, payload)
    #print(res)

    if 'errors' in res:
        error_msg = str(res)[:500]
        if "The target couldn't be found." in error_msg:
            error_code = err_code.ERR_FILE_NOT_FOUND
        else:
            error_code = err_code.ERR_GITEA_GET_FILEINFO_FAILED
        res = err_resp(error_code, 
                       error_msg, 
                       None)
    else:
        tmp = res['objects'][0]
        res = {
           'upload_href': tmp['actions']['upload']['href'] if 'actions' in tmp else ''
        }

    return res


def request_bos_upload(url, path_or_fileobj):
    """
    请求AIStudio gitea 进行上传LFS文件到bos
    """
    params = {'Content-Type': 'application/octet-stream'}
    headers = _header_fill_with_params(params)

    for _ in range(CONNECTION_RETRY_TIMES):
        try:
            err_msg = ''
            with open(path_or_fileobj, 'rb') as file:
                # 使用stream=True以避免一次性读取整个文件到内存中
                response = requests.request('PUT', url, headers=headers, data=file, timeout=CONNECTION_TIMEOUT, stream=True)
            print('finish')
            return {'Content-Md5': response.headers['Content-Md5']}

        except requests.exceptions.JSONDecodeError:
            err_msg = "Response body does not contain valid json: {}".format(response)
            biz_code = response.status_code
            log.debug(err_msg)
            #print(err_msg)
            return err_resp(err_code.ERR_FAILED, 
                    err_msg[:500],
                    biz_code)


def stub_request_aistudio_git_upload_pointer(func):
    def wrapper(*args, **kwargs):
        return {
        }  # 这里返回固定结果
    return wrapper
# TODO
#@stub_request_aistudio_git_upload_pointer
def request_aistudio_git_upload_pointer(call_host, user_name, repo_name, revision, commit_message, sha256, file_size, path_in_repo):
    """
    请求AIStudio gitea 上传LFS指针文件（到仓库）
    """
    headers = _header_fill()
    url = f"{call_host}/api/v1/repos/{quote(user_name, safe='')}/{quote(repo_name, safe='')}/contents/{quote(path_in_repo, safe='')}"
    params = {
        "branch": revision,     # 提交的分支
        "new_branch": revision, # 提交的分支
        "content": create_sha256_file_and_encode_base64(sha256, file_size),
        "lfsPointer": True,
        "dates": {"author": gen_ISO_format_datestr(),"committer": gen_ISO_format_datestr()},
        "message": commit_message
    }
    payload = json.dumps(params)
    res = _request_gitea('POST', url, headers, payload)

    if 'errors' in res:
        error_msg = str(res)[:500]
        if "The target couldn't be found." in error_msg:
            error_code = err_code.ERR_FILE_NOT_FOUND
        else:
            error_code = err_code.ERR_GITEA_GET_FILEINFO_FAILED
        res = err_resp(error_code, 
                       error_msg, 
                       None)
    else:
        # # Response StatusCode 201  TODO
        pass
        # res = {
        #     'actions': res['objects'][0]['actions']
        # }

    return res


def request_aistudio_git_upload_common(call_host, user_name, repo_name, revision, commit_message, path_or_fileobj, path_in_repo):
    """
    请求AIStudio gitea 上传普通文件（到仓库）
    """
    headers = _header_fill()
    url = f"{call_host}/api/v1/repos/{quote(user_name, safe='')}/{quote(repo_name, safe='')}/contents/{quote(path_in_repo, safe='')}"
    content_MD5 = gen_MD5(path_or_fileobj)
    params = {
        # TODO 邮箱怎么获取？
        #"author": {"email": "guoliangshuai@baidu.com","name": f"{user_name}"},
        #"committer": {"email": "guoliangshuai@baidu.com","name": f"{user_name}"},
        "branch": revision,     # 提交的分支
        "new_branch": revision, # 提交的分支
        "content": gen_base64(content_MD5),
        "lfs": False,
        "dates": {
            "author": gen_ISO_format_datestr(),
            "committer": gen_ISO_format_datestr()
        },
        "message": commit_message
    }
    payload = json.dumps(params)
    res = _request_gitea('POST', url, headers, payload)
    if 'errors' in res:
        error_msg = str(res)[:500]
        if "The target couldn't be found." in error_msg:
            error_code = err_code.ERR_FILE_NOT_FOUND
        else:
            error_code = err_code.ERR_GITEA_GET_FILEINFO_FAILED
        res = err_resp(error_code, 
                       error_msg, 
                       None)
    else:
        # # Response StatusCode 201  TODO
        pass

    return res


def _header_fill_with_params(params):
    """
    填充header
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {os.getenv("AISTUDIO_ACCESS_TOKEN", default="")}',
        'SDK-Version': str(VERSION)
    }
    headers.update(params)
    return headers


def _header_fill():
    """
    将环境变量的token填充到header
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {os.getenv("AISTUDIO_ACCESS_TOKEN", default="")}',
        'SDK-Version': str(VERSION)
    }
    return headers

