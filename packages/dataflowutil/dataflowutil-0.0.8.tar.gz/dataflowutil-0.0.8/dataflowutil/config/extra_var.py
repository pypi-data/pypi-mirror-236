import os

CONNECTION_VAR = 1 # 0 = PRODUCTION / 1 = TESTING
ACTIVATE_DATA_LOCAL = 0 # 0 Off / 1 ON

DIRNAME_CREDENTIALS = "credentials"
DIRNAME_UPLOAD_BUCKET  = "upload"
CONFIG_NAME_PRODUCTION = "connection_production.ini"
CONFIG_NAME_TEST = "connection_testing.ini"

PATH_CREDENTIALS = os.path.join(os.getcwd(), f"{DIRNAME_CREDENTIALS}")
PATH_UPLOAD_BUCKET = os.path.join(os.getcwd(), f"{DIRNAME_UPLOAD_BUCKET}")


NAME_SHEET = "CONFIG_DB"

def convert_sheet_url(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/e/{sheet_id}/pub?output=csv"
    return url

#name - format
type_archives = {
    "xlsx"  : "xlsx",
    "csv"   : "csv",
    "auto"  : "xlsx|csv"
}

STATUS_UPDATE = {
    "NO_UPDATE" : 0,
    "UPDATE" : 1,
    "NO_LOAD" : 2,
}
