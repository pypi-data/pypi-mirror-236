import pandas as pd
import warnings
import Levenshtein
from IPython.display import display

def jaccard_index(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return (intersection / union)

def corr_compare_number(value1, value2, tolerance=1e-6):
    return abs(value1 - value2) < tolerance

def check_types_columns(data_bucket,data_local):
    var_levenshtein = 1 - Levenshtein.distance(data_bucket.dtypes.values, data_local.dtypes.values) / max(len(data_bucket.dtypes.values), len(data_local.dtypes.values))
    print(f"** Error Types Columns: {var_levenshtein}")
    print("")
    check_types = pd.DataFrame({"columns_data_bucket":tuple(data_bucket.dtypes.values),"columns_data_local":tuple(data_local.dtypes.values)})
    print(check_types)

def start_report(data_bucket,data_local):

    data_bucket_shape = data_bucket.shape[0]
    data_local_shape = data_local.shape[0]

    if data_local_shape < data_bucket_shape:
        print("Error in lenght data , len data_bucket < data_local")
        return

    data_local = data_local.iloc[:data_bucket_shape]

    count = 1 - abs(len(data_bucket.columns) - len(data_local.columns)) / max(len(data_bucket.columns) , len(data_local.columns))

    columns_check = {
        "count_columns_data_bucket" : [len(data_bucket.columns)],
        "count_columns_data_local" : [len(data_local.columns)],
        "error" : [count]
    }

    display(pd.DataFrame(columns_check))
    
    list_columns_bucket = data_bucket.columns
    list_columns_local = data_local.columns
    
    data_check_test = pd.DataFrame([list_columns_bucket,list_columns_local]).T
    data_check_test.rename(columns = {0:"corr_columns_data_bucket",1:"corr_columns_data_local"}, inplace = True)
    data_check_test["Checks"] = False

    for key,value in dict(data_bucket.eq(data_local).all()).items():
        if value:
            data_check_test.loc[(data_check_test["corr_columns_data_bucket"] == key),"Checks"] = True
            
    display(data_check_test.style.applymap(lambda x: "background-color: green" if x else "background-color: red",subset=["Checks"]))

def dft_rows(data_bucket,data_local,column_check,dropna = False):
    if column_check not in data_bucket.columns:
        print(f"{column_check} no exist in data_bucket.")
    
    if column_check not in data_local.columns:
        print(f"{column_check} no exist in data_local.")

    merged_df = pd.merge(data_local[f"{column_check}"], data_bucket[f"{column_check}"], left_index=True, right_index=True, suffixes=('_local', '_bucket'))
    different_rows = merged_df[merged_df[f'{column_check}_local'] != merged_df[f'{column_check}_bucket']]
    if dropna:
        different_rows = different_rows.dropna(how="all",subset=[f'{column_check}_local',f'{column_check}_bucket'])
    return different_rows


def check_porcent_value_numeric(key,data_bucket,data_local):
    total = data_bucket[key].ne(data_local[key]).count()
    try:
        check_true = data_bucket[key].ne(data_local[key]).value_counts()[True]
        return f"{100 - abs(check_true / total)}"
    except:
        return f"{100}"


def corr(data_bucket,data_local):
    warnings.simplefilter(action='ignore', category=FutureWarning)        

    check_columns_data_bucket = data_bucket.select_dtypes(include=['object','string'])

    if len(check_columns_data_bucket.columns) > 0:

        print("")
        print("************************************")
        print("*** Corr DTypes Objects/Strings ***")
        print("************************************")
        print("")

        for a in check_columns_data_bucket.columns:
            data_bucket_corr = data_bucket[[a]].astype("category")[a].cat.codes
            data_local_corr = data_local[[a]].astype("category")[a].cat.codes

            var_jaccard = jaccard_index(set(data_bucket_corr), set(data_local_corr))
            var_levenshtein = 1 - Levenshtein.distance(data_bucket[a], data_local[a]) / max(len(data_bucket[a]), len(data_local[a]))

            print(f"{a.ljust(16)} {var_jaccard} - {var_levenshtein}")

    print("")
    print("************************************")
    print("******* Corr DTypes Numbers *******")
    print("************************************")
    print("")
    correlation = data_bucket.corrwith(data_local,method=corr_compare_number)
    for a in correlation.keys():
        value =  sum(correlation[a]) / len(correlation[a])
        print(f"{a.ljust(16)} {value} - {check_porcent_value_numeric(a,data_bucket,data_local)}")
    #return correlation

