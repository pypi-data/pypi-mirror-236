import pandas as pd
import os
import dataflowutil.config.extra_var as extra_var
import gc

class DataProcessing():
    def __init__(self,connection,path_bucket,cx_bigquery):
        self.cn = connection
        self.raw_data = {}
        self.raw_data_local = {}
        self.path_bucket = path_bucket
        self.cx_bigquery = cx_bigquery
    
    def load_data(self,data_get,data_get_compare,reduce_memory=False):
        try:        
            if extra_var.ACTIVATE_DATA_LOCAL:
                index = 0
                for data_strct_key,data_strct_value in data_get_compare.items():

                    update_status = data_strct_value["update"]
                    index += 1
                    if update_status == extra_var.STATUS_UPDATE["UPDATE"] or update_status == extra_var.STATUS_UPDATE["NO_LOAD"]:
                        continue
                    
                    name_data = data_strct_value["path_data_local"]
                    ruta = f"{extra_var.DIRNAME_UPLOAD_BUCKET}/{name_data}"
                    patch = os.path.isfile(ruta)
                    if patch:
                        tag = data_strct_key
                        sheet_index = data_strct_value["sheet_page"]
                        type_format = data_strct_value["type"].split("|")

                        if isinstance(sheet_index,list):
                            if len(sheet_index) > 1:
                                df_start = self.func_load_data(type_format,name_data,ruta,sheet_index[0])
                                for pages_sheet in range(1,len(sheet_index)):
                                    df_extra = self.func_load_data(type_format,name_data,ruta,sheet_index[pages_sheet])
                                    df_start = pd.concat([df_start, df_extra],axis=0).reset_index(drop=True)
                                    
                                df_start = df_start.rename(columns=lambda x: str(x).replace(' ', '_'))
                                self.raw_data_local[tag] = [df_start, tag, index]
                        else:
                            data = self.func_load_data(type_format,name_data,ruta,sheet_index)
                            data = data.rename(columns=lambda x: str(x).replace(' ', '_'))
                            self.raw_data_local[tag] = [ data , tag, index]
                    
                    
                self.func_load_data_bucket(data_get_compare,reduce_memory)

            else:
                self.func_load_data_bucket(data_get,reduce_memory)
        except:
            import sys
            tipo_excepcion, valor_excepcion, traceback = sys.exc_info()
            
            print("Tipo de excepción:", tipo_excepcion)
            print("Valor de excepción:", valor_excepcion)
            print("Traceback:", traceback)
            print(f"[LoadData] Error Load Data.")


    def func_load_data_bucket(self,data_get_func,reduce_memory=False):
        index = 0
        name_file = self.path_bucket.get_list_blobs(only_excel=True)

        if reduce_memory:
            print("[LoadData] Reduce_Memory: Successful")

        for data_strct_key,data_strct_value in data_get_func.items():
            update_status = data_strct_value["update"]
            index += 1
            if update_status == extra_var.STATUS_UPDATE["UPDATE"] or update_status == extra_var.STATUS_UPDATE["NO_LOAD"]:
                continue

            if extra_var.ACTIVATE_DATA_LOCAL:
                name_data = data_strct_value["path_data_bucket"]
            else:
                name_data = data_strct_value["path_data"]

            #Func Load Data Bucket
            if name_data in name_file:
                tag = data_strct_key
                sheet_index = data_strct_value["sheet_page"]
                type_format = data_strct_value["type"].split("|")
                if isinstance(sheet_index,list):
                    if len(sheet_index) > 1:
                        df_start = self.func_load_data(type_format,name_data,self.cn.bucket_path+name_data,sheet_index[0])
                        for pages_sheet in range(1,len(sheet_index)):
                            df_extra = self.func_load_data(type_format,name_data,self.cn.bucket_path+name_data,sheet_index[pages_sheet])
                            df_start = pd.concat([df_start, df_extra],axis=0).reset_index(drop=True)
                        
                        df_start = df_start.rename(columns=lambda x: str(x).replace(' ', '_'))
                        self.raw_data[tag] = [df_start, tag, index]
                        
                        print(f"[LoadData] Successful Load Data: NAME_DATA: {tag} ")

                        if reduce_memory:
                            self.upload_data()
                            self.raw_data = {}
                            df_start = None
                            gc.collect()

                else:
                    data = self.func_load_data(type_format,name_data,self.cn.bucket_path+name_data,sheet_index)
                    data = data.rename(columns=lambda x: str(x).replace(' ', '_'))
                    self.raw_data[tag] = [ data , tag, index]
                    print(f"[LoadData] Successful Load Data: NAME_DATA: {tag} ")

                    if reduce_memory:
                        self.upload_data()
                        self.raw_data = {}
                        df_start = None
                        gc.collect()


    def get_load_data(self):
        return self.raw_data

    def get_load_data_local(self):
        return self.raw_data_local
    
    def get_data_compare(self,tag_func):
        return (self.raw_data[tag_func][0],self.raw_data_local[tag_func][0])

    def get_only_data(self,tag):
        return self.raw_data[tag][0]

    def get_only_data_local(self,tag):
        return self.raw_data_local[tag][0]

    def transformation(name_tag):
        def sub_transformation(func):
            def wrapper(self):
                data =  self.get_only_data(name_tag)
                result = func(self, data)
                self.upload_transformation(name_tag,result)
                return result
            return wrapper
        return sub_transformation
    
    def upload_transformation(self,name_tag_data,df_tf):
        data_all = self.get_load_data()
        data_all[name_tag_data][0] = df_tf
    
    def upload_data(self):
        data_upload = self.get_load_data()
        self.cx_bigquery.upload_data(data_upload)
    
    def func_load_data(self,type_format,name_file,path_archive,sheet_page):
        if len(type_format) > 1:
            format_archive = name_file.split("/")[-1].split(".")[-1]
        else:
            format_archive = type_format[0]
                
        if "xlsx" in format_archive:           
            return pd.read_excel(path_archive,sheet_name=int(sheet_page))
        if "csv" in format_archive:
            return pd.read_csv(path_archive)