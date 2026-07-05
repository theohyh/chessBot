import chess


def main():
    print("=" * 40)
    # Rendu textuel ou message de bienvenue
    print("   DÉMARRAGE DU BOT D'ÉCHECS MINIMAX   ")
    print("=" * 40)

    board = chess.Board()

    print(board.legal_moves)

    print(chess.Move.from_uci("a8a1") in board.legal_moves)
    print(board.push_san("e4"))
    print(board.push_san("e5"))
    board.pop()

    print(board)


if __name__ == "__main__":
    main()
