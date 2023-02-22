import random

from pizza_vs_cats.deck.create_deck import value_str, n_of_wins_str, n_matches_str
from pizza_vs_cats.utils.input_utils import get_yes_no_answer
from pizza_vs_cats.utils.print_utils import clear_screen
from pizza_vs_cats.utils.elo import Elo


def evaluation_loop(deck):
    clear_screen()
    print("\nVoting started! You will be asked to decide between couple of cards. \nPress 1 or 2 to vote.")
    elo_rating = Elo()
    n_votes = 0
    go_on = True
    while go_on:
        card_name_1, card_name_2 = get_two_random_cards_to_compare(deck)
        s = f"\nVote #{n_votes}: which one do you prefer? \n" \
            f" 1 -> {card_name_1} \n" \
            f" 2 -> {card_name_2}\n" \
            f"Press 1 or 2 to vote... (if you want to stop the voting, press 'n') "
        valid_input = False
        while not valid_input:
            choice = input(s)
            if choice in ["1", "2", "n"]:
                valid_input = True
                if choice == "n":
                    are_you_sure = get_yes_no_answer("Are you sure you want to stop? (y/n) ")
                    if are_you_sure:
                        go_on = False
                        print("Ok, stopping...")
                        break
                    else:
                        print("Ok, let's go on!")
                n_votes += 1
                if choice == "1":
                    deck[card_name_1][n_of_wins_str] += 1
                    rate_win, rate_loss = elo_rating.rate_1vs1(
                        deck[card_name_1][value_str],
                        deck[card_name_2][value_str])
                    deck[card_name_1][value_str] = rate_win
                    deck[card_name_2][value_str] = rate_loss
                elif choice == "2":
                    deck[card_name_2][n_of_wins_str] += 1
                    rate_win, rate_loss = elo_rating.rate_1vs1(
                        deck[card_name_2][value_str],
                        deck[card_name_1][value_str])
                    deck[card_name_2][value_str] = rate_win
                    deck[card_name_1][value_str] = rate_loss
                deck[card_name_1][n_matches_str] += 1
                deck[card_name_2][n_matches_str] += 1
            else:
                print(f"'{choice}' is not a valid input!")

    print("\n\n")


def get_two_random_cards_to_compare(complete_deck):
    """Return two cards from the deck for a comparison. One of the two will have the minimum amount of votes.

    This ensures that there are no cards that get no votes and, at the same time, if we add some new cards to the deck
    they will not be the only ones selected for the comparisons.
    """
    n_of_votes = [card_params[n_matches_str] for card_params in complete_deck.values()]
    min_n_of_votes = min(n_of_votes)
    deck_with_min_votes = {card_name: card_params for card_name, card_params in complete_deck.items()
                           if card_params[n_matches_str] == min_n_of_votes}
    card_name_with_few_votes = random.choice(list(deck_with_min_votes))

    # Get the second card name
    two_random_card_names = random.sample(list(complete_deck), 2)
    if card_name_with_few_votes != two_random_card_names[0]:
        second_card_name = two_random_card_names[0]
    else:
        second_card_name = two_random_card_names[1]

    # Return them in a random order
    if random.uniform(0, 1) < 0.5:
        return card_name_with_few_votes, second_card_name
    else:
        return second_card_name, card_name_with_few_votes
