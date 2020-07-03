def print_seasons(seasons):
    print("")

    for index, s in enumerate(seasons):
        print(index + 1, "-", s)

    print("\nq - Quit\n")

    choice = input("Choose season to be simulated: ")

    return choice


def print_simulation_results(counts):
    print("\n")
    print("+" * 100)
    print("Bets (correct / incorrect):")
    print(" - Home wins bets:", counts['home_wins']['correct'], "/", counts['home_wins']['incorrect'])
    print(" - Draws bets:", counts['draws']['correct'], "/", counts['draws']['incorrect'])
    print(" - Away win bets:", counts['away_wins']['correct'], "/", counts['away_wins']['incorrect'])
    print(" - Total:", counts['home_wins']['correct'] + counts['draws']['correct'] + counts['away_wins']['correct'], "/", counts['home_wins']['incorrect'] + counts['draws']['incorrect'] + counts['away_wins']['incorrect'])
    print("+" * 100)
    print("\n")