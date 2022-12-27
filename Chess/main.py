import chess


def main():
    prev_pos = (0, 1)
    new_pos = [2, 0]
    chess.movePiece(prev_pos, new_pos)
    chess.printBoard()


if __name__ == '__main__':
    main()
