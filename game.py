import sys
import os
import random

# Налаштування UTF-8 для консолі
if sys.platform == "win32":
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} {self.suit}"

class Deck:
    SUITS = ['♠', '♥', '♦', '♣']
    
    def __init__(self, game_type="blackjack"):
        self.cards = []
        self.game_type = game_type
        self._build_deck()

    def _build_deck(self):
        if self.game_type == "21":
            ranks = {
                '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                'Валет': 2, 'Дама': 3, 'Король': 4, 'Туз': 11
            }
        else:
            ranks = {
                '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                '8': 8, '9': 9, '10': 10, 'Валет': 10, 'Дама': 10, 
                'Король': 10, 'Туз': 11
            }
        
        for suit in self.SUITS:
            for rank, value in ranks.items():
                self.cards.append(Card(suit, rank, value))
        
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self, game_type="blackjack"):
        if game_type == "21" and len(self.cards) == 2 and self.cards[0].rank == 'Туз' and self.cards[1].rank == 'Туз':
            return 21

        total = sum(card.value for card in self.cards)
        
        if game_type == "blackjack":
            aces = sum(1 for card in self.cards if card.rank == 'Туз')
            while total > 21 and aces > 0:
                total -= 10
                aces -= 1
                
        return total

    def show_hand(self, hide_first=False, game_type="blackjack"):
        if hide_first:
            cards_str = f"[Прихована карта], {self.cards[1]}"
            print(f"{self.name}: {cards_str}")
        else:
            cards_str = ", ".join(str(c) for c in self.cards)
            print(f"{self.name}: {cards_str} | Сума: {self.get_value(game_type)}")

class CardGame:
    def __init__(self):
        self.mode = None

    def select_mode(self):
        print("=== ЛАБОРАТОРНА РОБОТА: КАРТКОВІ ГРИ ===")
        print('1. "21" (36 карт, Валет=2, Дама=3, Король=4, Туз=11, 2 Тузи = 21)')
        print('2. "Блекджек" (52 карти, Фігури=10, Туз=11 або 1)')
        
        while True:
            choice = input("Оберіть режим (1 або 2): ").strip()
            if choice == '1':
                self.mode = "21"
                break
            elif choice == '2':
                self.mode = "blackjack"
                break
            print("Некоректне введення! Введіть 1 або 2.")

    def play_round(self):
        deck = Deck(game_type=self.mode)
        player = Hand("Гравець")
        dealer = Hand("Дилер")

        player.add_card(deck.deal())
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())

        print(f"\n--- Початок гри: {'Двадцять одне' if self.mode == '21' else 'Блекджек'} ---")
        
        while True:
            print("\n" + "="*30)
            player.show_hand(game_type=self.mode)
            dealer.show_hand(hide_first=True, game_type=self.mode)
            
            p_score = player.get_value(self.mode)
            
            if p_score >= 21:
                break
                
            choice = input("\nВзяти карту? (1 - Так, 0 - Ні): ").strip()
            if choice == '1':
                player.add_card(deck.deal())
            elif choice == '0':
                break
            else:
                print("Введіть 1 або 0!")

        p_score = player.get_value(self.mode)

        if p_score > 21:
            print("\n" + "="*30)
            player.show_hand(game_type=self.mode)
            print("\n❌ Перебір! Ви програли.")
            return

        print("\n--- Хід Дилера ---")
        while dealer.get_value(self.mode) < 17:
            dealer.add_card(deck.deal())

        d_score = dealer.get_value(self.mode)

        print("\n" + "="*30)
        print("--- РЕЗУЛЬТАТИ ---")
        player.show_hand(game_type=self.mode)
        dealer.show_hand(game_type=self.mode)

        if d_score > 21:
            print("\n🎉 У дилера перебір! Ви виграли!")
        elif p_score > d_score:
            print("\n🎉 Вітаємо, ви виграли!")
        elif p_score < d_score:
            print("\n❌ Ви програли.")
        else:
            print("\n🤝 Нічия!")

    def start(self):
        self.select_mode()
        while True:
            self.play_round()
            again = input("\nЗіграти ще раз? (1 - Так, 0 - Вихід): ").strip()
            if again != '1':
                print("Дякуємо за гру!")
                break

if __name__ == "__main__":
    game = CardGame()
    game.start()
