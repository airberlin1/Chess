from colors import WHITE, BLACK
KNIGHT_MOVES = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
KING_MOVES = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
CHESS_BOARD_SIZE = 8
VERTICAL = 1
HORIZONTAL = 2
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class Piece:
    def __init__(self, start_pos, white):
        self.pos = list(start_pos)
        self.color = WHITE if white else BLACK

    def move(self, new_pos):
        self.pos = list(new_pos)

    def eliminateInvalidMoves(self, moves):
        moves = [move for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
        # TODO eliminate invalid moves due to check
        return moves

    def getMovesStraight(self, direction):
        moves = []
        num_range = []

        if direction[0] == VERTICAL:
            if direction[1] == UP:
                num_range = range(self.pos[0] - 1, -1, -1)
            elif direction[1] == DOWN:
                num_range = range(self.pos[0] + 1, CHESS_BOARD_SIZE)

            for i in num_range:
                if board.board[i][self.pos[1]] is not None:
                    piece = board.board[i][self.pos[1]]
                    if piece.color == self.color:
                        break
                    else:
                        moves.append([i, self.pos[1]])
                        break
                moves.append([i, self.pos[1]])

        elif direction == HORIZONTAL:
            if direction[1] == LEFT:
                num_range = range(self.pos[1] - 1, -1, -1)
            elif direction[1] == RIGHT:
                num_range = range(self.pos[1] + 1, CHESS_BOARD_SIZE)

            for i in num_range:
                if board.board[self.pos[0]][i] is not None:
                    piece = board.board[self.pos[0]][i]
                    if piece.color == self.color:
                        break
                    else:
                        moves.append([self.pos[0], i])
                        break
                moves.append([self.pos[0], i])

        return moves

    def getAllMovesStraight(self):
        moves_down = self.getMovesStraight((VERTICAL, DOWN))
        moves_up = self.getMovesStraight((VERTICAL, UP))
        moves_left = self.getMovesStraight((HORIZONTAL, LEFT))
        moves_right = self.getMovesStraight((HORIZONTAL, RIGHT))
        moves = moves_down + moves_up + moves_left + moves_right
        return moves

    def getMovesDiagonal(self, direction):
        moves = []
        return moves

    def getAllMovesDiagonal(self):
        moves_up_right = self.getMovesDiagonal((UP, RIGHT))
        moves_up_left = self.getMovesDiagonal((UP, LEFT))
        moves_down_left = self.getMovesDiagonal((DOWN, LEFT))
        moves_down_right = self.getMovesDiagonal((DOWN, RIGHT))
        moves = moves_up_right + moves_up_left + moves_down_left + moves_down_right
        return moves


class Pawn(Piece):
    def __repr__(self):
        return f"Pawn at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        pass


class Rook(Piece):
    def __repr__(self):
        return f"Rook at ({self.pos[0]}, {self.pos[1]})"
    
    def getPossibleMoves(self):
        moves = self.getAllMovesStraight()
        return self.eliminateInvalidMoves(moves)


class Knight(Piece):
    def __repr__(self):
        return f"Knight at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        moves = [[self.pos[i] + move[i] for i in range(2)] for move in KNIGHT_MOVES]
        return self.eliminateInvalidMoves(moves)


class Bishop(Piece):
    def __repr__(self):
        return f"Bishop at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        moves = self.getAllMovesDiagonal()
        return self.eliminateInvalidMoves(moves)


class Queen(Piece):
    def __repr__(self):
        return f"Queen at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        straight_moves = self.getAllMovesStraight()
        diagonal_moves = self.getAllMovesDiagonal()
        moves = diagonal_moves + straight_moves
        return self.eliminateInvalidMoves(moves)


class King(Piece):
    def __repr__(self):
        return f"King at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        moves = [[self.pos[i] + move[i] for i in range(2)] for move in KING_MOVES]
        return self.eliminateInvalidMoves(moves)


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
            [Pawn([1, i], white) for i in range(CHESS_BOARD_SIZE)],
            [None for _ in range(CHESS_BOARD_SIZE)],
            [None for _ in range(CHESS_BOARD_SIZE)],
            [None for _ in range(CHESS_BOARD_SIZE)],
            [None for _ in range(CHESS_BOARD_SIZE)],
            [Pawn([6, i], bool(1-white)) for i in range(CHESS_BOARD_SIZE)],
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
    if list(new_pos) not in piece.getPossibleMoves():
        return 2
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
    print(board.board[0][1].getPossibleMoves())
