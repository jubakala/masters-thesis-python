from unittest import TestCase
from utils import *

class TestFunctions(TestCase):
    # Getting the games data from csv-file.
    def test_get_games_with_incorrect_filename(self):
        incorrect_filename = "game.csv"
        expected_result_message = "File not found"
        data = get_games(incorrect_filename)

        self.assertEqual(expected_result_message, data['msg'])

    def test_get_games_with_correct_filename(self):
        filename = "games.csv"
        expected_result_message = ""
        data = get_games(filename)

        self.assertEqual(expected_result_message, data['msg'])

    def test_check_that_games_is_not_none(self):
        filename = "games.csv"
        data = get_games(filename)

        self.assertIsNotNone(data['games'])

    def test_check_that_games_were_fetched(self):
        filename = "games.csv"
        data = get_games(filename)

        self.assertGreater(data['games'].shape[0], 0)

    # Preprocessing the games dataframe.
    def test_home_mean_column_exists(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        self.assertIn("home_mean", games)

    def test_home_mean_data_is_filled_with_zeros(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)
        column_data_sum = games['home_mean'].sum()

        self.assertEqual(column_data_sum, 0)

    def test_away_mean_column_exists(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        self.assertIn("away_mean", games)

    def test_away_mean_data_is_filled_with_zeros(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)
        column_data_sum = games['away_mean'].sum()

        self.assertEqual(column_data_sum, 0)        

    def test_checked_column_is_dropped(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        self.assertNotIn("checked", games)

    def test_id_column_is_dropped(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        self.assertNotIn("id", games)        

    def test_rows_are_sorted_by_match_date_asc(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        game_0 = pd.to_datetime(games.iloc[0]['match_date'])
        game_20 = pd.to_datetime(games.iloc[20]['match_date'])
        game_100 = pd.to_datetime(games.iloc[100]['match_date'])

        self.assertTrue(game_0 < game_20 and game_0 < game_100 and game_20 < game_100)

    # Test that season's list is correct.
    def test_get_seasons_list(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)
        seasons = get_seasons(games)

        self.assertGreater(len(seasons), 0)

    def test_check_that_seasons_are_in_asc_order(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        seasons = get_seasons(games)
        first = seasons[0]
        third = seasons[2]
        last = seasons[-1]

        self.assertTrue(first < third and first < last and third < last)

    # Season games.
    def test_get_season_games(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        seasons = get_seasons(games)
        season = seasons[0]        
        season_games = get_season_games(season, games)

        first_game = season_games.iloc[0]
        last_game = season_games.iloc[season_games.shape[0] - 1]
        season_start_year = season[0:4]
        season_end_year = season[5:10]

        self.assertTrue(first_game['match_date'][0:4] == season_start_year and last_game['match_date'][0:4] == season_end_year)

    # Team scored goals mean values.
    def test_get_team_means(self):
        data = get_games("games.csv")
        games = data['games']
        games = preprocess_games(games)

        seasons = get_seasons(games)
        season = seasons[0]        
        season_games = get_season_games(season, games)

        team_means = get_team_means(season_games, "home", 25, 3)
        first_mean = 2.00 # First mean means the mean of scored goals in previous three games.

        self.assertEqual(team_means.iloc[3]['home_mean'], first_mean)

    # Game outcome probabilities based on poisson distribution.
    def test_get_outcome_probabilities(self):
        home_mean = 2.0
        away_mean = 3.0

        # Calculated with: https://www.winnergambling.com/sports-betting-bingo/correct-score-betting-alculator/
        expected_home_win_probability = 0.247
        expected_away_win_probability = 0.585
        expected_draw_probability = 0.168

        home_win_prob, draw_prob, away_win_prob = get_outcome_probabilities(home_mean, away_mean)

        self.assertTrue(expected_home_win_probability == home_win_prob and expected_draw_probability == draw_prob and expected_away_win_probability == away_win_prob)

    def test_get_biggest_probability_label_home_win(self):
        probabilities = {"home_win": 0.5, "draw": 0.2, "away_win": 0.3}
        expected = "home_win"
        bet = get_bet(probabilities)

        self.assertEqual(expected, bet)

    # When the biggest value is not first in the dict.
    def test_get_biggest_probability_label_away_win(self):
        probabilities = {"home_win": 0.2, "draw": 0.2, "away_win": 0.6}
        expected = "away_win"
        bet = get_bet(probabilities)

        self.assertEqual(expected, bet)

    # When all the probabilities are equal.
    def test_get_biggest_probability_when_probs_are_equal(self):
        probabilities = {"home_win": 0.333, "draw": 0.333, "away_win": 0.333}
        expected = "home_win"
        bet = get_bet(probabilities)

        self.assertEqual(expected, bet)                

    # Check, if the prediction was correct, compared to the real outcome of the game.
    def test_check_if_prediction_was_correct_home_win(self):
        probabilities = { "home_win": 0.600, "draw": 0.150, "away_win": 0.250 }
        is_correct = check_result(4, 1, probabilities)

        self.assertTrue(is_correct)

    def test_check_if_prediction_was_correct_away_win(self):
        probabilities = { "home_win": 0.250, "draw": 0.150, "away_win": 0.600 }
        is_correct = check_result(3, 5, probabilities)

        self.assertTrue(is_correct)        

    def test_check_if_prediction_was_correct_draw(self):
        probabilities = { "home_win": 0.200, "draw": 0.550, "away_win": 0.250 }
        is_correct = check_result(2, 2, probabilities)

        self.assertTrue(is_correct)

    # Update bets counts.
    def test_bets_counter_correct_home_win(self):
        counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
        probs = {"home_win": 0.6, "draw": 0.1, "away_win": 0.3} 
        counts = update_betting_score(counts, True, probs)

        self.assertTrue(counts['home_wins']['correct'] == 1)

    def test_bets_counter_correct_away_win(self):
        counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
        probs = {"home_win": 0.4, "draw": 0.1, "away_win": 0.5} 
        counts = update_betting_score(counts, True, probs)

        self.assertTrue(counts['away_wins']['correct'] == 1)

    def test_bets_counter_correct_draw(self):
        counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
        probs = {"home_win": 0.4, "draw": 0.5, "away_win": 0.1}
        counts = update_betting_score(counts, True, probs)

        self.assertTrue(counts['draws']['correct'])

    def test_bets_counter_incorrect_home_win(self):
        counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
        probs = {"home_win": 0.6, "draw": 0.3, "away_win": 0.1} 
        counts = update_betting_score(counts, False, probs)

        self.assertTrue(counts['home_wins']['incorrect'] == 1)

    def test_bets_counter_incorrect_away_win(self):
        counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
        probs = {"home_win": 0.2, "draw": 0.1, "away_win": 0.7}
        counts = update_betting_score(counts, False, probs)

        self.assertTrue(counts['away_wins']['incorrect'] == 1)

    def test_bets_counter_incorrect_draw(self):
        counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
        probs = {"home_win": 0.2, "draw": 0.5, "away_win": 0.3} 
        counts = update_betting_score(counts, False, probs)

        self.assertTrue(counts['draws']['incorrect'] == 1)        