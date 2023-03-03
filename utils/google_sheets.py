import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"
         ]

cred = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(cred)


def upload_data(data, sheet):
    try:
        spd = client.open(sheet)
        spd.values_clear('A1:Z100')
    except Exception as e:
        spd = client.create(sheet)
    spd.sheet1.append_row(["Title", "Server Name", "Stock", "Total Price",
                           "Avg. Price", "Updated At"])
    spd.share(value=None, role='writer', perm_type='anyone')
    spd.sheet1.append_rows(data)
    return spd.url


def export(sheet, file):
    try:
        sht = client.open(sheet).sheet1
    except Exception as e:
        print(e)
        print(e.args)
        return False
    dt = sht.get_all_values()
    dtb = [['"'+g.replace('"', '""')+'"' if ',' in g else g for g in m]
           for m in dt]
    with open(file, 'wb+') as fl:
        fl.write('\n'.join([','.join(it) for it in dtb]).encode())
    return True
