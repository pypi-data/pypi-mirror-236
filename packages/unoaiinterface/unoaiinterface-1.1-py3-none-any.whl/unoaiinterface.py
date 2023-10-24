class Discard:
    def __init__(self):
        self.cards = []
        self.top_card = None

    def add(self, card):
        self.cards.append(card)
        self.top_card = card

    def get_discard(self):
        return self.cards


class Player:
    def __init__(self):
        """
        Parameters:
            hand (list): The player's hand
        """
        self.hand = []

    def __str__(self):
        output = ""
        for i, card in enumerate(self.hand):
            output += f"{i+1}. {card}\n"
        return output

    def give(self, card):
        """
        Gives the player a card.

        Parameters:
            card (Card): The card to give to the player
        """
        self.hand.append(card)

    def set_hand(self, hand: list):
        """
        Sets the player's hand to the given list.

        Parameters:
            hand (list): The player's hand
        """
        self.hand = hand

    def draw_card(self, deck):
        """
        Draws a card from the deck and appends it to the player's hand.

        Parameters:
            deck (Deck): The deck to draw from
        """
        self.hand.append(deck.draw_card())

    def play_card(self, card: int, discard: Discard) -> bool:
        """
        Checks if a card is playable and handles the logic for playing a card.

        Parameters:
            card (int): The index of the card to play
            discard (Discard): The discard pile

        Returns:
            bool: Whether the card was playable
        """
        if self.hand[card].is_playable(discard.top_card):
            discard.add(self.hand[card])
            self.hand.remove(self.hand[card])
            return True
        return False


class Card:
    def __init__(self, color: str, value: int):
        """
        Parameters:
            color (str): The color of the card
            value (int): The value of the card
        """
        self.color = color
        self.value = value
        self.action = None

    def __str__(self):
        return f"{self.color} {self.value}"

    def is_playable(self, top_card) -> bool:
        """
        Checks if a card is playable.

        Parameters:
            top_card (Card): The top card of the discard pile

        Returns:
            bool: Whether the card is playable
        """
        return self.color == top_card.color or self.value == top_card.value or self.color == 'wild'


class SpecialCard(Card):
    def __init__(self, color: str, value: str, action: str):
        """
        Parameters:
        color (str): The color of the card
        value (str): The value of the card
        action (str): The action of the card
        """
        super().__init__(color, value)
        self.action = action

    def __str__(self):
        return f"{self.color} {self.action}"


class Deck:
    def __init__(self):
        self.cards = []
        self.setup_deck()

    def __str__(self):
        return f"Deck: {self.cards}"

    def setup_deck(self):
        """
        Sets up the deck with the standard 108 cards.
        """
        colors = ['Red', 'Blue', 'Green', 'Yellow']
        values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        special_cards = ['skip', 'switch', 'two']

        for color in colors:
            self.cards.append(Card(color, '0'))
            for value in values:
                for _ in range(2):
                    self.cards.append(Card(color, value))
            for i, special in enumerate(special_cards):
                for _ in range(2):
                    self.cards.append(SpecialCard(color, -(i+1), special))

        for _ in range(4):
            self.cards.append(SpecialCard('wild', -4, 'wild'))
            self.cards.append(SpecialCard('wild', -5, 'four'))

        self.shuffle()

    def shuffle(self):
        """
        Shuffles the deck.
        """
        from random import shuffle
        shuffle(self.cards)

    def draw_card(self, discard: Discard = []) -> Card:
        """
        Draws a card from the deck.

        Parameters:
            discard (Discard): The discard pile

        Returns:
            Card: The card drawn
        """
        if not self.cards:
            self.cards = discard.cards[::-1]
            discard.cards = []
        card = self.cards.pop()
        if card.value in [-4, -5]:
            card.color = 'wild'
        return card

    def add_card(self, card):
        """
        Adds a card to the deck.

        Parameters:
            card (Card): The card to add
        """
        self.cards.append(card)
