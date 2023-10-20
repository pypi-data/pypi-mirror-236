import pandas as pd
from ipywidgets import interactive, fixed, IntSlider, HBox, Layout,widgets
from IPython.display import display, HTML

CHECK_ALERT_S = "S"
CHECK_ALERT_N = "N"
CHECK_ALERT_G = "G"

class LoadReport():
    def __init__(self,ld):

        self.list_tags = []
        self.load_tags(ld)
        
        self.is_widgets = False
        self.data_bucket = None
        self.data_local = None
        self.data_local_historic = None
        self.data_local_new = None

    def clear(self):
        self.data_bucket = None
        self.data_local = None
        self.data_local_historic = None
        self.data_local_new = None

    def load_tags(self,ld):
        get_tags = ld.get_data_compare()
        self.list_tags = []
        for key,value in get_tags.items():
            if not value["update"]:
                self.list_tags.append(key)
            
    def check_alert_print(self,text,val="S"):

        
        if "S" in val:
            if self.is_widgets:
                display(HTML(f"<span style='color: green; '>✔ [LoadReport] {text}</span>"))
            else:
                print(f'\033[1;32m✔ [LoadReport] {text}')
        if "N" in val:
            if self.is_widgets:
                display(HTML(f"<span style='color: red;'>✗ [LoadReport] {text}</span>"))
            else:
                print(f'\033[1;31m✗ [LoadReport] {text}')
        if "G" in val:
            if self.is_widgets:
                display(HTML(f"<span style='color: DodgerBlue;'>▶ [LoadReport] {text}</span>"))
            else:    
                print(f'\033[1;36m▶ [LoadReport] {text}')

    def check_lenght_historic(self):
        data_bucket_shape = self.data_bucket.shape[0]
        data_local_shape = self.data_local.shape[0]

        if data_local_shape < data_bucket_shape:
            self.check_alert_print("Error in lenght data , len data_bucket < data_local",CHECK_ALERT_N)
            return False

        return True

    def check_columns_all_df(self,column_check):
        if column_check not in self.data_bucket.columns:
            return False
        
        if column_check not in self.data_local_historic.columns:
            return False
        
        return True

    def get_df_na_rows(self,column_check,dropna_check = False):
        merged_df = pd.merge(self.data_local_historic[f"{column_check}"], self.data_bucket[f"{column_check}"], left_index=True, right_index=True, suffixes=('_local', '_bucket'))
        different_rows = merged_df[merged_df[f'{column_check}_local'] != merged_df[f'{column_check}_bucket']]
        if dropna_check:
            different_rows = different_rows.dropna(how="all",subset=[f'{column_check}_local',f'{column_check}_bucket'])

        #if different_rows[f"{column_check}_local"].isna().sum() != 0 and different_rows[f"{column_check}_bucket"].isna().sum() != 0:
           # if different_rows[f"{column_check}_local"].isna().sum() == different_rows[f"{column_check}_bucket"].isna().sum():
                #return True
        
        if different_rows[f"{column_check}_local"].shape[0] <= 0 and different_rows[f"{column_check}_bucket"].shape[0] <= 0:
            return True
        
        return False

    def get_df_negative(self,column_check,dropna_check = False):
        merged_df = pd.merge(self.data_local_historic[f"{column_check}"], self.data_bucket[f"{column_check}"], left_index=True, right_index=True, suffixes=('_local', '_bucket'))
        #different_rows = merged_df[merged_df[f'{column_check}_local'] != merged_df[f'{column_check}_bucket']]
        different_rows =  merged_df
        if dropna_check:
            different_rows = different_rows.dropna(how="all",subset=[f'{column_check}_local',f'{column_check}_bucket'])

        #if different_rows[f"{column_check}_local"].isna().sum() != 0 and different_rows[f"{column_check}_bucket"].isna().sum() != 0:
           # if different_rows[f"{column_check}_local"].isna().sum() == different_rows[f"{column_check}_bucket"].isna().sum():
                #return True
        
        if different_rows[f"{column_check}_local"].shape[0] > 0 and different_rows[f"{column_check}_bucket"].shape[0] > 0:

            if different_rows[f"{column_check}_local"].dtype in ['int64', 'float64'] and different_rows[f"{column_check}_bucket"].dtype in ['int64', 'float64']:
                if (different_rows[f"{column_check}_local"] < 0).any() or (different_rows[f"{column_check}_bucket"] < 0).any():
                    return False

        return True
    
    
    def check_count_columns(self,display_check=False):
        count = 1 - abs(len(self.data_bucket.columns) - len(self.data_local.columns)) / max(len(self.data_bucket.columns) , len(self.data_local.columns))
        columns_check = {
            "count_columns_data_bucket" : [len(self.data_bucket.columns)],
            "count_columns_data_local" : [len(self.data_local.columns)],
            "error" : [count]
        }

        if display_check:
            display(pd.DataFrame(columns_check))

        if count < 1:
            self.check_alert_print("DataFrames have different number of columns.",CHECK_ALERT_N)
            return False
        return True

    def check_report_all(self,display_check=False,dropna_check=False):
        data_local = self.data_local_historic

        list_columns_bucket = self.data_bucket.columns
        list_columns_local  = data_local.columns

        data_check_test = pd.DataFrame([list_columns_bucket,list_columns_local]).T
        data_check_test.rename(columns = {0:"corr_columns_data_bucket",1:"corr_columns_data_local"}, inplace = True)
        data_check_test["Checks"] = False

        for key,value in dict(self.data_bucket.eq(data_local).all()).items():
            if value:
                data_check_test.loc[(data_check_test["corr_columns_data_bucket"] == key),"Checks"] = True
                self.check_alert_print(f"Corr in variable ( {key} )",CHECK_ALERT_S)
            else:
                if self.check_columns_all_df(key):

                    get_df_check = self.get_df_na_rows(key,dropna_check=dropna_check)
                    get_df_negative = self.get_df_negative(key,dropna_check=dropna_check)

                    if get_df_check and get_df_negative:
                        data_check_test.loc[(data_check_test["corr_columns_data_bucket"] == key),"Checks"] = True
                        self.check_alert_print(f"Corr in variable ( {key} )",CHECK_ALERT_S)
                    else:
                        self.check_alert_print(f"Corr in variable ( {key} )",CHECK_ALERT_N)
                else:
                    self.check_alert_print(f"Corr in variable ( {key} )",CHECK_ALERT_N)

        if display_check:
            display(data_check_test.style.applymap(lambda x: "background-color: green" if x else "background-color: red",subset=["Checks"]))


    def check_report_columns(self,tag,dropna=False):
        if tag:
            if len(tag) > 0:
                data_local = self.data_local_historic

                list_columns_bucket = self.data_bucket.columns
                list_columns_local  = data_local.columns

                check_compare_columns = True
                if tag not in list_columns_bucket:
                    self.check_alert_print(f"Column ( {tag} ) Not exist in Bucket Data",CHECK_ALERT_N)
                    check_compare_columns = False
                elif tag not in list_columns_local:
                    self.check_alert_print(f"Column ( {tag} ) Not exist in Local Data",CHECK_ALERT_N)
                    check_compare_columns = False
                else:
                    self.check_alert_print(f"Column ( {tag} ) exist in Local and Bucket Data",CHECK_ALERT_S)
                
                if check_compare_columns:
                    column_check = tag
                    merged_df = pd.merge(data_local[f"{column_check}"], self.data_bucket[f"{column_check}"], left_index=True, right_index=True, suffixes=('_local', '_bucket'))
                    different_rows = merged_df[merged_df[f'{column_check}_local'] != merged_df[f'{column_check}_bucket']]
                    if dropna:
                        different_rows = different_rows.dropna(how="all",subset=[f'{column_check}_local',f'{column_check}_bucket'])


                    get_df_negative = self.get_df_negative(column_check,dropna_check=dropna)


                    row = different_rows.shape[0]
                    if row <= 0 and get_df_negative:
                        self.check_alert_print(f"Corr in variable ( {tag} )",CHECK_ALERT_S)
                    else:
                        self.check_alert_print(f"Corr in variable ( {tag} )",CHECK_ALERT_N)

                    display(HTML("<br>"))

                    if get_df_negative:
                        display(different_rows)
                    else:
                        different_rows = merged_df
                        if different_rows[f"{column_check}_local"].shape[0] > 0 and different_rows[f"{column_check}_bucket"].shape[0] > 0:
                            if different_rows[f"{column_check}_local"].dtype in ['int64', 'float64'] and different_rows[f"{column_check}_bucket"].dtype in ['int64', 'float64']:
                                if (different_rows[f"{column_check}_local"] < 0).any():
                                    display(different_rows[different_rows[f"{column_check}_local"] < 0])
                                else:
                                    if(different_rows[f"{column_check}_bucket"] < 0).any():
                                        display(different_rows[different_rows[f"{column_check}_bucket"] < 0])

    def get_check_data_historic(self,tag,data,dropna):
        if tag:
            #self.clear()

            (data_bucket,data_local) = data.get_data_compare(tag)

            self.data_bucket = data_bucket
            self.data_local = data_local
            data_bucket_shape = data_bucket.shape[0]
            self.data_local_historic = self.data_local.iloc[:data_bucket_shape]

            self.check_alert_print(f"The analysis process has begun. lengh_analysis: {self.data_local_historic.shape[0]}",CHECK_ALERT_G)
            
            self.check_lenght_historic()
            self.check_count_columns()
            self.check_report_all(dropna_check=dropna)
    
    def start_check_historic(self,data,tag=""):
        if len(tag) <= 0:
            self.is_widgets = True
            dropdown_w = widgets.Dropdown(
                options=self.list_tags,
                value=None,
                description='Data_Sets: ',
                disabled=False,
            )

            dropdown_columns = widgets.Dropdown(
                description='Columns: ',
                value=None,
                disabled=False,
            )

            check_nan = widgets.Checkbox(
                    value=False,
                    description='Delete NaN',
                    disabled=False,
                    indent=False
            )


            display(HTML(f"<p style='text-align:left; font-size:35px'><strong>Compare Historical Data.</strong></p>"))

            dropdown_w.layout = widgets.Layout(flex='2 1 10%',)
            dropdown_columns.layout = widgets.Layout(flex='2 1 0%',)
            check_nan.layout = widgets.Layout(flex='0 1 2%',padding="0 0 0 20px")

            box = HBox(children=[dropdown_w,dropdown_columns,check_nan])

            out = widgets.interactive_output(self.get_check_data_historic,{"tag" : dropdown_w, "data":widgets.fixed(data), "dropna": check_nan})
            out2 = widgets.interactive_output(self.check_report_columns, {"tag" : dropdown_columns, "dropna": check_nan})

            out.layout = widgets.Layout(justify_content='flex-start', flex='2',height='350px', overflow='scroll', padding='0 0 0 30px')
            out2.layout = widgets.Layout(justify_content='flex-end', flex='2',height='350px', overflow='scroll', padding='0 0 0 30px')

            box2 = HBox(children=[out,out2])

            def update_dropdown_columns_options(change):
                if change['type'] == 'change' and change['name'] == 'value':
                    columns_bucket = set(self.data_bucket.columns)
                    columns_local_historic = set(self.data_local_historic.columns)

                    dropdown_columns.options = list(columns_bucket.union(columns_local_historic))
                    dropdown_columns.disabled = False

            dropdown_w.observe(update_dropdown_columns_options)

            display(box,box2)

        else:
            self.is_widgets = False
            self.get_check_data_historic(tag,data)
    
    def check_report_new(self,display_check=False):
        data_local = self.data_local_new

        list_columns_bucket = self.data_bucket.columns
        list_columns_local  = data_local.columns
        
        check_new_columns = []
        check_types = []
        check_nan = []
        check_negative = []

        if data_local.shape[0] > 0:
            list_columns = list(list_columns_bucket.union(list_columns_local))
            
            for i in list_columns:
                if i in list_columns_bucket and i in list_columns_local:
                    check_new_columns.append(True)

                    check_types.append(self.data_bucket[i].dtypes == data_local[i].dtypes)
                else:
                    check_new_columns.append(False)
                    check_types.append(False)

                if i in list_columns_local:
                    check_nan.append(data_local[i].isna().sum())

                    if data_local[i].dtype in ['int64', 'float64']:
                        check_negative.append((data_local[i] < 0).any())
                    else:
                        check_negative.append(False)
                else:
                    check_nan.append(0)
                    check_negative.append(False)
            
            df_new = pd.DataFrame([list_columns,check_new_columns,check_types,check_nan,check_negative]).T

            df_new.rename(columns={0:"Columns",1:"Columns_Equals",2:"DTypes_Columns",3:"NaN_Count",4:"Negative_V"},inplace=True)

            df_new["NaN_Count"] = df_new["NaN_Count"].astype(int)            

            style = df_new.style.applymap(lambda x: "background-color: green" if x else "background-color: red",subset=["Columns_Equals","DTypes_Columns"])
            style = style.applymap(lambda x: "background-color: red" if x != 0 else "background-color: green",subset=["NaN_Count"])
            style = style.applymap(lambda x: "background-color: red" if x else "background-color: green",subset=["Negative_V"])

            display(style)

    def check_report_columns_new(self,tag,dropna=False):
        if tag:
            if len(tag) > 0:
                data_local = self.data_local_new

                list_columns_bucket = self.data_bucket.columns
                list_columns_local  = data_local.columns

           
                if tag not in list_columns_local:
                    self.check_alert_print(f"Column ( {tag} ) Not exist in Local Data",CHECK_ALERT_N)
                elif tag not in list_columns_bucket:
                    self.check_alert_print(f"Column ( {tag} ) Not exist in Bucket Data",CHECK_ALERT_N)
                else:
                    self.check_alert_print(f"Column ( {tag} ) exist in Local and Bucket Data",CHECK_ALERT_S)

                if tag in list_columns_local:
                    if data_local[tag].shape[0] > 0:
                        column_check = tag
                        display(HTML("<br>"))

                        data_values_unique = data_local[column_check].unique().copy()
                        #data_values_unique.rename(columns={0:"Values_Uniques"},inplace=True)

                        display(pd.DataFrame(data_values_unique, columns=["Values_Uniques"]))
                    
    def get_check_data_new(self,tag,data,dropna):
        if tag:
            #self.clear()


            (data_bucket,data_local) = data.get_data_compare(tag)
            self.data_bucket = data_bucket
            data_bucket_shape = data_bucket.shape[0]
            self.data_local_new = data_local.iloc[data_bucket_shape:]

            self.check_alert_print(f"The analysis process has begun. lengh_analysis: {self.data_local_new.shape[0]}",CHECK_ALERT_G)
            self.check_report_new()
    
    def start_check_data_new(self,data,tag=""):
        if len(tag) <= 0:
            self.is_widgets = True
            dropdown_w = widgets.Dropdown(
                options=self.list_tags,
                value=None,
                description='Data_Sets: ',
                disabled=False,
            )

            dropdown_columns = widgets.Dropdown(
                description='Columns: ',
                value=None,
                disabled=False,
            )

            check_nan = widgets.Checkbox(
                    value=False,
                    description='Delete NaN',
                    disabled=True,
                    indent=False
            )

            display(HTML(f"<p style='text-align:left; font-size:35px'><strong>Compare New Data.</strong></p>"))

            dropdown_w.layout = widgets.Layout(flex='2 1 10%',)
            dropdown_columns.layout = widgets.Layout(flex='2 2 0%',)

            check_nan.layout = widgets.Layout(flex='0 1 2%',padding="0 0 0 20px")

            box = HBox(children=[dropdown_w,dropdown_columns])

            out = widgets.interactive_output(self.get_check_data_new,{"tag" : dropdown_w, "data":widgets.fixed(data), "dropna": check_nan})
            out2 = widgets.interactive_output(self.check_report_columns_new, {"tag" : dropdown_columns, "dropna": check_nan})

            out.layout = widgets.Layout(justify_content='flex-start', flex='3',height='400px', overflow='scroll', padding='0 0 0 30px')
            out2.layout = widgets.Layout(justify_content='flex-end', flex='2',height='400px', overflow='scroll', padding='0 0 0 30px')

            box2 = HBox(children=[out,out2])

            def update_dropdown_columns_options_new(change):
                if change['type'] == 'change' and change['name'] == 'value':
                    columns_bucket = set(self.data_bucket.columns)
                    columns_local_new = set(self.data_local_new.columns)

                    dropdown_columns.options = list(columns_bucket.union(columns_local_new))
                    dropdown_columns.disabled = False

            dropdown_w.observe(update_dropdown_columns_options_new)

            display(box,box2)

        else:
            self.is_widgets = False
            self.get_check_data_new(tag,data)

       
    