import numpy as np
dtypes_explicit = {
    'subject_id': str,
    'IvSocSec': np.int64,
    'PdPeriod': np.int64,
    'PdName': str,
    'DaDay': np.int64,
    'DaDate': str, #will combine this with MaTime to make a timestamp
    'MaMeal': np.int64,
    'MaName': str,
    'MaTime': str, #will combine this with MaDate to make a timestamp
    'MaType': np.float64,
    'CoRow': np.int64,
    'Code': str,
    'CoIcAdId1': np.int64,
    'CoIcAdId2': np.int64,
    'Name': str,
    'MainGroup': np.int64,
    'MgName': str,
    'SubGroup': np.int64,
    'SgName': np.int64,
    'CoFormel': str, #some rows have quotes around decimal values, mixed content fails to parse in read_csv with delimiter and dtype options
}