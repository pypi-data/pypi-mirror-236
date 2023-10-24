#constants
DATASETS = ['TRMM_LIS_FULL','TRMM_LIS_SEASONAL','TRMM_LIS_MONTHLY', 'TRMM_LIS_DIURNAL', 'TRMM_LIS_DAILY',
            'OTD_FULL','OTD_MONTHLY','OTD_DIURNAL','OTD_DAILY', 'ISSLIS', 'NALMA', 'HS3']
BASE_URL = 'https://wug8w3fg42.execute-api.us-west-2.amazonaws.com/development/singleband/' #base url for actual COG images
base_url = "https://s23k5d19rl.execute-api.us-west-2.amazonaws.com/" #base url for fetching dropdown parameters

##################################################################Datasets mapper##############################################################################

#season_data
seasons = {'Spring':'2013_03_01','Summer':'2013_07_01','Autumn':'2013_10_01','Winter':'2013_12_01'}

#month_data
months = {}
for i in range(9):
    months[f'{i+1}'] = f"20130{i+1}"
months['10'] = '201310'
months['11'] = '201311'
months['12'] = '201312'

#Diurnal_data
diurnal = {}
hour = 1
for i in range(9):
    diurnal[f'Hour {hour}'] = f'2013_0{i+1}_01'
    hour+=1
    diurnal[f'Hour {hour}'] = f'2013_0{i+1}_15'
    hour+=1
for i in range(3):
    diurnal[f'Hour {hour}'] = f'2013_{i+10}_01'
    hour+=1
    diurnal[f'Hour {hour}'] = f'2013_{i+10}_15'
    hour+=1

#Daily data
daily = {}
calendar = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
count = 1
day = 0
for x in range(12):
    month = '00'
    if(x+1 <= 9):
        month = f'0{x+1}'
    else:
        month = f'{x+1}'

    for i in range(calendar[x]): 
        if i+1 <= 9:
            daily[f"Day {count}"] = f"2013_{month}_0{i+1}"
        else:
            daily[f"Day {count}"] = f'2013_{month}_{i+1}'
        count+=1