import random

# Card values for blackjack
card_values = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
    'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10,
    'King': 10, 'Ace': 11
}

# Card suits
suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']

# Card faces
faces = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace']

class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if not self.root:
            self.root = TreeNode(key, value)
        else:
            self.helper_insert_recursively(self.root, key, value)

    def helper_insert_recursively(self, node, key, value):
        if value < node.value:
            if not node.left:
                node.left = TreeNode(key, value)
            else:
                self.helper_insert_recursively(node.left, key, value)
        else:
            if not node.right:
                node.right = TreeNode(key, value)
            else:
                self.helper_insert_recursively(node.right, key, value)

    def find_best_option(self, target_value):
        return self.helper_find_best_option(self.root, target_value, None)

    def helper_find_best_option(self, node, target_value, best_choice):
        if not node:
            return best_choice
        if node.value <= target_value:
            if not best_choice or target_value - node.value < target_value - best_choice.value:
                best_choice = node
            best_choice = self.helper_find_best_option(node.right, target_value, best_choice)
        else:
            best_choice = self.helper_find_best_option(node.left, target_value, best_choice)
        return best_choice

class Deck:
    def __init__(self):
        self.cards = [(face, suit) for face in faces for suit in suits]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0) if self.cards else None

def calculate_hand_value(hand):
    total = sum(card_values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'Ace')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def calculate_probability(player_hand, dealer_visible, deck):
    player_current = calculate_hand_value(player_hand)
    dealer_current = card_values[dealer_visible[0]]
    favorable_outcomes = 0
    total_outcomes = 0
    for face, _ in deck.cards:
        new_value = calculate_hand_value(player_hand + [(face, 'Suits')])
        if new_value <= 21:
            favorable_outcomes += 1
        total_outcomes += 1
    probability = favorable_outcomes / total_outcomes if total_outcomes else 0
    return probability

def blackjack():
    deck = Deck()
    bst = BST()
    for card in deck.cards:
        bst.insert(card, card_values[card[0]])

    balance = int(input("How much money do you want to start with? $"))
    continue_playing = True
    while continue_playing and balance > 0:
        bet = int(input(f"Your balance is ${balance}. How much would you like to bet? $"))
        if bet > balance:
            print("You cannot bet more than your current balance.")
            continue

        player_hand = [deck.deal_card(), deck.deal_card()]
        dealer_hand = [deck.deal_card(), deck.deal_card()]

        print("Player's hand:", player_hand)
        print("Dealer's hand:", [dealer_hand[0], "Hidden"])

        while calculate_hand_value(player_hand) < 21:
            probability = calculate_probability(player_hand, dealer_hand[0], deck)
            print(f"Probability of improving hand without busting: {probability:.2%}")
            best_card = bst.find_best_option(21 - calculate_hand_value(player_hand))
            if best_card:
                print(f"Best card to draw next: {best_card.key}")
            else:
                print("No suitable card to draw next.")
            action = input("Do you want to hit or stand? (h/s): ").lower()
            if action == 'h':
                new_card = deck.deal_card()
                if new_card:
                    player_hand.append(new_card)
                    print("Player's hand:", player_hand)
                    if calculate_hand_value(player_hand) > 21:
                        break
            else:
                break

        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.deal_card())

        print("Dealer's final hand:", dealer_hand, ", Total value:", calculate_hand_value(dealer_hand))
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if player_value > 21:
            print("Player busts! Dealer wins.")
            balance -= bet
        elif dealer_value > 21 or player_value > dealer_value:
            print("Player wins!")
            balance += bet
        elif player_value < dealer_value:
            print("Dealer wins.")
            balance -= bet
        else:
            print("It's a push!")

        continue_playing = input("Play another round? (yes/no): ").lower() == 'yes'
    print("Game over! Your final balance is $", balance)

if __name__ == "__main__":
    blackjack()
