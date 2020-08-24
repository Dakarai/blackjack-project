import random

suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit[0].lower()
        self.rank = rank
        self.value = values[rank]

    def __repr__(self):
        return self.rank + "" + self.suit


class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop(0)

    def __repr__(self):
        return str(self.all_cards)


class Hand:
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

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


if __name__ == '__main__':
    # create players w/ starting balance
    name = input("Welcome to the table. What is your name? ")
    player_human = Player(name, 1000)
    player_dealer = Player("Dealer", 1000)

    play_game = True
    while play_game:
        # create deck object and shuffle it
        new_deck = Deck()
        new_deck.shuffle()

        # reset player hands
        player_human.new_game()
        player_dealer.new_game()

        print("{}'s Balance: {}".format(name, player_human.balance))
        while True:
            try:
                bet_amount = int(input("How much to bet? "))
            except ValueError:
                print("Looks like you didn't enter an integer.")
                pass
            else:
                break

        # deal and display initial cards and totals
        player_human.hand.add_card(new_deck.deal_one())
        player_human.hand.add_card(new_deck.deal_one())
        player_dealer.hand.add_card(new_deck.deal_one())
        print("Dealer has: {}".format(player_dealer.hand))
        print("{} has: {}".format(name, player_human.hand))
        print("{}'s total: {}".format(name, player_human.hand.hand_total()))

        # continue until player stands or busts
        stand = False
        while not stand and player_human.hand.hand_total() < 21:
            while True:
                response = input("[H]it or [S]tand? ")
                if response[0].capitalize() == 'H':
                    player_human.hand.add_card(new_deck.deal_one())
                    break
                elif response[0].capitalize() == 'S':
                    stand = True
                    break
                else:
                    print("Invalid response.")
                    continue
            print()
            print("DEALER HAS: {}".format(player_dealer.hand))
            print("{} has: {}".format(name, player_human.hand))
            print("{}'s total: {}".format(name, player_human.hand.hand_total()))
            print()

        # dealer game play
        while player_dealer.hand.hand_total() < player_human.hand.hand_total() <= 21:
            player_dealer.hand.add_card(new_deck.deal_one())
            print("Dealer has: {}".format(player_dealer.hand))
            print("Dealer total: {}".format(player_dealer.hand.hand_total()))
            print()

        # evaluate winner
        player_hand_total = player_human.hand.hand_total()
        dealer_hand_total = player_dealer.hand.hand_total()
        print("{}'s total: {}".format(name, player_hand_total))
        print("Dealer total: {}".format(dealer_hand_total))
        if player_hand_total > 21:
            print("Bust! ")
            player_human.balance -= bet_amount
        elif dealer_hand_total < player_hand_total <= 21:
            print("You win! ")
            player_human.balance += bet_amount
        elif player_hand_total < dealer_hand_total <= 21:
            print("You lose! ")
            player_human.balance -= bet_amount
        elif dealer_hand_total == player_hand_total:
            print("Tie! ")
        else:
            print("Dealer busts! You win! ")
            player_human.balance += bet_amount
