from copy import deepcopy
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
REGULAR_PAWN_MOVE = 1
TWO_FORWARD = 2


class Piece:
    def __init__(self, start_pos, white):
        self.pos = list(start_pos)
        self.color = WHITE if white else BLACK
        self.has_moved = False
        # this could possibly lead to problems when promoting in some chess variants,
        # however it won't in regular chess

    def move(self, new_pos):
        self.pos = list(new_pos)
        self.has_moved = True

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

        elif direction[0] == HORIZONTAL:
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
        if direction == (UP, RIGHT):
            change = (1, 1)
        elif direction == (UP, LEFT):
            change = (1, -1)
        elif direction == (DOWN, LEFT):
            change = (-1, -1)
        elif direction == (DOWN, RIGHT):
            change = (-1, 1)
        else:
            change = (CHESS_BOARD_SIZE, CHESS_BOARD_SIZE)
        for i in range(1, CHESS_BOARD_SIZE):
            if not 0 <= self.pos[0] + i * change[0] < CHESS_BOARD_SIZE or not 0 <= self.pos[1] + i * change[1] < CHESS_BOARD_SIZE:
                break
            if board.board[self.pos[0] + i * change[0]][self.pos[1] + i * change[1]] is not None:
                if board.board[self.pos[0] + i * change[0]][self.pos[1] + i * change[1]].color == self.color:
                    break
                else:
                    moves.append([self.pos[0] + i * change[0], self.pos[1] + i * change[1]])
                    break
            moves.append([self.pos[0] + i * change[0], self.pos[1] + i * change[1]])
        return moves

    def getAllMovesDiagonal(self):
        moves_up_right = self.getMovesDiagonal((UP, RIGHT))
        moves_up_left = self.getMovesDiagonal((UP, LEFT))
        moves_down_left = self.getMovesDiagonal((DOWN, LEFT))
        moves_down_right = self.getMovesDiagonal((DOWN, RIGHT))
        moves = moves_up_right + moves_up_left + moves_down_left + moves_down_right
        return moves


class Pawn(Piece):
    def __init__(self, start_pos, white):
        super().__init__(start_pos, white)
        self.last_move = REGULAR_PAWN_MOVE

    def move(self, new_pos):
        if new_pos[1] - self.pos[1] == 2 or new_pos[1] - self.pos[1] == -2:
            self.last_move = TWO_FORWARD
        else:
            self.last_move = REGULAR_PAWN_MOVE
        super().move(new_pos)

    def __repr__(self):
        return f"Pawn at ({self.pos[0]}, {self.pos[1]})"

    # noinspection PyUnresolvedReferences
    def getPossibleMoves(self, check_valid):
        moves = []

        if self.color == WHITE:
            y_change = 1
        elif self.color == BLACK:
            y_change = -1
        else:
            print("wtf are you even doing to your colors in Pawn.getPossibleMoves")
            return 1

        # going forward
        if board.board[self.pos[0] + y_change][self.pos[1]] is None:
            moves.append([self.pos[0] + y_change, self.pos[1]])
            if not self.has_moved:  # is allowed to move twice when on the starting row
                if board.board[self.pos[0] + (2 * y_change)][self.pos[1]] is None:
                    moves.append([self.pos[0] + (2 * y_change), self.pos[1]])

        # taking something
        for i in (-1, 1):
            if board.board[self.pos[0] + y_change][self.pos[1] + i] is not None:
                if board.board[self.pos[0] + y_change][self.pos[1] + i].color != self.color:
                    moves.append([self.pos[0] + y_change, self.pos[1] + i])

        # en passant
        for i in (-1, 1):
            if board.board[self.pos[0]][self.pos[1] + i] is not None:
                if type(board.board[self.pos[0]][self.pos[1] + i]) == type(self):
                    if board.board[self.pos[0]][self.pos[1] + i].last_move == TWO_FORWARD:
                        moves.append([self.pos[0] + y_change, self.pos[1] + i])

        # promotion is not treated as a special move here, but instead handled in the movePiece function
        return eliminateInvalidMoves(self.pos, moves, check_valid)


