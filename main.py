from time import sleep

import chess

from MiniMax.engine import minimax
from InputBot.input import inputMoves


def main():
    print("=" * 40)
    print("   DÉMARRAGE DU BOT D'ÉCHECS MINIMAX   ")
    print("=" * 40)

    board = chess.Board()
    human = chess.BLACK
    depth = 3

    while not board.is_game_over():
        print("=" * 40)
        if board.turn == human:
            """
            move_str = input("Votre Coup (ex: e2e4): ").strip()
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Coup invalide.")
            except ValueError:
                print("Format incorrecte.")
            """
            """ print("Bot 1 is playing ...")
            is_max = board.turn == chess.WHITE

            score, best_move = minimax(board, 3, is_max)

            if best_move:
                print(f"Le bot joue : {best_move}")
                print(f"score : {score}")
                board.push(best_move)

            else:
                print("Aucun coup")
                break """

            ok = input("Appuyez sur Entrée pour jouer votre coup : ")
            if ok.lower() != "":
                break
            i = inputMoves()
            if len(i) == 0:
                break
            else:
                print(f"Vous jouez : {i[0]}")
                move = chess.Move.from_uci(i[0])
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Coup invalide.")
                print(board)

        else:
            print("Bot 2 is playing ...")
            is_max = board.turn == chess.WHITE

            score, best_move = minimax(board, 3, is_max)

            if best_move:
                print(f"Le bot joue : {best_move}")
                print(f"score : {score}")
                board.push(best_move)
                print(board)
                input("Appuyez sur Entrée pour jouer votre coup : ")
                inputMoves()

            else:
                print("Aucun coup")
                break

    print("Fin de partie :", board.result())


if __name__ == "__main__":
    main()
