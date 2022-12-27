import chess


def main():
    prev_pos = (0, 4)
    new_pos = (4, 5)
    chess.movePiece(prev_pos, new_pos)
    chess.printBoard()


if __name__ == '__main__':
    main()
