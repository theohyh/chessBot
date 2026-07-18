import chess

from MiniMax.engine import minimax


def main():
    print("=" * 40)
    print("   DÉMARRAGE DU BOT D'ÉCHECS MINIMAX   ")
    print("=" * 40)

    board = chess.Board()
    human = chess.WHITE
    depth = 3

    while not board.is_game_over():
        print("=" * 40)
        print(board)
        print("=" * 40)
        if board.turn == human:
            move_str = input("Votre Coup (ex: e2e4): ").strip()
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Coup invalide.")
            except ValueError:
                print("Format incorrecte.")
        else:
            print("Bot is playing ...")
            is_max = board.turn == chess.WHITE

            score, best_move = minimax(board, depth, is_max)

            if best_move:
                print(f"Le bot joue : {best_move}")
                print(f"score : {score}")
                board.push(best_move)

            else:
                print("Aucun coup")
                break
    print("Fin de partie :", board.result())


if __name__ == "__main__":
    main()
