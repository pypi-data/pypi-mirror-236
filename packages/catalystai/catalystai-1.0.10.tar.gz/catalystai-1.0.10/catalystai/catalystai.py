from minio import Minio
import datetime
import requests
import os
import urllib3
from typing import Union
from .schema import (Response,FileResponse)
class CatalystStorage:

    """
    Allows user to get list of all files in a specific workspace and project.
    Allows user to upload the data to Catalyst Storage for a specific workspace and project.

    :param tenant_domain:
        Catalyst AI domain.

    :param apikey:
        ApiKey generated from the platform.
    """

    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(cls)
    # def __init__(self,**kwargs):
    def __init__(self,tenant_domain,apikey) -> None:
        if not (isinstance(tenant_domain,str)) or tenant_domain =="":
                raise TypeError("tenant_domain should be string")
        if not (isinstance(apikey,str)) or apikey =="":
                raise TypeError("apikey should be string")
        
        self.tenant_domain = tenant_domain
        self.apikey = apikey
        
        
        # for key, value in kwargs.items():
        #     if key not in ['tenant_domain','apikey']:
        #         raise TypeError("invalid parameter")
        #     else:
        #         setattr(self, key, value)

    
    def getfiles(self,workspace_name,project_name) -> Union[Response, FileResponse] :

        if not (isinstance(workspace_name,str)) or workspace_name =="":
                raise TypeError("workspace_name is missing")
        if not (isinstance(project_name,str)) or project_name =="":
                raise TypeError("project_name is missing")
        
        secrets = "apps-catalyst-service-v1-2.onrender.com"
        if secrets != self.tenant_domain:
             return "Tenant Domain is incorrect,Please check again !"
        
        response = self.get_data(workspace_name,project_name)
        
        if response.get('data')== None and response.get('type')=='Failed':
            return response.get('message')
        elif response.get('data')== None and response.get('type')=='success':
            return f'No file found in "{project_name}" project.Start exploring CatalystAI services with your data.'
        # 'No Data found'
        else:
            res = self.send_response(response)
            return res
        
    def get_data(self,workspace_name,project_name) -> Response:
        api_url = self.tenant_domain+'/api/v1/workbench'
        try :
            response = requests.post('https://'+api_url + '/get/files',
                json={"tenant_domain":self.tenant_domain,"apikey": self.apikey,"workspace_name": workspace_name,"project_name": project_name}
                )
            token = response.json()
            result = {
                "data":token.get("data"),
                "message":token.get("message"),
                "type":token.get("type") 
            }
            return result

        except Exception as e:
            result = {'data': None, 'message': 'Failed !', 'type': 'Fail'}
            return result
            
    
    def send_response(self,response) -> FileResponse:
            data = next(iter(response.values()))
            res = [d['dataset_name'] for d in data]
            return res
    
    def uploadfiles(self,workspace_name,project_name,data,dataset_name):

        if not (isinstance(workspace_name,str)) or workspace_name =="":
                raise TypeError("workspace_name is missing")
        if not (isinstance(project_name,str)) or project_name =="":
                raise TypeError("project_name is missing")
        if not (isinstance(data,str)) or data =="":
                raise TypeError("data is missing")
        if not (isinstance(dataset_name,str)) or dataset_name =="":
                raise TypeError("dataset_name is missing")
        
        secrets = "apps-catalyst-service-v1-2.onrender.com"
        if secrets != self.tenant_domain:
             return "Tenant Domain is incorrect,Please check again !"
        
        
        # validate user
        response = self.validate_user(workspace_name,project_name)
        if response.get('data') == None:
            return response.get("message")
        else :
            # connect to MinIO
            minio_client = self.connect_minio()
            if minio_client.get('data') == None:
                return minio_client.get("message")
            else:
                # upload file to MinIO
                current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                dataset_size = os.path.getsize(data)
                client = minio_client.get('data')
                return_data = self.add_minio_data(client,response,current_time,data,dataset_name)
                
                # insert into DB  
                if return_data.get('data') == None:
                    return return_data.get('message')   
                else:
                    insert_res = self.insert_record(response,current_time,dataset_size,dataset_name)
                    return insert_res.get('message')
    
    def validate_user(self,workspace_name,project_name) -> Response:
        api_url = self.tenant_domain+'/api/v1/workbench'
        try :
            response = requests.post('https://'+api_url + '/validate',
                json={"tenant_domain":self.tenant_domain,"apikey": self.apikey,"workspace_name": workspace_name,"project_name": project_name}
                )
            token = response.json()
            result = {
                "data":token.get("data"),
                "message":token.get("message"),
                "type":token.get("type")
                
            }
            return result

        except Exception as e:
            return {"data":None,"type": "Failed", "message": "service is not available,Please try again later"}

    def connect_minio(self) -> Response:
            # minio_endpoint = os.getenv('MINIO_ENDPOINT')
            # access_key = os.getenv('MINIO_ACCESSKEY')
            # secret_key = os.getenv('MINIO_SECRETKEY')

            minio_client = Minio("storage.catalystlabs.ai:9000",
            access_key = "KVJxvhyWQ5JQByPzrO97",
            secret_key = "hsTsv5eKto2ZoXf8FWkOEdindELMwWNvWyc164Qb",
            secure=True,
            # http_client=urllib3.ProxyManager(
            #      "https://storage.catalystlabs.ai:9000",
            #                 retries=urllib3.Retry(
            #                     total=5,
            #                     backoff_factor=0.2,
            #                     status_forcelist=[500, 502, 503, 504],
            #                 ),
            #             ),
            )
            
            try:
                if not minio_client.bucket_exists("nonexistingbucket"):
                    result = {'data': minio_client, 'message': 'Success', 'type': 'Success'}
                    return result
            except:
                result = {'data': None, 'message': 'Catalyst Storage is unavailable,Please try again later !', 'type': 'Fail'}
                return result
        
    def add_minio_data(self,minio_client,res,current_time,data,dataset_name) -> Response:
        try:
            user_id = res.get('data').get('user_id')
            workspace_id = res.get('data').get('workspace_id')
            project_id = res.get('data').get('project_id')
            
            object_name = str(workspace_id) +"/"+str(project_id)+"/data-files/"+str(current_time)+"/"+str(dataset_name)
            found = minio_client.bucket_exists(str(user_id))
            if not found:
                try :
                    minio_client.make_bucket(str(user_id))
                    result = minio_client.fput_object(user_id,object_name,data)
                    response = {'data': 'Success', 'message': 'File uploaded successfully', 'type': 'Success'}
                    return response
                except Exception as e:
                    response = {'data': None, 'message': 'Can not create Bucket', 'type': 'Fail'}
                    return response
            
            else:
                try:
                    result = minio_client.fput_object(user_id,object_name,data)
                    response = {'data': 'success', 'message': 'File uploaded successfully', 'type': 'Success'}
                    return response
                except Exception as e:
                    response = {'data': None, 'message': 'Can not upload file to storage', 'type': 'Fail'}
                    return response
        except Exception as e:
            response = {'data': None, 'message': 'Can not upload file to storage,please try again later', 'type': 'Fail'}
            return response
    
    def insert_record(self,res,current_time,dataset_size,dataset_name) -> Response:
        user_id = res.get('data').get('user_id')
        workspace_id = res.get('data').get('workspace_id')
        project_id = res.get('data').get('project_id')
        user_name = res.get('data').get('user_name')
        api_url = self.tenant_domain+'/api/v1/workbench'
        try :
            response = requests.post('https://'+api_url + '/upload',
                json={"user_id": user_id,"workspace_id": workspace_id,"project_id": project_id,"current_time":current_time,"dataset_name":dataset_name,"dataset_size":dataset_size,"user_name":user_name}
                )
            token = response.json()
            result = {
                "data":"Success",
                "message":token.get("message"),
                "type":token.get("type")
                
            }
            return result

        except Exception as e:
            return {"data":None,"type": "Failed", "message": "Service is not available,Please try again later"}
