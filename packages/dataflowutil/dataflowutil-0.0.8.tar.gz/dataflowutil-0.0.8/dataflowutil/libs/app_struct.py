import dataflowutil.libs.load_data as ld
import dataflowutil.libs.load_bucket as lb
import dataflowutil.libs.upload_data as up
import dataflowutil.libs.load_connection as cn
import dataflowutil.libs.load_spreadsheets as up_sh
import dataflowutil.libs.load_report as ld_report

class AppStruct:
    def __init__(self):
        self.cn = cn.LoadConnection()

        self.us = up_sh.LoadSpreadSheets(self.cn)
        self.ld = ld.LoadData(self.cn,self.us)
        self.lb = lb.LoadBucket(self.cn,self.us)
        self.up = up.UploadData(self.cn,self.us)
        self.rp = ld_report.LoadReport(self.ld)
            
    #Start Load Data Buckets
    def load_data(self,db,reduce_memory=False):
        self.data = db.LoadDB(self.cn,self.lb,self.up,self.ld.get_data(),self.ld.get_data_compare(),reduce_memory)

    #GET all data load "ConfigData"
    def get_load_data(self):
        get_data = self.data.get_load_data()
        return get_data
    
    #Get all data local load "ConfigData"
    def get_load_data_local(self):
        get_data = self.data.get_load_data_local()
        return get_data

    #GET only data load "ConfigData"
    def get_only_data(self,tag=""):
        get_data = self.data.get_only_data(tag)
        return get_data

    #GET only data local load "ConfigData"
    def get_only_data_local(self,tag=""):
        get_data = self.data.get_only_data_local(tag)
        return get_data
    
    #Upload data to BigQuery
    def upload_load_data(self):
        self.data.upload_data()
    
    def get_data_compare(self,tag):
        get_data_compare = self.data.get_data_compare(tag)
        return get_data_compare

    #Get path list blobs Bucket
    def get_list_blobs(self):
        for name_file in self.lb.get_list_blobs(only_excel=True):
            print(name_file)
    
    #Upload data to Buckets
    def upload_data_buckets(self):
        self.lb.upload_files_bucket()
    
    #Load data SpreadSheets
    def load_spreadsheets(self,id_spreadsheets,name_sheets):
        get_load_spreadsheets = self.us.load_spreadsheets(id_spreadsheets,name_sheets)
        return get_load_spreadsheets

    #Upload data SpreadSheets
    def upload_spreadsheets(self,id_spreadsheets,name_sheets,cell,value):
        self.us.update_spreadsheets(id_spreadsheets,name_sheets,cell,value)

    #Functions Report
    def start_check_historic(self,tag=""):
        self.rp.start_check_historic(self.data,tag)
    
    def start_check_new(self,tag=""):
        self.rp.start_check_data_new(self.data,tag)
    

    #Functions BigQuery
    def run_routine(self,name_project,dataset,procedure):
        self.up.run_routine(name_project,dataset,procedure)

    def run_transfer(self,project_number,location,transfer_config_id):
        self.up.run_transfer(project_number,location,transfer_config_id)
    
    def select_query(self,query):
        return self.up.select_query(query)
