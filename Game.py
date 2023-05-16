import random
from Minmax import *

scores = [0, 0]
player_name = ["AI1", "AI2"]


def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "King", "Queen", "Jack", "Ace"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


def ai_player_shoot_moon_strat(hand, trick, hearts_broken):
    valid_moves = get_valid_moves(hand, trick)
    best_move = None
    best_score = float('-inf')
    for move in valid_moves:
        new_trick = trick.copy()
        new_trick.append(move)
        new_hand = hand.copy()
        new_hand.remove(move)
        score = shooting_for_moon_minimax((new_hand, new_trick, [0, 0]), 3, 1, hearts_broken)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def ai_player_point_strat(hand, trick, hearts_broken):
    valid_moves = get_valid_moves(hand, trick)
    best_move = None
    best_score = float('-inf')
    for move in valid_moves:
        new_trick = trick.copy()
        new_trick.append(move)
        new_hand = hand.copy()
        new_hand.remove(move)
        score = minimax((new_hand, new_trick, [0, 0]), 3, 1, hearts_broken)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def ai_player_rand(hand, trick):
    valid_moves = get_valid_moves(hand, trick)
    return random.choice(valid_moves)


def deal_cards(deck):
    hands = [[] for _ in range(2)]
    for i in range(0, len(deck), 2):
        for j in range(2):
            hands[j].append(deck[i + j])
    return hands


def play_card(player, hand, trick, hearts_broken):
    valid_moves = get_valid_moves(hand, trick)

    #### area where you can change the type of AI player ####
    if player == 1:
        '''
        can change player here by uncommenting the player you want
        '''
        ## point strategy ai ##
        #card = ai_player_point_strat(hand, trick, hearts_broken)

        ## random valid pick ai ##
        card = ai_player_rand(hand, trick)

        ## shooting the moon ai ##
        #card = ai_player_shoot_moon_strat(hand, trick, hearts_broken)
    elif player == 0:
        '''
        can change player here by uncommenting the player you want
        '''
        ## point strategy ai ##
        #card = ai_player_point_strat(hand, trick, hearts_broken)

        ## random valid pick ai ##
        card = ai_player_rand(hand, trick)

        ## shooting the moon ai ##
        #card = ai_player_shoot_moon_strat(hand, trick, hearts_broken)
    else:
        while True:
            index = int(input("Enter index of card to play: "))
            card = hand[index]
            if card not in valid_moves:
                continue
            if card[1] == "Hearts":
                hearts_broken = True
            hand.remove(card)
            trick.append(card)
            return hearts_broken
    if card[1] == "Hearts":
        hearts_broken = True
    hand.remove(card)
    trick.append(card)
    return hearts_broken


def play_round(start_player, hands):
    trick = []
    hearts_broken = False
    for i in range(2):
        player = (start_player + i) % 2
        hand = hands[player]
        hearts_broken = play_card(player, hand, trick, hearts_broken)
    winner = get_trick_winner(trick)
    return winner


def score_game(hands, scores):
    for i in range(2):
        hand = hands[i]
        for card in hand:
            if card[1] == "Hearts":
                scores[i] += 1
            if card == ("Queen", "Spades"):
                scores[i] += 13


def play_game(ai1_win=0, ai2_win=0):
    deck = create_deck()
    hands = deal_cards(deck)
    start_player = random.randint(0, 0)
    trick = []
    for i in range(13):
        winner = play_round(start_player, hands)
        start_player = winner
        score = score_trick(trick)
        scores[winner] += score

    score_game(hands, scores)
    if min(scores) == scores[0]:
        ai1_win += 1
    else:
        ai2_win += 1
    return ai1_win, ai2_win


def main():
    ai1_win = 0
    ai2_win = 0

    for done in range(100):
        ai1_win, ai2_win = play_game(ai1_win, ai2_win)
    print("Final scores after playing 100 games:", scores)

    if min(scores) == scores[0]:
        print("Winner:", player_name[0], "with the lowest score", min(scores))
        print(f"Won: {ai1_win}/{100} times")
    else:
        print("Winner:", player_name[1], "with the lowest score", min(scores))
        print(f"Won: {ai2_win}/{100} times")


if __name__ == '__main__':
    main()
