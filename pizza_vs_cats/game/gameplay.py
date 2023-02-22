import json
import os.path
import sys

from pizza_vs_cats.config import decks_folder
from pizza_vs_cats.deck.collect_votes import evaluation_loop
from pizza_vs_cats.deck.create_deck import create_deck
from pizza_vs_cats.game.game import Game
from pizza_vs_cats.utils.input_utils import get_yes_no_answer, get_player_names, get_a_number, get_a_deck_name
from pizza_vs_cats.utils.print_utils import clear_screen, three_two_one_timer


def play_pizza_vs_cats():
    clear_screen()
    print("-----------------------------------")
    print("---- WELCOME TO PIZZA VS CATS! ----")
    print("-----------------------------------")
    three_two_one_timer()
    deck_name_no_ext, deck_path, deck = create_deck()

    clear_screen()
    print(f"You are now ready to start the voting phase for deck '{deck_name_no_ext}'. \n"
          f"You can skip this part if the deck already contains votes or if you di not add any new card!")

    print()

    add_votes_to_database = get_yes_no_answer("\nDo you want to add vote to the deck? "
                                              "\n y -> add votes"
                                              "\n n -> start the game directly"
                                              "\n ")

    if add_votes_to_database:
        evaluation_loop(deck)

        print()
        overwrite = get_yes_no_answer("Do you want to save the votes to the same deck or save a new one?\n"
                                      "y: save the votes to the same deck, n: save a new one ")
        if not overwrite:
            deck_name_no_ext, deck_name = get_a_deck_name(
                "Please enter the name of a deck that will contain the new votes. New deck name: ")
            deck_path = os.path.join(decks_folder, deck_name)
            with open(deck_path, 'w') as out_file:
                json.dump(deck, out_file, indent=4)
        else:
            with open(deck_path, 'w') as out_file:
                json.dump(deck, out_file, indent=4)

    clear_screen()
    start_game = get_yes_no_answer("You have finished to collect the votes. Do you want to start a game? (y/n) ")
    if not start_game:
        print("Okay. Goodbye ...")
        sys.exit()

    player_names = get_player_names()
    print("-----------------------------------")
    number_of_cards = get_a_number("How many cards per player?", [i + 1 for i in range(5)])
    print("-----------------------------------")
    game = Game(player_names, deck, number_of_cards)

    game.game_loop()
