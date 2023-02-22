import json
import os.path
import random

from pizza_vs_cats.config import decks_folder
from pizza_vs_cats.utils.elo import INITIAL
from pizza_vs_cats.utils.input_utils import get_yes_no_answer, get_a_number, get_a_deck_name

value_str = "Value"
n_of_wins_str = "Number of wins"
n_matches_str = "Number of matches"


def create_deck():
    """Create a new deck, or add cards into an existing one.

    :return: the deck name, the path, and a dictionary representing the deck
    """
    create_new = get_yes_no_answer("Welcome , I am Trinity, I will follow you in the creation of your deck. "
                                   "Do you want to create a new deck? \n"
                                   "y -> create new deck / n -> use and select existing one: ")

    if create_new:
        print("You are now in the creation deck room, I'm your database and guide.\n"
              "I can show you the path, but you only know the destination.\n"
              "My database is empty and it doesn't feel good. The only weapon that we have against them is "
              "knowledge, I'm counting on you on that.\n")
        selected_deck_name_no_ext, selected_deck_name = get_a_deck_name()
        deck_path = os.path.join(decks_folder, selected_deck_name)
        deck = dict()
    else:
        print("These are the names of the available decks:")
        decks_names = [filename for filename in os.listdir(decks_folder) if filename.endswith('.json')]

        print()
        for i, deck_name in enumerate(decks_names):
            tmp_deck = json.load((open(os.path.join(decks_folder, deck_name))))
            deck_name_no_ext = deck_name[:-5]
            n_cards = len(tmp_deck)
            sample_cards = random.sample(list(tmp_deck), min(3, n_cards))
            print(f" - Deck number {i}: name '{deck_name_no_ext}'. A total of {len(tmp_deck)} cards,"
                  f" including {sample_cards}")

        print()
        deck_index = get_a_number("Please insert the number of the deck you want to use and press enter. Deck number: ",
                                  range(len(decks_names)))
        selected_deck_name = decks_names[deck_index]
        selected_deck_name_no_ext = selected_deck_name[:-5]
        deck_path = os.path.join(decks_folder, selected_deck_name)
        deck = json.load(open(deck_path))

        print()
        print(f"Welcome back with deck '{selected_deck_name_no_ext}', I was waiting for you. "
              f"In moments like this we have to be careful and patient.\n")

    print()
    while get_yes_no_answer(
            f"'{selected_deck_name_no_ext}' has {len(deck)} cards. Do you want to add new cards? (y/n) "):
        new_card_name = input("Write the card to add to the deck and press enter. Card name: ")

        rnumb = random.randint(0, 100)
        if rnumb < 30:
            print(f"Perfect, '{new_card_name}' will be strong against them!")
        elif 31 < rnumb < 50:
            print(f"{new_card_name}... if you say so...")
        else:
            print(f"'{new_card_name}', Nice!")

        card_name_is_correct = get_yes_no_answer("Confirm? (y/n) ")

        if not card_name_is_correct:
            if random.randint(0, 100) > 50:
                print(f"I will discard '{new_card_name}', what a pitie. I was already in love with it!")
            else:
                print(f"Ok, you do not like '{new_card_name}'. Stop wasting my time and be more careful!")
        else:
            add_new_card(deck, new_card_name)

        print()

    with open(deck_path, 'w') as out_file:
        json.dump(deck, out_file, indent=4)

    return selected_deck_name_no_ext, deck_path, deck


def add_new_card(deck, new_card_name):
    if new_card_name in deck.keys():
        print(f"Wow, '{new_card_name}' is already in the deck. I will not add it again!")
        return

    new_card_params_dict = {
        value_str: INITIAL,
        n_of_wins_str: 0,
        n_matches_str: 0
    }
    deck[new_card_name] = new_card_params_dict


def reset_deck(deck_name):
    deck_path = os.path.join(decks_folder, deck_name)
    deck = json.load(open(deck_path, 'r'))

    out_path = os.path.join(decks_folder, deck_name[:-5] + '_backup.json')
    with open(out_path, 'w') as out_file:
        json.dump(deck, out_file, indent=4)

    restored_deck = dict()
    for card_name in deck.keys():
        add_new_card(restored_deck, card_name)

    with open(deck_path, 'w') as out_file:
        json.dump(restored_deck, out_file, indent=4)
