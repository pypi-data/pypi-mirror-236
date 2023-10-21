
from minio import Minio
# import pandas as pd
import datetime
from minio import Minio
import pandas as pd
import datetime
import requests
import json
import os

class CatalystStorage:

    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(cls)
    # def __init__(self,**kwargs):
    def __init__(self,tenant_point,apikey):
        if not (isinstance(tenant_point,str)) or tenant_point =="":
                raise TypeError("tenant_point should be string")
        if not (isinstance(apikey,str)) or apikey =="":
                raise TypeError("apikey should be string")

        
        self.tenant_point = tenant_point
        self.apikey = apikey
        
        # for key, value in kwargs.items():
        #     if key not in ['tenant_point','apikey']:
        #         raise TypeError("invalid parameter")
        #     else:
        #         setattr(self, key, value)

    
    def getfiles(self,workspace_name,project_name):
        if not (isinstance(workspace_name,str)) or workspace_name =="":
                raise TypeError("workspace_name is missing")
        if not (isinstance(project_name,str)) or project_name =="":
                raise TypeError("project_name is missing")
        response = self.GetData(workspace_name,project_name)
        res = self.Send_response(response)
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
        # validate user
        response = self.validate_user(workspace_name,project_name)
        if response.get("Type") == "Failed":
            return response.get("Message")
        else :
            # connect to MinIO
            minio_client = self.Connect_minio()
            # upload file to MinIO
            current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            dataset_size = os.path.getsize(data)
            return_data = self.add_minio_data(minio_client,response,current_time,data,dataset_name)
            # insert into DB 
            if return_data == "Success":
                insert_res = self.insertrecord(response,current_time,dataset_size,dataset_name)
                return insert_res.get('Message')
            else:
                return return_data
    
    def validate_user(self,workspace_name,project_name):
        api_url = self.tenant_point+'/api/v1/workbench'
        try :
            response = requests.post('http://'+api_url + '/validate',
                json={"tenant_point":self.tenant_point,"apikey": self.apikey,"workspace_name": workspace_name,"project_name": project_name}
                )
            token = response.json()
            return token

        except Exception as e:
            return {"Type": "Failed", "Message": "service is not available,Please try again later", "Error":"service is not available,Please try again later"}

    def Connect_minio(self):
        try :
            minio_client = Minio(
            "storage.catalystlabs.ai:9000",
            access_key = "HBbMqITM5SAv6MbnU18N",
            secret_key = "O7LWGjCks8TltKK5CCXOCJ5yg8sEciclvlSkrXQR",
            secure=True,
            )
            return minio_client
        except Exception as e:
            return e
    
        
    def add_minio_data(self,minio_client,res,current_time,data,dataset_name):
        try:
            user_id = res.get('Data').get('user_id')
            workspace_id = res.get('Data').get('workspace_id')
            project_id = res.get('Data').get('project_id')
            
            object_name = str(workspace_id) +"/"+str(project_id)+"/data-files/"+str(current_time)+"/"+str(dataset_name)
            found = minio_client.bucket_exists(str(user_id))
            if not found:
                try :
                    minio_client.make_bucket(str(user_id))
                    result = minio_client.fput_object(user_id,object_name,data)
                    return "Success"
                except Exception as e:
                    return "Can not create Bucket"
            
            else:
                try:
                    result = minio_client.fput_object(user_id,object_name,data)
                    return "Success"
                except Exception as e:
                    return "Can not upload file to storage"
        except Exception as e:
            return "Failed"
    
    def insertrecord(self,res,current_time,dataset_size,dataset_name):
        user_id = res.get('Data').get('user_id')
        workspace_id = res.get('Data').get('workspace_id')
        project_id = res.get('Data').get('project_id')
        user_name = res.get('Data').get('user_name')
        api_url = self.tenant_point+'/api/v1/workbench'
        try :
            response = requests.post('http://'+api_url + '/upload',
                json={"user_id": user_id,"workspace_id": workspace_id,"project_id": project_id,"current_time":current_time,"dataset_name":dataset_name,"dataset_size":dataset_size,"user_name":user_name}
                )
            token = response.json()
            return token

        except Exception as e:
            return {"Type": "Failed", "Message": "service is not available,Please try again later", "Error":"service is not available,Please try again later"}

        
    def GetData(self,workspace_name,project_name):
        api_url = self.tenant_point+'/api/v1/workbench'
        try :
            response = requests.post('http://'+api_url + '/get/files',
                json={"tenant_point":self.tenant_point,"apikey": self.apikey,"workspace_name": workspace_name,"project_name": project_name}
                )
            token = response.json()
            return token

        except Exception as e:
              return "service is not available,Please try again later"
            
    
    def Send_response(self,response):
        if response == "service is not available,Please try again later":
            return "service is not available,Please try again later"
        if response.get("Type") == "success":
            data = next(iter(response.values()))
            res = [d['dataset_name'] for d in data]
            return res
    #         df = pd.DataFrame(data)
    #         print(df)
        if response.get("Type") == "Failed":
            data = response.get("Message")
            return data



