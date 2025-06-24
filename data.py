import pandas as pd

PATH = "data/"

# Load well data from json file
def load_wells():
    return pd.read_json(PATH + "wells.json", orient="records")

def load_data():
    data = pd.read_csv(PATH + "data.csv")
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    return data