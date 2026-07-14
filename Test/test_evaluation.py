import unittest

import chess

from MiniMax.evaluation import evaluate_board


class TestEvaluation(unittest.TestCase):
    def test_init_position(self):
        board = chess.Board()
        score = evaluate_board(board)
        self.assertEqual(score, 0)

    def test_white_beginning(self):
        board = chess.Board()
        board.push_san("d4")
        score = evaluate_board(board)
        self.assertEqual(score, 40)


if __name__ == "__main__":
    unittest.main()
