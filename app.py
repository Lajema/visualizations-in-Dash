import dash

from dash import html,dcc

import pandas as pd
import gspread
import plotly_express as px
import warnings
from termcolor import colored
warnings.filterwarnings("ignore")
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("../credentials.json", scope)  # ‘client_secret.json’, scope)
gc = gspread.authorize(creds)
wks = gc.open_by_url( "https://docs.google.com/spreadsheets/d/1hOMGLSsvE_V3vkY_7Hal85ROvKLjZM2VX2X8j9hZlHo/edit#gid=0")
# -----------------------------------------------------------------------------------------------------------
def reader(sheet):
    """Given a sheet name, this function returns the data contained therein"""
    sheetnme = wks.worksheet(sheet)
    record = pd.DataFrame(sheetnme.get_all_records())
    print( colored(f"The read data:{sheet} has shape ----------->{record.shape}", "green"))
    record = record.rename(columns={"Firm ID": "firm_id"})
    try:
        record = record.fillna(0)
        record = record.drop(["Unnamed: 0"], 1)
        record = record.drop(["check"], 1)
    except:
        pass
    return record
# read the data
data = reader("Data")

q10 = data[data["Question_code"]=="SFD-GND-010"]
y = q10.groupby(["Country of Residence","value"]).size().reset_index().rename(columns = {0:'n'})
pie = px.pie(y,names = "value",values = "n",facet_col = "Country of Residence",title = q10["variable"][0])

q20 = data[data["Question_code"]=="SFD-GND-020"]
y = q20.groupby(["Country of Residence","value"]).size().reset_index().rename(columns = {0:'n'})
pie2 = px.pie(y,names = "value",values = "n",facet_col = "Country of Residence")


app = dash.Dash(__name__)

app.layout = html.Div(
children = [
    html.Div(dcc.Graph(id = "001",figure = pie),style = {'width':'900px','height':'700px','display':'inline-block'}),
    html.Div(dcc.Graph(id = "002",figure = pie2),style = {'width':'900px','height':'700px','display':'inline-block'})
]
)






if __name__ == "__main__":
    app.run_server(debug = True)
    