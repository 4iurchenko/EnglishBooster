import gspread

class EngGoogleSheet():
    def __init__(self, sh_name, wks_name):
        self.sa = gspread.service_account(filename="secret_client.json")
        self.sh = self.sa.open(sh_name)
        self.wks = self.sh.worksheet(wks_name)

    def getFields(self, r_from = 3, r_to = 999999):
        data = self.wks.get_all_values()[r_from:r_to]
        return data

"""
# Example of usage
data = EngGoogleSheet(sh_name = "To-do list", wks_name = "tifwords3000")
d_list = data.getFields()
d_list_filt = [x for x in d_list if (x[0] != "FALSE" and (x[1] != "" or x[2] != "" or x[3] != ""))]
print(d_list_filt)
"""





