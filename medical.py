import pandas as pd
def handle():
    data=pd.io.stata.read_stata('unhandle_data/Health_History.dta')
    data.to_csv('data/Health_History.csv')
handle()