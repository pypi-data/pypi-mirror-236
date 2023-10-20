# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件实现了模型库hub接口封装

Authors: linyichong(linyichong@baidu.com)
Date:    2023/08/21
"""
import os
from pathlib import Path
from urllib.parse import quote
from aistudio_sdk.model_resources.abstract import APIResource
from aistudio_sdk.api_requester import request_aistudio_hub
from aistudio_sdk.api_requester import request_aistudio_git_download
from aistudio_sdk.api_requester import request_aistudio_git_file_info
from aistudio_sdk.api_requester import request_aistudio_git_file_type
from aistudio_sdk.api_requester import request_aistudio_git_upload_access
from aistudio_sdk.api_requester import request_bos_upload
from aistudio_sdk.api_requester import request_aistudio_git_upload_pointer
from aistudio_sdk.api_requester import request_aistudio_git_upload_common
from aistudio_sdk.util import convert_to_dict_object, is_valid_host, calculate_sha256
from aistudio_sdk.util import err_resp
from aistudio_sdk import err_code
from aistudio_sdk import config


__all__ = [
    "create_repo",
    "download",
    "upload"
]


class Hub(APIResource):
    """Hub类"""
    OBJECT_NAME = "hub"

    def __init__(self):
        """初始化函数，从本地磁盘加载AI Studio认证令牌。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        """

        # 当用户已经设置了AISTUDIO_ACCESS_TOKEN环境变量，那么优先读取环境变量，忽略本地磁盘存的token
        # 未设置时才读存本地token
        if not os.getenv("AISTUDIO_ACCESS_TOKEN", default=""):
            cache_home = os.getenv("AISTUDIO_CACHE_HOME", default=os.getenv("HOME"))
            token_file_path = f'{cache_home}/.cache/aistudio/.auth/token'
            if os.path.exists(token_file_path):
                with open(token_file_path, 'r') as file:
                    os.environ["AISTUDIO_ACCESS_TOKEN"] = file.read().strip()


    def create_repo(self, **kwargs):
        """
        创建一个repo仓库并返回创建成功后的信息。
        """
        # 参数检查
        str_params_not_valid = 'params not valid.'
        if "repo_id" not in kwargs:
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)

        if 'private' in kwargs and kwargs['private'] not in (True, False):
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)
        for key in ['repo_id', 'model_name', 'license', 'token']:
            if key in kwargs:
                if type(kwargs[key]) != str:
                    return err_resp(err_code.ERR_PARAMS_INVALID, 
                                    str_params_not_valid)
                kwargs[key] = kwargs[key].strip()
                if not kwargs[key]:
                    return err_resp(err_code.ERR_PARAMS_INVALID, 
                                    str_params_not_valid)

        if not os.getenv("AISTUDIO_ACCESS_TOKEN") and 'token' not in kwargs:
            return err_resp(err_code.ERR_TOKEN_IS_EMPTY,
                            'token have not been set.')

        if 'desc' in kwargs \
                and type(kwargs['desc']) != str:
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)

        # 兼容 带前缀的入参写法 TODO 未测试
        repo_name_raw = kwargs['repo_id']
        if "/" in repo_name_raw:
            user_name, repo_name = repo_name_raw.split('/')
            user_name = user_name.strip()
            repo_name = repo_name.strip()
            if not repo_name or not user_name:
                return err_resp(err_code.ERR_PARAMS_INVALID, 
                                str_params_not_valid)
            kwargs['repo_id'] = repo_name
        else:
            kwargs['repo_id'] = repo_name_raw

        params = {
            'repoType': 0 if kwargs.get('private') else 1,
            'repoName': kwargs['repo_id'],
            'modelName': kwargs['model_name'] if kwargs.get('model_name') else kwargs['repo_id'],
            'desc': kwargs.get('desc', ''),
            'license': kwargs['license'].strip() if kwargs.get('license') else 'Apache License 2.0',
            'token': kwargs['token'] if 'token' in kwargs else ''
        }
        resp = convert_to_dict_object(request_aistudio_hub(**params))
        if 'errorCode' in resp and resp['errorCode'] != 0:
            if "repo already created" in resp['errorMsg']:
                res = err_resp(err_code.ERR_REPO_EXISTS, 
                               resp['errorMsg'],
                               resp['errorCode'])
            else:
                res = err_resp(err_code.ERR_AISTUDIO_CREATE_REPO_FAILED, 
                               resp['errorMsg'],
                               resp['errorCode'])
            return res

        res = {
            'model_name': resp['result']['modelName'],
            'repo_id': resp['result']['repoName'],
            'private': True if resp['result']['repoType'] == 0 else False,
            'desc': resp['result']['desc'],
            'license': resp['result']['license']
        }
        return res


    def download(self, **kwargs):
        """
        下载
        """
        # 参数检查
        str_params_not_valid = 'params not valid.'
        if "repo_id" not in kwargs or "filename" not in kwargs:
            return err_resp(err_code.ERR_PARAMS_INVALID,
                            str_params_not_valid)

        for key in ['filename', 'repo_id', 'revision', 'cache_dir', 'token']:
            if key in kwargs:
                if type(kwargs[key]) != str:
                    return err_resp(err_code.ERR_PARAMS_INVALID, 
                                    str_params_not_valid)
                kwargs[key] = kwargs[key].strip()
                if not kwargs[key]:
                    return err_resp(err_code.ERR_PARAMS_INVALID, 
                                    str_params_not_valid)
        revision = kwargs['revision'] if kwargs.get('revision') else 'master'
        file_path = kwargs['filename']
        token = kwargs['token'] if 'token' in kwargs else ''

        repo_name = kwargs['repo_id']
        if "/" not in repo_name:
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)

        user_name, repo_name = repo_name.split('/')
        user_name = user_name.strip()
        repo_name = repo_name.strip()
        if not repo_name or not user_name:
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)

        call_host = os.getenv("STUDIO_GIT_HOST", default=config.STUDIO_GIT_HOST_DEFAULT)
        if not is_valid_host(call_host):
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            'host not valid.')

        # 查询文件sha值
        info_res = request_aistudio_git_file_info(call_host, user_name, repo_name, file_path, 
                                                  revision, token)
        if 'error_code' in info_res and info_res['error_code'] != err_code.ERR_OK:
            return info_res
        file_sha = info_res['sha']

        # 构建source_path
        home = os.getenv("HOME")
        cache_home = os.getenv("AISTUDIO_CACHE_HOME", default=home)
        source_dir = Path(f"{cache_home}/.cache/aistudio/models/{repo_name}/blobs")
        source_path = Path(f"{source_dir}/{file_sha}")

        # 检查目标文件是否已下载
        if os.path.exists(source_path):
            print("The file already exists, skip the download.")
        else:
            print('Start downloading.')
            # 创建下载文件目录
            os.makedirs(source_dir, exist_ok=True)
            url = f"{call_host}/api/v1/repos/{quote(user_name, safe='')}/{quote(repo_name, safe='')}/media/{quote(file_path, safe='')}"
            if revision != 'master':
                url += f"?ref={quote(revision, safe='')}"
            download_res = request_aistudio_git_download(url, source_path, token)
            if 'error_code' in download_res and download_res['error_code'] != err_code.ERR_OK:
                return download_res

        # 构建软链接的路径
        if 'cache_dir' in kwargs:
            cache_dir = kwargs['cache_dir']
            target_dir = Path(cache_dir)
        else:
            commit_id = info_res['last_commit_sha']
            target_dir = Path(f"{cache_home}/.cache/aistudio/models/{repo_name}/snapshots/{revision}/{commit_id}")  
        target_path = Path(f"{target_dir}/{file_path}")

        # 删掉已经存在的软链接文件
        if os.path.exists(target_path):
            os.unlink(target_path)

        # 预创建软链接文件所在目录
        parsed_path = Path(file_path)
        prefix_path = parsed_path.parent
        os.makedirs(os.path.join(target_dir, prefix_path), exist_ok=True)

        # 创建符号链接（软链接）
        if os.name == "nt":  # Windows系统  
            # 使用不同的命令来创建目录链接和文件链接
            if os.path.isdir(source_path):
                os.system(f"mklink /D \"{target_path}\" \"{source_path}\"")
            else:
                os.system(f"mklink \"{target_path}\" \"{source_path}\"")
        else:  # 非Windows系统（如Linux）
            os.symlink(source_path, target_path) 

        return {'path': f"{target_path}"}


    def upload(self, **kwargs):
        """
        上传
        """
        # 参数检查
        str_params_not_valid = 'params not valid.'
        if "repo_id" not in kwargs or "path_or_fileobj" not in kwargs or "path_in_repo" not in kwargs:
            return err_resp(err_code.ERR_PARAMS_INVALID,
                            str_params_not_valid)

        for key in ['path_or_fileobj', 'repo_id', 'revision', 'path_in_repo', 
                    'commit_message', 'token']:
            if key in kwargs:
                if type(kwargs[key]) != str:
                    return err_resp(err_code.ERR_PARAMS_INVALID, 
                                    str_params_not_valid)
                kwargs[key] = kwargs[key].strip()
                if not kwargs[key]:
                    return err_resp(err_code.ERR_PARAMS_INVALID, 
                                    str_params_not_valid)

        if not os.getenv("AISTUDIO_ACCESS_TOKEN") and 'token' not in kwargs:
            return err_resp(err_code.ERR_TOKEN_IS_EMPTY,
                            'token have not been set.')

        revision = kwargs['revision'] if kwargs.get('revision') else 'master'
        commit_message = kwargs['commit_message'] if kwargs.get('commit_message') else ''
        token = kwargs['token'] if kwargs.get('token') else ''

        path_or_fileobj = Path(kwargs['path_or_fileobj'])
        path_in_repo = kwargs['path_in_repo']

        repo_id = kwargs['repo_id']
        if "/" not in repo_id:
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)

        user_name, repo_name = repo_id.split('/')
        user_name = user_name.strip()
        repo_name = repo_name.strip()
        if not repo_name or not user_name:
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            str_params_not_valid)

        call_host = os.getenv("STUDIO_GIT_HOST", default=config.STUDIO_GIT_HOST_DEFAULT)
        if not is_valid_host(call_host):
            return err_resp(err_code.ERR_PARAMS_INVALID, 
                            'host not valid.')

        # 检查待上传文件在本地磁盘是否存在
        if not os.path.exists(path_or_fileobj):
            return err_resp(err_code.ERR_UPLOAD_FILE_NOT_FOUND,
                            'file not found.')

        # 检查待上传文件类型，不能是folder（目录）
        if os.path.isdir(path_or_fileobj):
            return err_resp(err_code.ERR_UPLOAD_FOLDER_NO_SUPPORT,
                            'upload folder no support.')

        # 计算文件大小（byte）
        file_size = os.path.getsize(path_or_fileobj)

        # 检查文件大小
        if file_size > config.LFS_FILE_SIZE_LIMIT:
            return err_resp(err_code.ERR_UPLOAD_FILE_TOO_LARGE,
                            'file too large(>5GB).')
        
        # 第一步: 检查文件是否需要走LFS上传流程
        res = request_aistudio_git_file_type(call_host, user_name, repo_name, 
                                             revision, path_in_repo, token)
        if 'error_code' in res and res['error_code'] != err_code.ERR_OK:
            return res
        is_lfs = res['is_lfs']

        # 计算sha256
        sha256 = calculate_sha256(path_or_fileobj)

        if is_lfs:
            print("Start uploading LFS file.")
            # 第二步：申请上传LFS文件

            res = request_aistudio_git_upload_access(call_host, user_name, repo_name, revision, 
                                                     file_size, sha256, token)
            if 'error_code' in res and res['error_code'] != err_code.ERR_OK:
                return res

            if res['upload_href']:
                upload_href = res['upload_href']

                # 第三步：上传LFS文件（到BOS）
                res = request_bos_upload(upload_href, path_or_fileobj)
                if 'error_code' in res and res['error_code'] != err_code.ERR_OK:
                    return res

            else:
                # bos存储中该文件已存在。只需要再创建一次指针文件到指定分支即可。
                pass

            # 第四步：上传LFS指针文件（到仓库）
            res = request_aistudio_git_upload_pointer(call_host, user_name, repo_name, revision, 
                                                    commit_message, sha256, file_size, path_in_repo,
                                                    token)
            if 'error_code' in res and res['error_code'] != err_code.ERR_OK:
                return res

        else:
            print("Start uploading Common file.")
            # 如果大小超标，报错返回
            if file_size > config.COMMON_FILE_SIZE_LIMIT:
                return err_resp(err_code.ERR_UPLOAD_FILE_TOO_LARGE,
                                'file too large(>5MB).')

            # 上传普通文件（到仓库）
            res = request_aistudio_git_upload_common(call_host, user_name, repo_name, revision, 
                                                    commit_message, path_or_fileobj, path_in_repo,
                                                    token)
            if 'error_code' in res and res['error_code'] != err_code.ERR_OK:
                return res

        return {'message': 'Upload Done.'}


def create_repo(**kwargs):
    """
    创建
    """
    return Hub().create_repo(**kwargs)

def download(**kwargs):
    """
    下载
    """
    return Hub().download(**kwargs)

def upload(**kwargs):
    """
    上传
    """
    return Hub().upload(**kwargs)

