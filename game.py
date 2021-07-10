from piece import Piece, GraphicalPiece


class GraphicalBoard:
    def __init__(self, rows, cols, display_variables):
        self.rows = rows
        self.cols = cols
        self.display_variables = display_variables

        self.graphicalboard = [[0 for x in range(8)] for _ in range(rows)]

    def draw(self, gameDisplay):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.graphicalboard[i][j] != 0 and self.graphicalboard[i][j].getType() != 0:
                    self.graphicalboard[i][j].draw(gameDisplay)

    def importBoard(self, board):
        i = 0
        while i < 64:
            if board.getPiece(i) != 0:
                graphicalPiece = GraphicalPiece(board.getPiece(i), i, self.display_variables)
            else:
                graphicalPiece = GraphicalPiece(0, i, self.display_variables)
            self.graphicalboard[graphicalPiece.row][graphicalPiece.col] = graphicalPiece
            i += 1

    def getPiece(self, row, col):
        return self.graphicalboard[row][col]

    def setPiece(self, graphicalPiece, row, col):
        self.graphicalboard[row][col] = graphicalPiece


class Board:
    def __init__(self):
        self.b = [0] * 64
        self.dense_b = {}

    def importBoard(self, board):
        for i in range(8):
            for j in range(8):
                index = i * 8 + j
                self.b[index] = board.getPiece(i, j)
        return self.b

    def getPiece(self, index):
        return self.b[index]

    def setPiece(self, piece, index):
        self.b[index] = piece

    def importFEN(self, fenString):
        fenString = fenString
        fenParts = fenString.split(" ")

        boardIndex = 0
        for element in fenParts[0]:
            if element == '/':
                pass
            elif element.isdigit():
                boardIndex = boardIndex + int(element)
            else:
                color = 16  # black color
                if element.isupper():
                    color = 8  # white color
                if element.lower() == 'p':
                    self.b[boardIndex] = color + 1
                elif element.lower() == 'r':
                    self.b[boardIndex] = color + 2
                elif element.lower() == 'n':
                    self.b[boardIndex] = color + 3
                elif element.lower() == 'b':
                    self.b[boardIndex] = color + 4
                elif element.lower() == 'q':
                    self.b[boardIndex] = color + 5
                elif element.lower() == 'k':
                    self.b[boardIndex] = color + 6
                boardIndex += 1
        return self.b

    def generateDenseBoard(self):
        self.dense_b = {}
        index = 0
        for element in self.b:
            if self.b[index] != 0:
                self.dense_b[index] = self.b[index]
            index += 1
        return self.dense_b
