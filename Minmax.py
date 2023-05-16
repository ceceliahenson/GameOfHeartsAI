def score_trick(trick):
    """
    Calculates score when trick is played
    :param trick:
    :return:
    """
    score = 0
    for card in trick:
        if card[1] == "Hearts":
            score += 1
        if card == ("Queen", "Spades"):
            score += 13
    return score


def get_card_points(card):
    """
    get points allocated to each card
    :param card:
    :return:
    """
    if card == ("Queen", "Spades"):
        return 13
    elif card[1] == "Hearts":
        return 1
    else:
        return 0


def get_trick_winner(trick):
    lead_suit = trick[0][1]
    highest_card = trick[0]
    for card in trick[1:]:
        if card[1] == lead_suit and card[0] > highest_card[0]:
            highest_card = card
    return trick.index(highest_card)


def get_valid_moves(hand, trick):
    if len(trick) == 0:
        return hand
    lead_suit = trick[0][1]
    follow_suit = [card for card in hand if card[1] == lead_suit]
    if follow_suit:
        return follow_suit
    else:
        return hand


def evaluate_state(state):
    hand, trick, scores = state
    score = 0
    for card in trick:
        score += get_card_points(card)
    for card in hand:
        score -= get_card_points(card)
    return score


def minimax(self, depth, player, hearts_broken):
    if depth == 0:
        return evaluate_state(self)

    hand, trick, scores = self
    valid_moves = get_valid_moves(hand, trick)

    if not valid_moves:
        return scores[player]

    # Max player: choose the move that maximizes the evaluation of the resulting state
    if player == 0:
        best_score = float('-inf')
        for move in valid_moves:
            new_hand = hand[:]
            new_hand.remove(move)
            new_trick = trick[:]
            new_trick.append(move)
            new_scores = scores[:]
            if move[1] == "Hearts":
                hearts_broken = True
            if len(new_trick) == 4:
                trick_score = score_trick(new_trick)
                new_scores[player] += trick_score
                winner = get_trick_winner(new_trick)
                if winner == player:
                    new_scores[player] += 100
            score = minimax((new_hand, new_trick, new_scores), depth - 1, 1, hearts_broken)
            best_score = max(best_score, score)
        return best_score

    # Min player: choose the move that minimizes the evaluation of the resulting state
    else:
        best_score = float('inf')
        for move in valid_moves:
            new_hand = hand[:]
            new_hand.remove(move)
            new_trick = trick[:]
            new_trick.append(move)
            new_scores = scores[:]
            if move[1] == "Hearts":
                hearts_broken = True
            if len(new_trick) == 4:
                trick_score = score_trick(new_trick)
                new_scores[player] += trick_score
                winner = get_trick_winner(new_trick)
                if winner == player:
                    new_scores[player] += 100
            score = minimax((new_hand, new_trick, new_scores), depth - 1, 0, hearts_broken)
            best_score = min(best_score, score)
        return best_score


def shoot_moon_evaluate_state(state, player):
    # Return the score of the state for the given player
    _, _, scores = state
    return scores[player]


def shooting_for_the_moon(state):
    hand, trick, scores = state
    hearts = [card for card in hand if card[1] == "Hearts"]
    queen_spades = ("Queen", "Spades") in hand
    if len(hearts) == len(hand) and queen_spades:
        # Player has captured all the hearts and the Queen of Spades
        return 26
    else:
        return 0


def shooting_for_moon_minimax(self, depth, player, hearts_broken):
    if depth == 0:
        return shooting_for_the_moon(self)

    hand, trick, scores = self
    valid_moves = get_valid_moves(hand, trick)

    if not valid_moves:
        return scores[player]

    # Max player: choose the move that maximizes the evaluation of the resulting state
    if player == 0:
        best_score = float('-inf')
        for move in valid_moves:
            new_hand = hand[:]
            new_hand.remove(move)
            new_trick = trick[:]
            new_trick.append(move)
            new_scores = scores[:]
            if move[1] == "Hearts":
                hearts_broken = True
            if len(new_trick) == 4:
                trick_score = score_trick(new_trick)
                new_scores[player] += trick_score
                winner = get_trick_winner(new_trick)
                if winner == player:
                    new_scores[player] += 100
            score = shooting_for_moon_minimax((new_hand, new_trick, new_scores), depth - 1, 1, hearts_broken)
            best_score = max(best_score, score)
        return best_score

    # Min player: choose the move that minimizes the evaluation of the resulting state
    else:
        best_score = float('inf')
        for move in valid_moves:
            new_hand = hand[:]
            new_hand.remove(move)
            new_trick = trick[:]
            new_trick.append(move)
            new_scores = scores[:]
            if move[1] == "Hearts":
                hearts_broken = True
            if len(new_trick) == 4:
                trick_score = score_trick(new_trick)
                new_scores[player] += trick_score
                winner = get_trick_winner(new_trick)
                if winner == player:
                    new_scores[player] += 100
            score = shooting_for_moon_minimax((new_hand, new_trick, new_scores), depth - 1, 0, hearts_broken)
            best_score = min(best_score, score)
        return best_score

