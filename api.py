import pandas as pd
from pathlib import Path


def load_data():
    # Define the path to the CSV file
    csv_path = Path(__file__).parent / "train" / "nfl_data.csv"

    # Load the data into a pandas DataFrame
    data = pd.read_csv(csv_path)
    return data


def process_data(data):
    # Placeholder for data processing logic
    return data


class NFLDataAPI:
    def __init__(self):
        self.data = process_data(load_data())

    def get_team_stats(self, team_name):
        team_data = self.data[self.data['Team'] == team_name]
        if not team_data.empty:
            return team_data.to_dict(orient='records')[0]
        else:
            return None