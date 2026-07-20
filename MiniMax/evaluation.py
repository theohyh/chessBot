import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

PAWN_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_PST = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_PST_MIDDLEGAME = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

KING_PST_ENDGAME = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]


def evaluate_board(board: chess.Board, dict={}) -> int:
    if board.fen() in dict:
        return dict[board.fen()]

    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999

    score = 0

    for square, piece in board.piece_map().items():
        if piece is not None:
            rank = chess.square_rank(square)
            col = chess.square_file(square)
            index = (7 - rank) * 8 + col
            score += (
                PIECE_VALUES[piece.piece_type]
                if piece.color == chess.WHITE
                else -PIECE_VALUES[piece.piece_type]
            )
            if piece.piece_type == chess.PAWN:
                score += (
                    PAWN_PST[index]
                    if piece.color == chess.WHITE
                    else -PAWN_PST[chess.square_mirror(index)]
                )
            if piece.piece_type == chess.KNIGHT:
                score += (
                    KNIGHT_PST[index]
                    if piece.color == chess.WHITE
                    else -KNIGHT_PST[chess.square_mirror(index)]
                )
            if piece.piece_type == chess.BISHOP:
                score += (
                    BISHOP_PST[index]
                    if piece.color == chess.WHITE
                    else -BISHOP_PST[chess.square_mirror(index)]
                )
            if piece.piece_type == chess.ROOK:
                score += (
                    ROOK_PST[index]
                    if piece.color == chess.WHITE
                    else -ROOK_PST[chess.square_mirror(index)]
                )
            if piece.piece_type == chess.QUEEN:
                score += (
                    QUEEN_PST[index]
                    if piece.color == chess.WHITE
                    else -QUEEN_PST[chess.square_mirror(index)]
                )
            if piece.piece_type == chess.KING and len(board.pieces(chess.QUEEN,True))==0 and len(board.pieces(chess.QUEEN,False))==0:
                score += (
                    KING_PST_ENDGAME[index]
                    if piece.color == chess.WHITE
                    else -KING_PST_ENDGAME[chess.square_mirror(index)]
                )
            elif piece.piece_type == chess.KING:
                score += (
                    KING_PST_MIDDLEGAME[index]
                    if piece.color == chess.WHITE
                    else -KING_PST_MIDDLEGAME[chess.square_mirror(index)]
                )
    dict[board.fen()] = score
    return score
