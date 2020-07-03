from utils import *
from ui import *

# Simulate games of a single season.
def simulate(season, games):
    game_counter = 0
    # Stats about simulated games and bets. 
    counts = { "home_wins": { "correct": 0, "incorrect": 0 }, "away_wins": { "correct": 0, "incorrect": 0 }, "draws": { "correct": 0, "incorrect": 0 }}
    season_games = games[games.season == season]

    for index, game in season_games.iterrows():
        game_counter += 1

        # Include only games where scored goals mean of last three games were available.
        if game.home_mean > -1 and game.away_mean > -1:
            # Get the probabilities for game outcomes based on scored goals mean Poisson distribution.
            home_win_prob, draw_prob, away_win_prob = get_outcome_probabilities(game.home_mean, game.away_mean)
            probabilities = {"home_win": home_win_prob, "draw": draw_prob, "away_win": away_win_prob}
            # Check if the prediction based on poisson probabilitie was correct compared to the actual result of the game.
            correct = check_result(game.home_goals, game.away_goals, probabilities)
            # Update bets counts.
            counts = update_betting_score(counts, correct, probabilities)            
            
            # Print simulation progress.
            if game_counter % 50 == 0:
                print('{:4d}'.format(game_counter), "games simulated.") 

    return counts


def main():
    """
    Get games from csv-file as a dictionary {"games": games, "msg": ""}, where games is pandas dataframe, 
    and msg is possibly an empty message string.
    """
    data = get_games("games.csv")

    # If games were not downloaded correctly from csv-file. 
    if len(data['msg']) > 0:
        print(data['msg'])
        return    
    
    games = data['games']
    # Remove unnecessary columns and add new ones and initialize them. Also returns the dataframe sorted by match date, in ascending order.
    games = preprocess_games(games)
    # Get the list of available seasons.
    seasons = get_seasons(games)

    # Let the user to choose the season to be simulated.
    choice = print_seasons(seasons)

    while choice.isnumeric():
        if int(choice) > 0 and int(choice) < len(seasons) + 1:
            # Get the season user chose.
            season = seasons[int(choice) - 1]
            # season_games_with_means = season_means(get_season_games(season, games))
            season_games_with_means = season_means(season, games)
            # Simulate the season.
            counts = simulate(season, season_games_with_means)
            print_simulation_results(counts)

            choice = print_seasons(seasons)
        else:
            print("Incorrect season chosen, please try again!")
            choice = print_seasons(seasons)

if __name__ == "__main__":
    main()