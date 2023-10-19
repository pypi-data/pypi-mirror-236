import os
import time
import pandas_gbq
from pandas.io import gbq
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
import dataflowutil.config.extra_var as extra_v
from google.cloud import bigquery_datatransfer_v1
from google.protobuf.timestamp_pb2 import Timestamp

class UploadData:
    def __init__(self,connection,spreadsheets):
        self.cn = connection
        self.spreadsheets = spreadsheets
        self.credentials = service_account.Credentials.from_service_account_file(os.path.join(extra_v.PATH_CREDENTIALS, self.cn.credentials_path) ) # Same Credentials Storage Client
        self.client = bigquery.Client()

    def select_query(self,query):
        df_get = gbq.read_gbq(query,project_id = self.cn.project_id,credentials=self.credentials)
        return df_get

    def run_routine(self,name_project,dataset,procedure):
        query = f'CALL `{name_project}.{dataset}.{procedure}`();'
        query_job = self.client.query(query)
        print(query_job.result())
        print(f'[Run_Routine] Stored procedure {name_project}.{dataset}.{procedure} executed successfully..')
    
    def run_transfer(self,project_number,location,transfer_config_id):
        parent = 'projects/' + project_number + '/locations/' + location + '/transferConfigs/' + transfer_config_id
        
        clientBQTransfer = bigquery_datatransfer_v1.DataTransferServiceClient()

        start_time = Timestamp(seconds=int(time.time()))

        request = bigquery_datatransfer_v1.types.StartManualTransferRunsRequest(
            { "parent": parent, "requested_run_time": start_time }
        )

        response = clientBQTransfer.start_manual_transfer_runs(request, timeout=360)
        for run in response.runs:
            print(f"Ejecución iniciada con ID: {run.name}")

        print(f'[Run_Transfer] Successful Transfer {parent} executed successfully..')

    def upload_data(self,raw_data,method="replace"):
        if len(raw_data) <= 0:
            print("[UploadData] Alert: 0 items found to update.")
            return
        
        for df_upload,tag,index in raw_data.values():
            try:
                #Replace DTypes and Replace all types Objects to String
                df_upload = df_upload.convert_dtypes()
                for col in df_upload.select_dtypes(include='object'):
                    df_upload[col] = df_upload[col].astype("string") 

                pandas_gbq.to_gbq(df_upload,f"{self.cn.name_db_bigquery}.{tag}", project_id=self.cn.project_id,credentials=self.credentials,if_exists=method)
                print(f"[UploadData] Successful Upload Data: NAME_DATA: {tag} // DB_NAME: {self.cn.name_db_bigquery} // ProjectID: {self.cn.project_id}")
                self.spreadsheets.update_spreadsheets(self.cn.id_spread_sheets,self.cn.page_sheet_bucket_to_bigquery,f"F{index+1}",str(datetime.now()))
                self.spreadsheets.update_spreadsheets(self.cn.id_spread_sheets,self.cn.page_sheet_bucket_to_bigquery,f"E{index+1}",extra_v.STATUS_UPDATE["UPDATE"])
                
            except:
                import sys
                tipo_excepcion, valor_excepcion, traceback = sys.exc_info()
                print("Tipo de excepción:", tipo_excepcion)
                print("Valor de excepción:", valor_excepcion)
                print("Traceback:", traceback)
                print(f"[UploadData] Error Upload Data: NAME_DATA: {tag} // DB_NAME: {self.cn.name_db_bigquery} // ProjectID: {self.cn.project_id}")
        
        df_upload = None
        raw_data = None
