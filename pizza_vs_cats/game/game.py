import copy
import random

from pizza_vs_cats.deck.collect_votes import value_str
from pizza_vs_cats.deck.create_deck import n_matches_str, n_of_wins_str
from pizza_vs_cats.player.player import Player
from pizza_vs_cats.utils.print_utils import clear_screen


class Game:
    def __init__(self, player_names, full_deck, n_cards_initial):
        self._n_players = len(player_names)
        self._full_deck = full_deck
        self._remaining_cards = copy.copy(self._full_deck)
        self._n_cards_initial = n_cards_initial
        self._players = self._initialize_players(player_names)

    def _initialize_players(self, player_names):
        players = list()
        for player_name in player_names:
            initial_card_names = list()
            for _ in range(self._n_cards_initial):
                card_name = self._get_one_random_card_from_remaining_cards()
                initial_card_names.append(card_name)
            player = Player(player_name, initial_card_names)
            players.append(player)
        return players

    def game_loop(self):
        print("THE GAME IS ABOUT TO START ...")
        input("Press any key to start!")

        round = 0
        while self._get_player_that_finished_all_cards() is None:
            played_cards = list()
            for (i, player) in enumerate(self._players):
                clear_screen()
                input(f"ROUND {round}: Give the laptop to '{player.name}' ... "
                      f"'{player.name}': once you have the laptop, press enter! ")
                clear_screen()
                print(f"Players played {played_cards}")
                played_card = player.play_card()
                played_cards.append(played_card)
            clear_screen()
            best_card_index = self._get_best_card_index(played_cards)
            self._give_new_cards_to_players(self._players, self._players[best_card_index])
            self._players = self._get_sorted_players(winning_player=self._players[best_card_index])
            input("----press any key to continue---")
            clear_screen()

        player_with_no_cards = self._get_player_that_finished_all_cards()
        print(f"We have a winner!!! Well done '{player_with_no_cards.name}'!")

    def _get_one_random_card_from_remaining_cards(self):
        card_name = random.choice(list(self._remaining_cards))
        self._remaining_cards.pop(card_name)
        return card_name

    def _get_player_that_finished_all_cards(self):
        for player in self._players:
            if not player.are_cards_left():
                return player
        return None

    def _get_best_card_index(self, card_names):
        def sort_cards_function(card):
            _, card_params = card
            return card_params[value_str], card_params[n_matches_str], card_params[n_of_wins_str]

        reduced_deck = dict()
        for (i, card_name) in enumerate(card_names):
            reduced_deck[card_name] = self._full_deck[card_name]
            reduced_deck[card_name]["player_index"] = i

        sorted_cards = sorted(reduced_deck.items(), key=sort_cards_function)
        best_card = sorted_cards[-1]
        best_card_name = best_card[0]
        winning_player_index = best_card[1]["player_index"]

        print(f"Wow! {self._players[winning_player_index].name} won with {best_card_name}, among {card_names}")
        return winning_player_index

    def _give_new_cards_to_players(self, players, best_player):
        if len(self._remaining_cards) < self._n_players:
            print("NOT ENOUGH CARDS LEFT. FIGHT WITH WHAT YOU HAVE!")
        for player in players:
            if player != best_player:
                card_name = self._get_one_random_card_from_remaining_cards()
                player.add_card(card_name)

    def _get_sorted_players(self, winning_player):
        """Return a list where the first player is the winning player and the other elements are the players sorted
        by number of cards"""
        not_winning_players = [player for player in self._players if player != winning_player]
        sorted_players = sorted(not_winning_players, key=lambda player: player.n_cards_left())
        sorted_players.insert(0, winning_player)
        return sorted_players
