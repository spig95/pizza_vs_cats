from pizza_vs_cats.utils.input_utils import get_a_number


class Player:
    def __init__(self, name, initial_card_names: list):
        self.name = name
        self.card_names = initial_card_names

    def play_card(self):
        """Let the player choose a card and remove it from the list of cards"""
        s = f"Hey {self.name}! Which card do you want to play?"
        for (i, name) in enumerate(self.card_names):
            s += f"\n {i} -> {name}"
        s += "\n"
        print(s)
        card_index = get_a_number("Type the card number: ", range(self.n_cards_left()))
        played_card_name = self.card_names[card_index]
        self.card_names.pop(card_index)
        return played_card_name

    def add_card(self, card_name):
        self.card_names.append(card_name)

    def are_cards_left(self):
        return len(self.card_names) > 0

    def n_cards_left(self):
        return len(self.card_names)
