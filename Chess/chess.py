from colors import *


class Piece:
    def __init__(self, start_pos, white):
        self.pos = start_pos
        self.color = WHITE if white else BLACK

    def move(self, new_pos):
        self.pos = new_pos


class Pawn(Piece):
    def __repr__(self):
        return f"Pawn at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        pass


class Rook(Piece):
    def __repr__(self):
        return f"Rook at ({self.pos[0]}, {self.pos[1]})"


class Knight(Piece):
    def __repr__(self):
        return f"Knight at ({self.pos[0]}, {self.pos[1]})"


class Bishop(Piece):
    def __repr__(self):
        return f"Bishop at ({self.pos[0]}, {self.pos[1]})"


class Queen(Piece):
    def __repr__(self):
        return f"Queen at ({self.pos[0]}, {self.pos[1]})"


class King(Piece):
    def __repr__(self):
        return f"King at ({self.pos[0]}, {self.pos[1]})"


class Board:
    def __init__(self):
        self.captured = []
        white = True
        self.board = [
            [
                Rook([0, 0], white), Knight([0, 1], white), Bishop([0, 2], white),
                Queen([0, 3], white), King([0, 4], white), Bishop([0, 5], white),
                Knight([0, 6], white), Rook([0, 7], white)
            ],
            [Pawn([1, i], white) for i in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn([6, i], bool(1-white)) for i in range(8)],
            [
                Rook([7, 0], bool(1-white)), Knight([7, 1], bool(1-white)), Bishop([7, 2], bool(1-white)),
                Queen([7, 3], bool(1-white)), King([7, 4], bool(1-white)), Bishop([7, 5], bool(1-white)),
                Knight([7, 6], bool(1-white)), Rook([7, 7], bool(1-white))
            ]
        ]


board = Board()


def movePiece(prev_pos, new_pos):
    if board.board[prev_pos[0]][prev_pos[1]] is None:
        return 1
    piece = board.board[prev_pos[0]][prev_pos[1]]
    board.board[prev_pos[0]][prev_pos[1]] = None
    if board.board[new_pos[0]][new_pos[1]] is not None:
        board.captured.append(board.board[new_pos[0]][new_pos[1]])
    board.board[new_pos[0]][new_pos[1]] = piece
    piece.move(new_pos)


def printBoard():
    for b in board.board:
        print(b)


def resetBoard():
    global board
    board = Board()


if __name__ == '__main__':
    printBoard()
