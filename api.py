import pandas as pd
from pathlib import Path


def load_week_data(week):
    file_path = f'data/week{week}.csv'
    df_week = pd.read_csv(file_path)
    df_week = df_week.drop(columns=['s', 'a', 'dis', 'o', 'nflId', 'dir', 'event', 'route'])
    return df_week


def load_plays_data():
    file_path = 'data/plays.csv'
    df_plays = pd.read_csv(file_path)
    df_plays = df_plays.drop(columns=['yardlineSide', 'defendersInTheBox', 'isDefensivePI', 'epa', 'numberOfPassRushers',
                                      'typeDropback', 'penaltyCodes', 'penaltyJerseyNumbers', 'offensePlayResult'])
    return df_plays


def load_games_data():
    file_path = 'data/games.csv'
    df_games = pd.read_csv(file_path)
    df_games = df_games.drop(columns='gameTimeEastern')
    return df_games


def load_all_weeks():
    all_weeks = []
    for week in range(1, 2):
        week_df = load_week_data(week)
        all_weeks.append(week_df)
    all_weeks_df = pd.concat(all_weeks, ignore_index=True)
    return all_weeks_df


def process_data():
    all_weeks_df = load_all_weeks()
    missing_values = all_weeks_df.isna().sum()
    # TODO: when we want to print values in common, check if it is available we have a few missing values but we can
    #  live with that, important values like coordinates and time stamps are complete
    #  Misiing Value imputation makes no sence
    print(f"\nAll Weeks Combined - Missing values:\n{missing_values[missing_values > 0]}")
    # Drop duplicates
    all_weeks_df_clean = all_weeks_df.drop_duplicates()



    games_df = load_games_data()
    missing_values = games_df.isna().sum()
    print(f"\nGames - Missing values:\n{missing_values[missing_values > 0]}")
    # Drop duplicates
    games_df_clean = games_df.drop_duplicates()

    plays_df = load_plays_data()
    missing_values = plays_df.isna().sum()
    print(f"\nPlays - Missing values:\n{missing_values[missing_values > 0]}")
    # Drop duplicates
    plays_df_clean = plays_df.drop_duplicates()

    return all_weeks_df_clean, games_df_clean, plays_df_clean


class NFLDataAPI:
    def __init__(self):
        self.df_weeks, self.df_games, self.df_plays = process_data()
