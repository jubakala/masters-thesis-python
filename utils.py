from scipy.stats import poisson
import pandas as pd
import os
import operator

def update_betting_score(counts, is_correct, probabilities):
    bet = get_bet(probabilities)
    label = "incorrect"

    if is_correct:
        label = "correct"

    # The + "s" is to pluralize the bet name.
    counts[bet + "s"][label] += 1 

    return counts


def get_bet(probabilities):
    """
    Find the biggest probability and return it's string key.
    If all the probabilities are equal, the bet is home win.
    """
    return max(probabilities.items(), key=operator.itemgetter(1))[0]


# Check if the prediction based on poisson probabilities was correct, based on the actual score.
def check_result(home_goals, away_goals, probabilities):
    bet = get_bet(probabilities)
    is_correct = False

    if home_goals > away_goals and bet is "home_win": # Home win.
        is_correct = True
    elif home_goals < away_goals and bet is "away_win": # Away win.
        is_correct = True
    elif home_goals == away_goals and bet is "draw": # Draw.
        is_correct = True
    
    return is_correct


# Calculate poisson distribution for each game score, and then calculate probabilities for each three game outcomes, home or away win, or draw.
def get_outcome_probabilities(home_mean, away_mean):
    home_win_probability = 0.0
    draw_probability = 0.0
    away_win_probability = 0.0

    for ii in range(0, 11): # Home goals, 0-10.
        for jj in range(0, 11): # Away goals, 0-10.
            home_poisson = poisson.pmf(ii, home_mean)
            away_poisson = poisson.pmf(jj, away_mean)

            result_probability = home_poisson * away_poisson # The game result is ii - jj.
                
            if ii > jj: # Home win.
                home_win_probability += result_probability
            elif ii < jj: # Away win.
                away_win_probability += result_probability
            elif jj == ii: # Draw.
                draw_probability += result_probability

    return round(home_win_probability, 3), round(draw_probability, 3), round(away_win_probability, 3)


# Used for testing purposes only.
def get_season_games(season, games):
    return games.loc[games.season == season]


def get_team_means(games, home_away, team_id, game_amount):
    team_goals = games.loc[games[home_away + '_team'] == team_id][home_away + '_goals']
    # Calculate scored goals mean for home games for the team in question.
    means = pd.DataFrame(team_goals.rolling(game_amount).mean().round(decimals=2))        
        # Rename the column home_goals to home_mean.
    means.rename(columns={home_away + '_goals': home_away + '_mean'}, inplace=True)
    """
        Shift mean values one place down. Currently, when calculating the scored goals mean, 
        also the goals which result is to be predicted is calculted to the mean. By shifting all the mean values one place "down", 
        we get the correct mean, which doesn't include the goals scored "in the future", ie. in the game in question.
    """
    means[home_away + '_mean'] = means[home_away + '_mean'].shift()
    # Replace NaNs with -1.
    means[home_away + '_mean'] = means[home_away + '_mean'].fillna(-1)

    return means

"""
Calculate scored goals means for games of a chosen season. All the games, not just the chosen season's games, 
are fed to this function in order to avoid SettingWithCopyWarning pandas error/warning.
"""
def season_means(season, games):
    game_amount = 3
    team_ids = games.home_team.unique()

    for team_id in team_ids:
        # Update the games dataframe with the home mean values of this team.
        home_means = get_team_means(get_season_games(season, games), "home", team_id, game_amount)  
        games.update(home_means)

        # Update the games dataframe with the away mean values of this team.
        away_means = get_team_means(get_season_games(season, games), "away", team_id, game_amount)
        games.update(away_means)

    return games


# Gets the all available season names, ie. 2005-06 etc.
def get_seasons(games):
    return sorted(games.season.unique())


# Does some preprocessing tasks for the dataframe containing the game data.
def preprocess_games(games):
    # Initialize new columns home and away mean with zeros.
    games['home_mean'] = 0.0
    games['away_mean'] = 0.0

    # Drop unnecessary columns.
    games = games.drop("id", axis=1)
    games = games.drop("checked", axis=1)

    # Sort games by date.
    games = games.sort_values("match_date", axis=0, ascending=True)

    return games


# Fetches all the games from the csv-file.
def get_games(filename):    
    if not os.path.isfile(filename):
        return {"games": None, "msg": "File not found"}
    else:
        games = pd.read_csv(filename)

        return {"games": games, "msg": ""}