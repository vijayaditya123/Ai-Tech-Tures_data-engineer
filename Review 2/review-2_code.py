from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def can_move(self, board, start, end):
        pass

    @abstractmethod
    def symbol(self):
        pass


class Pawn(Piece):
    def can_move(self, board, start, end):
        r1, c1 = start
        r2, c2 = end
        direction = -1 if self.color == "white" else 1

        if c1 == c2 and board.is_empty(end):
            if r2 - r1 == direction:
                return True
        return False

    def symbol(self):
        return "P" if self.color == "white" else "p"


class Rook(Piece):
    def can_move(self, board, start, end):
        r1, c1 = start
        r2, c2 = end
        if r1 == r2 or c1 == c2:
            return board.clear_path(start, end)
        return False

    def symbol(self):
        if self.color == "white":
            return "R" 
        else:
            return "r"


class Knight(Piece):
    def can_move(self, board, start, end):
        r1, c1 = start
        r2, c2 = end
        return (abs(r1 - r2), abs(c1 - c2)) in [(2, 1), (1, 2)]

    def symbol(self):
        if self.color == "white":
          return "N" 
        else:
            return "n"


class Bishop(Piece):
    def can_move(self, board, start, end):
        r1, c1 = start
        r2, c2 = end
        if abs(r1 - r2) == abs(c1 - c2):
            return board.clear_path(start, end)
        return False

    def symbol(self):
        return "B" if self.color == "white" else "b"


class Queen(Piece):
    def can_move(self, board, start, end):
        r1, c1 = start
        r2, c2 = end
        if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
            return board.clear_path(start, end)
        return False

    def symbol(self):
        return "Q" if self.color == "white" else "q"


class King(Piece):
    def can_move(self, board, start, end):
        r1, c1 = start
        r2, c2 = end
        return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

    def symbol(self):
        return "K" if self.color == "white" else "k"




class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup()

    def setup(self):
        for c in range(8):
            self.grid[1][c] = Pawn("black")
            self.grid[6][c] = Pawn("white")

        self.grid[0][0] = self.grid[0][7] = Rook("black")
        self.grid[7][0] = self.grid[7][7] = Rook("white")

        self.grid[0][1] = self.grid[0][6] = Knight("black")
        self.grid[7][1] = self.grid[7][6] = Knight("white")

        self.grid[0][2] = self.grid[0][5] = Bishop("black")
        self.grid[7][2] = self.grid[7][5] = Bishop("white")

        self.grid[0][3] = Queen("black")
        self.grid[7][3] = Queen("white")

        self.grid[0][4] = King("black")
        self.grid[7][4] = King("white")

    def display(self):
        print("\n  0 1 2 3 4 5 6 7")
        for r in range(8):
            print(r, end=" ")
            for c in range(8):
                piece = self.grid[r][c]
                print(piece.symbol() if piece else ".", end=" ")
            print()
        print()

    def is_empty(self, pos):
        r, c = pos
        return self.grid[r][c] is None

    def clear_path(self, start, end):
        r1, c1 = start
        r2, c2 = end
        dr = (r2 - r1) and (1 if r2 > r1 else -1)
        dc = (c2 - c1) and (1 if c2 > c1 else -1)

        r, c = r1 + dr, c1 + dc
        while (r, c) != (r2, c2):
            if self.grid[r][c]:
                return False
            r += dr
            c += dc
        return True

    def move_piece(self, start, end):
        piece = self.grid[start[0]][start[1]]
        target = self.grid[end[0]][end[1]]

        if target and target.color == piece.color:
            return False

        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        return True


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color



class Game:
    def __init__(self):
        self.board = Board()
        self.players = [
            Player("Player 1", "white"),
            Player("Player 2", "black")
        ]
        self.turn = 0

    def current_player(self):
        return self.players[self.turn % 2]

    def play(self):
        while True:
            self.board.display()
            player = self.current_player()
            print(f"{player.name} ({player.color}) turn")

            try:
                r1, c1, r2, c2 = map(int, input("Enter move (r1 c1 r2 c2): ").split())
            except:
                print("Invalid input")
                continue

            piece = self.board.grid[r1][c1]
            if not piece:
                print("No piece at source")
                continue
            if piece.color != player.color:
                print("Cannot move opponent piece")
                continue
            if not piece.can_move(self.board, (r1, c1), (r2, c2)):
                print("Illegal move")
                continue
            if not self.board.move_piece((r1, c1), (r2, c2)):
                print("Move blocked")
                continue

            self.turn += 1


if __name__ == "__main__":
    game = Game()
    game.play()
