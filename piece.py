import pygame
import os
import math


def getBoardIndex(col, row):
    index = row * 8 + col
    return (index)


class GraphicalPiece:
    def __init__(self, piece, fieldIndex, display_variables):
        self.row = math.floor(fieldIndex / 8)
        self.col = fieldIndex - self.row * 8
        self.color, self.type = Piece(piece).getPieceType()
        self.intType = Piece(piece).getIntPieceType()
        self.fieldsize = display_variables.get("fieldsize")
        self.board_offset_x = display_variables.get("board_offset_x")
        self.board_offset_y = display_variables.get("board_offset_y")

    def draw(self, gameDisplay):
        if self.color != 'none':
            drawThis = pygame.transform.scale(
                pygame.image.load(os.path.join("img", self.color + "_" + self.type + ".png")),
                (self.fieldsize, self.fieldsize))

            x = self.col * self.fieldsize + self.board_offset_x
            y = self.row * self.fieldsize + self.board_offset_y

            gameDisplay.blit(drawThis, (x, y))

    def getImageToDraw(self):
        if self.color != 'none':
            drawThis = pygame.transform.scale(
                pygame.image.load(os.path.join("img", self.color + "_" + self.type + ".png")),
                (self.fieldsize, self.fieldsize))
        return drawThis

    def getType(self):
        return self.type

    def getIntType(self):
        return self.intType


class Piece:
    def __init__(self, piece):
        self.piece = piece

    def getPieceType(self):
        numberRepresentation = {
            "none": 0,
            "pawn": 1,
            "rook": 2,
            "knight": 3,
            "bishop": 4,
            "queen": 5,
            "king": 6
            # "white": 8,
            # "black": 16
        }
        tempPiece = self.piece
        if tempPiece > 15:
            color = 'black'
            tempPiece -= 16
        elif tempPiece == 0:
            color = "none"
        else:
            color = 'white'
            tempPiece -= 8

        for descr, num in numberRepresentation.items():
            if num == tempPiece:
                type = descr
                break
        return color, type

    def getIntPieceType(self):
        return self.piece
