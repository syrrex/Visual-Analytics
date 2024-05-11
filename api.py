import pandas as pd
from pathlib import Path


class NFLDataAPI:
    def __init__(self):
        """
        Constructor for MyClass.

        Args:
            instance_variable1: Description of the first instance variable.
            instance_variable2: Description of the second instance variable.

        """
        print("Initializing NFLDataAPI...")
        self.df_weeks, self.df_games, self.df_plays = self.process_data()
        print("Done with loading the data")

    def load_week_data(self, week):
        file_path = f'data/week{week}.csv'
        df_week = pd.read_csv(file_path)
        df_week = df_week.drop(columns=['s', 'a', 'dis', 'o', 'nflId', 'dir', 'event', 'route'])
        return df_week

    def load_plays_data(self):
        file_path = 'data/plays.csv'
        df_plays = pd.read_csv(file_path)
        df_plays = df_plays.drop(
            columns=['yardlineSide', 'defendersInTheBox', 'isDefensivePI', 'epa', 'numberOfPassRushers',
                     'playType', 'typeDropback', 'penaltyCodes', 'penaltyJerseyNumbers', 'offensePlayResult'])
        print("Done with loading play data")
        return df_plays

    def load_games_data(self):
        file_path = 'data/games.csv'
        df_games = pd.read_csv(file_path)
        df_games = df_games.drop(columns='gameTimeEastern')
        print("Done loading game data")
        return df_games

    def load_all_weeks(self):
        all_weeks = []
        for week in range(1, 18):
            week_df = self.load_week_data(week)
            all_weeks.append(week_df)
        all_weeks_df = pd.concat(all_weeks, ignore_index=True)
        print("Done loading week data")
        return all_weeks_df

    def process_data(self):
        all_weeks_df = self.load_all_weeks()
        missing_values = all_weeks_df.isna().sum()
        # TODO: when we want to print values in common, check if it is available we have a few missing values but we can
        #  live with that, important values like coordinates and time stamps are complete
        #  Misiing Value imputation makes no sence
        print(f"\nAll Weeks Combined - Missing values:\n{missing_values[missing_values > 0]}")
        # Drop duplicates
        all_weeks_df_clean = all_weeks_df.drop_duplicates()

        games_df = self.load_games_data()
        missing_values = games_df.isna().sum()
        print(f"\nGames - Missing values:\n{missing_values[missing_values > 0]}")
        # Drop duplicates
        games_df_clean = games_df.drop_duplicates()

        plays_df = self.load_plays_data()
        missing_values = plays_df.isna().sum()
        print(f"\nPlays - Missing values:\n{missing_values[missing_values > 0]}")
        # Drop duplicates
        plays_df_clean = plays_df.drop_duplicates()

        return all_weeks_df_clean, games_df_clean, plays_df_clean

    def get_teams_in_specific_week(self, week):
        """
            This function gives you a list of all teams playing in specific week.

            Args:
                week (int): [1..17]

            Returns:
                return_type: data frame with all teams playing in specific week and the according gameID
        """

        if not 1 <= week <= 17:
            print("Error: Week must be between 1 and 17")
            exit(0)

            # Read the CSV file
        df = self.df_games

        # Filter the DataFrame for the given week
        matchups_in_given_week = df[df['week'] == week][['homeTeamAbbr', 'visitorTeamAbbr', 'gameId']]

        return matchups_in_given_week

    def get_data_given_week_and_matchup(self, week, game_id):
        """
                This function gives you the relevant gama data for a given matchup in a given week

                Args:
                    week (int): [1..17]
                    matchup (pd dataframe): collumns: ['homeTeamAbbr', 'visitorTeamAbbr', 'gameId']

                Returns:
                    dataframe: dataframe with relevant data given a specific week and specific matchup
         """

        if not 1 <= week <= 17:
            print("Error: Week must be between 1 and 17")
            exit(0)

        filtered_df = self.df_weeks[self.df_weeks['gameId'] == game_id]

        return filtered_df


