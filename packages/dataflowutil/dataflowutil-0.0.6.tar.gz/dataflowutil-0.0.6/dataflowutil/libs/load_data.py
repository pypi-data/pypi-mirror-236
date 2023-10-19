import pandas as pd
import dataflowutil.config.extra_var as extra_v

class LoadData:
    def __init__(self,connection,spreadsheets):
        self.cn = connection
        self.list_data = {}
        self.list_data_compare = {}
        self.spreadsheets = spreadsheets

        self.data = spreadsheets.load_spreadsheets(self.cn.id_spread_sheets,self.cn.page_sheet_bucket_to_bigquery)

        if extra_v.ACTIVATE_DATA_LOCAL:
            self.data_compare = spreadsheets.load_spreadsheets(self.cn.id_spread_sheets,self.cn.page_sheet_data_compare)

        self.load_data()

    def load_data(self):
        for index,row in self.data.iterrows():
            tag_name = row["TAG / DB_NAME"]
            path_data = row["PATH_BUCKET"]
            sheet_page = row["SHEET_PAGE"]
            type_data = row["TYPE"]
            update = int(row["UPDATE"])

            if isinstance(sheet_page,str):
                if "-" in sheet_page:
                    split_sheets = sheet_page.split("-")
                    sheet_page = [int(new_sheets) for new_sheets in split_sheets]
                else:
                    sheet_page = int(sheet_page)
                    
            self.list_data[tag_name] = {
                "path_data" : path_data,
                "sheet_page" : sheet_page,
                "type" :  extra_v.type_archives[type_data],
                "update" : update,
            }
        
        if extra_v.ACTIVATE_DATA_LOCAL:
            for index,row in self.data_compare.iterrows():
                tag_name = row["TAG / DB_NAME"]
                path_data_bucket = row["PATH_DATA_BUCKET"]
                path_data_local = row["PATH_DATA_LOCAL"]
                sheet_page = row["SHEET_PAGE"]
                type_data = row["TYPE"]
                update = int(row["UPDATE"])

                if isinstance(sheet_page,str):
                    if "-" in sheet_page:
                        split_sheets = sheet_page.split("-")
                        sheet_page = [int(new_sheets) for new_sheets in split_sheets]
                    else:
                        sheet_page = int(sheet_page)
                        
                self.list_data_compare[tag_name] = {
                    "path_data_bucket" : path_data_bucket,
                    "path_data_local" : path_data_local,
                    "sheet_page" : sheet_page,
                    "type" :  extra_v.type_archives[type_data],
                    "update" : update,
                }
                
    def get_data(self):
        return self.list_data

    def get_data_compare(self):
        return self.list_data_compare


