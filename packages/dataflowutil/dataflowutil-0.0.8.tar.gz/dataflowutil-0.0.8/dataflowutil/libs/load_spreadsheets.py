from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import dataflowutil.config.extra_var as extra_v
import pandas as pd
from google.oauth2 import service_account

class LoadSpreadSheets:
    def __init__(self,connection):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        self.credentials = service_account.Credentials.from_service_account_file(os.path.join(extra_v.PATH_CREDENTIALS, connection.credentials_path), scopes=self.SCOPES)
        
        self.connection = False
        self.sheet = None
        self.load_function()

    def load_function(self):
        try:
            
            service = build('sheets', 'v4', credentials=self.credentials)
            self.sheet = service.spreadsheets()
            print("[LoadSpreadSheets] Succefull Connection function LoadSpreadSheets")
            self.connection = True
        except HttpError as err:
            print(err)
            self.connection = False
            print("[LoadSpreadSheets] Error: Connection function LoadSpreadSheets")


    def load_spreadsheets(self,id_spreadsheets,name_sheets):
        if self.connection:
            try:
                result = self.sheet.values().get(spreadsheetId=id_spreadsheets,
                                    range=name_sheets).execute()
                
                values = result.get('values', [])

                df = pd.DataFrame(values)
                df.columns = df.iloc[0]
                df.drop(df.index[0],inplace=True)

                return df
            
            except HttpError as err:
                print(err)
                return None
        else:
            print("[UploadSheets] Error: Connection function UploadSheets")

    def update_spreadsheets(self,id_spreadsheets,name_sheets,cell,value):
        if self.connection:
            try:
                self.sheet.values().update(spreadsheetId=id_spreadsheets,range=f"{name_sheets}!{cell}",
                            valueInputOption="USER_ENTERED" , body={"values": [[value]]}).execute()
                #print(f"[UploadSheets] Succefull: Edit id_sheets: {id_spreadsheets} // sheet_edit: {name_sheets}!{cell} // value: {value}")
            except HttpError as err:
                print(err)
        else:
            print("[UploadSheets] Error: Connection function UploadSheets")
