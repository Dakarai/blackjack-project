import random

suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1}
max_shoe_size = 12
shuffle_at_percentage = 0.25
blackjack_payout_ratio = 1.5


class Card:
    def __init__(self, suit, rank):
        self.suit = suit[0].lower()
        self.rank = rank
        self.value = values[rank]

    def __repr__(self):
        return self.rank + "" + self.suit


class Shoe:
    def __init__(self, decks):
        self.all_cards = []
        self.size = decks * 52
        for _ in range(decks):
            for suit in suits:
                for rank in ranks:
                    self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop(0)

    def remaining_percentage(self):
        return len(self.all_cards) / self.size

    def __repr__(self):
        return str(self.all_cards)


class Hand:
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def has_blackjack(self):
        if self.hand_size() == 2 and self.hand_total() == 21:
            return True
        return False

    def hand_size(self):
        return len(self.hand)

    def hand_total(self):
        num_aces = 0
        temp_total = 0
        current_hand = self.hand
        for current_card in current_hand:
            if current_card.rank == 'A':
                # give all Aces a minimum 1 point, 10 more will be added later if needed
                num_aces += 1
                temp_total += 1
            else:
                temp_total += current_card.value

        # add the extra 10 points from the Aces if beneficial
        while temp_total <= 11 and num_aces >= 1:
            temp_total += 10
            num_aces -= 1
        return temp_total

    def __repr__(self):
        return str(self.hand)


class Player:
    def __init__(self, player_name, balance):
        self.player_name = player_name.capitalize()
        self.hand = Hand()
        self.balance = balance

    def new_game(self):
        self.hand = Hand()


def evaluate_winner(player_human, player_dealer, bet_amount):
    player_hand_total = player_human.hand.hand_total()
    dealer_hand_total = player_dealer.hand.hand_total()
    print("{}'s total: {}".format(player_human.player_name, player_hand_total))
    print("Dealer total: {}".format(dealer_hand_total))
    print()

    if player_hand_total > 21:
        print("Bust!")
        player_human.balance -= bet_amount
    elif player_dealer.hand.has_blackjack():
        if player_human.hand.has_blackjack():
            print("Push! Dealer and player have blackjack!")
        else:
            print("Dealer blackjack! You lose!")
            player_human.balance -= bet_amount
    elif player_human.hand.has_blackjack():
        print("Blackjack!")
        player_human.balance += bet_amount * blackjack_payout_ratio
    elif dealer_hand_total < player_hand_total <= 21:
        print("You win!")
        player_human.balance += bet_amount
    elif player_hand_total < dealer_hand_total <= 21:
        print("You lose!")
        player_human.balance -= bet_amount
    elif dealer_hand_total == player_hand_total:
        print("Push!")
    else:
        print("Dealer busts! You win!")
        player_human.balance += bet_amount


def print_rules():
    # create players w/ starting balance
    print("Blackjack Rules:")
    print("Any number of decks from 1-12.")
    print("Shoe will shuffle after {}% usage.".format(shuffle_at_percentage*100))
    print("Double Down and Surrender are permitted.")
    print("Dealer must stand on soft 17. Blackjack pays 3:2")
    print()


if __name__ == '__main__':
    print_rules()
    name = input("Welcome to the table. What is your name? ")
    player_human = Player(name, 1000)
    player_dealer = Player("Dealer", 1000)

    while True:
        try:
            num_decks = int(input("How many decks to play with? "))
        except ValueError:
            print("Looks like you didn't enter an integer.")
            pass
        else:
            if num_decks > max_shoe_size:
                print("Let's not get crazy here. Choose between 1-12 decks.")
            elif num_decks <= 0:
                print("Choose a real value to play with.")
            else:
                break

    # create deck object and shuffle it
    new_shoe = Shoe(num_decks)
    new_shoe.shuffle()
    play_game = True
    while play_game:
        # check if current cards in shoe is below the threshold needed to reshuffle
        if new_shoe.remaining_percentage() < shuffle_at_percentage:
            new_shoe = Shoe(num_decks)
            new_shoe.shuffle()

        # reset player hands
        player_human.new_game()
        player_dealer.new_game()

        print()
        print("{}'s Balance: {}".format(name, player_human.balance))
        while True:
            try:
                bet_amount = int(input("How much to bet? "))
                print()
            except ValueError:
                print("Looks like you didn't enter an integer.")
                pass
            else:
                if bet_amount > player_human.balance:
                    print("You can't bet that much!")
                elif bet_amount <= 0:
                    print("Choose a real value to bet with.")
                else:
                    break

        # deal and display initial cards and totals
        player_human.hand.add_card(new_shoe.deal_one())
        player_human.hand.add_card(new_shoe.deal_one())
        player_dealer.hand.add_card(new_shoe.deal_one())
        print("Dealer has: {}".format(player_dealer.hand))
        print("{} has: {}".format(name, player_human.hand))
        print("{}'s total: {}".format(name, player_human.hand.hand_total()))

        # continue until player stands or busts
        stand = False
        skip_dealer = False
        while not stand and player_human.hand.hand_total() < 21:
            while True:
                if player_human.hand.hand_size() == 2:
                    response = input("[H]it, [S]tand, [D]ouble Down, or Su[R]render? ")
                    if response[0].capitalize() == 'H':
                        player_human.hand.add_card(new_shoe.deal_one())
                        break
                    elif response[0].capitalize() == 'S':
                        stand = True
                        break
                    elif response[0].capitalize() == 'D':
                        if bet_amount * 2 > player_human.balance:
                            print("You don't have enough to double down!")
                            continue
                        else:
                            print("Dealing one.")
                            bet_amount = bet_amount * 2
                            player_human.hand.add_card(new_shoe.deal_one())
                            stand = True
                            break
                    elif response[0].capitalize() == "R":
                        # a surrender immediately ends the game
                        print("Surrendered. Half the bet is returned. ")
                        player_human.balance -= bet_amount / 2
                        stand = True
                        skip_dealer = True
                        break
                    else:
                        print("Invalid response.")
                        continue

                else:
                    response = input("[H]it or [S]tand? ")
                    if response[0].capitalize() == 'H':
                        player_human.hand.add_card(new_shoe.deal_one())
                        break
                    elif response[0].capitalize() == 'S':
                        stand = True
                        break
                    else:
                        print("Invalid response.")
                        continue
            print()
            print("Dealer has: {}".format(player_dealer.hand))
            print("{} has: {}".format(name, player_human.hand))
            print("{}'s total: {}".format(name, player_human.hand.hand_total()))
            print()

        # dealer game play
        # must stand on soft 17 (any 17, including A + 6)
        if not skip_dealer:
            while player_dealer.hand.hand_total() < 17:
                player_dealer.hand.add_card(new_shoe.deal_one())
                print("Dealer has: {}".format(player_dealer.hand))
                print("Dealer total: {}".format(player_dealer.hand.hand_total()))
                print()

            evaluate_winner(player_human, player_dealer, bet_amount)