class Rook(Piece):
    def __repr__(self):
        return f"Rook at ({self.pos[0]}, {self.pos[1]})"
    
    def getPossibleMoves(self, check_valid):
        moves = self.getAllMovesStraight()
        return eliminateInvalidMoves(self.pos, moves, check_valid)


class Knight(Piece):
    def __repr__(self):
        return f"Knight at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self, check_valid):
        moves = [[self.pos[i] + move[i] for i in range(2)] for move in KNIGHT_MOVES]
        return eliminateInvalidMoves(self.pos, moves, check_valid)


class Bishop(Piece):
    def __repr__(self):
        return f"Bishop at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self, check_valid):
        moves = self.getAllMovesDiagonal()
        return eliminateInvalidMoves(self.pos, moves, check_valid)


class Queen(Piece):
    def __repr__(self):
        return f"Queen at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self, check_valid):
        straight_moves = self.getAllMovesStraight()
        diagonal_moves = self.getAllMovesDiagonal()
        moves = diagonal_moves + straight_moves
        return eliminateInvalidMoves(self.pos, moves, check_valid)


class King(Piece):
    def __repr__(self):
        return f"King at ({self.pos[0]}, {self.pos[1]})"

    def getPossibleMoves(self):
        moves = [[self.pos[i] + move[i] for i in range(2)] for move in KING_MOVES]

        # castling
        if not self.has_moved:
            if type(board.board[self.pos[0]][0]) == type(Rook):
                if not board.board[self.pos[0]][0].has_moved:
                    count = 0
                    for i in range(1, self.pos[1]):
                        if board.board[self.pos[0]][i] is None:
                            count += 1
                    if count == self.pos[1] - 1:
                        moves.append([self.pos[0], self.pos[1] - 2])
            if type(board.board[self.pos[0]][CHESS_BOARD_SIZE - 1]) == type(Rook):
                if not board.board[self.pos[0]][CHESS_BOARD_SIZE - 1].has_moved:
                    count = 0
                    for i in range(self.pos[1] + 1, CHESS_BOARD_SIZE - 1):
                        if board.board[self.pos[0]][i] is None:
                            count += 1
                    if count == CHESS_BOARD_SIZE - 1 - self.pos[1] - 1:
                        moves.append([self.pos[0], self.pos[1] - 2])

        return eliminateInvalidMoves(self.pos, moves)


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


def inCheck(board_to_be_checked):

    pos = [[0, 0], [0, 0]]
    pos_ind = 0

    for row in board_to_be_checked:
        for piece in row:
            if type(piece) == type(King):
                pos[pos_ind] = piece.pos
                pos_ind += 1

    for row in board_to_be_checked:
        for piece in row:
            if piece is not None:
                if piece.pos in pos:
                    return True

    return False


board = Board()


def eliminateInvalidMoves(pos, moves, check_valid):
    moves = [move for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
    if check_valid:
        return moves
    valid_moves = []
    for move in moves:
        pass
    # TODO eliminate invalid moves due to check
    return valid_moves


def movePiece(prev_pos, new_pos, check_valid=False, changed_board=board):
    # TODO castling
    # TODO en passant
    # TODO promotion
    if changed_board.board[prev_pos[0]][prev_pos[1]] is None:
        return 1
    piece = changed_board.board[prev_pos[0]][prev_pos[1]]
    if list(new_pos) not in piece.getPossibleMoves(check_valid):
        return 2
    changed_board.board[prev_pos[0]][prev_pos[1]] = None
    if changed_board.board[new_pos[0]][new_pos[1]] is not None:
        changed_board.captured.append(changed_board.board[new_pos[0]][new_pos[1]])
    changed_board.board[new_pos[0]][new_pos[1]] = piece
    piece.move(new_pos)


def printBoard():
    for b in board.board:
        print(b)


def resetBoard():
    global board
    board = Board()


if __name__ == '__main__':
    pass
