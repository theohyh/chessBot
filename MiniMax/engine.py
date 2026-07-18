import chess

from .evaluation import evaluate_board


def minimax(board: chess.Board, depth: int, max_player: bool):
    return maximize(board, depth) if max_player else minimize(board, depth)


def maximize(board: chess.Board, depth: int):
    best_move = None
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), best_move
    max_eval = float("-inf")

    for move in board.legal_moves:
        board.push(move)
        score, _ = minimize(board, depth - 1)
        if score > max_eval:
            max_eval = score
            best_move = move
        board.pop()
    return max_eval, best_move


def minimize(board: chess.Board, depth: int):
    best_move = None
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), best_move
    min_eval = float("inf")

    for move in board.legal_moves:
        board.push(move)
        score, _ = maximize(board, depth - 1)
        if score < min_eval:
            min_eval = score
            best_move = move
        board.pop()
    print(min_eval, best_move)
    return min_eval, best_move
