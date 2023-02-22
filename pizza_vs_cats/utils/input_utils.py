def get_yes_no_answer(input_str):
    while True:
        answer = input(input_str)
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Not valid. Please type 'y' or 'n'!")


def get_player_names():
    print("Now, you will be asked the name of the players.")
    player_names = list()
    go_on = True
    while go_on:
        add_new_player = get_yes_no_answer(f"For the moment, the players are: {player_names}. Add a new player? (y/n) ")
        if not add_new_player:
            if len(player_names) < 2:
                print("You need at least 2 players!")
            else:
                go_on = False
                continue
        name_is_correct = False
        while not name_is_correct:
            player_name = input(f"Add the name of player {len(player_names) + 1}: ")
            name_is_correct = get_yes_no_answer(f"Got '{player_name}'. Confirm? (y/n) ")
            if name_is_correct:
                print("Perfect!")
                player_names.append(player_name)
            else:
                print("Oh no... type it again!")
    return player_names


def get_a_number(input_str, valid_range):
    while True:
        user_input = input(input_str)
        try:
            number = int(user_input)
        except ValueError:
            number = None
        if number in valid_range:
            return number
        else:
            print(f"'{user_input}' is not valid. Please type a number in {list(valid_range)}")


def get_a_deck_name(input_str=None):
    """Get a deck name from the user and make sure the json extension is handled properly (experimental, there is
    probably a library for this)
    """
    if input_str is None:
        input_str = "Please insert the name of the NEW deck and press enter. Deck name: "
    selected_deck_name_no_ext = input(input_str)
    if selected_deck_name_no_ext[:-5] == '.json':
        selected_deck_name_no_ext = selected_deck_name_no_ext[:-5]
    selected_deck_name_with_ext = selected_deck_name_no_ext + '.json'
    return selected_deck_name_no_ext, selected_deck_name_with_ext
