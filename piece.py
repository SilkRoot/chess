import pygame
import os
import math


def getBoardIndex(col, row):
    index = row * 8 + col
    return index


class GraphicalPiece:
    def __init__(self, piece, fieldIndex, display_variables):
        self.row = math.floor(fieldIndex / 8)
        self.col = fieldIndex - self.row * 8
        self.fieldIndex = fieldIndex
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

    def getFieldIndex(self):
        return self.fieldIndex


def getRookMoves():
    movingDirections = [
        8,  # runter
        -8,  # hoch
        -1,  # links
        1  # rechts
    ]
    maxDistance = 8
    return maxDistance, movingDirections


def getKnightMoves():
    movingDirections = [
        -17,
        -15,
        -10,
        -6,
        6,
        10,
        15,
        17
    ]
    maxDistance = 1
    return maxDistance, movingDirections


def getBishopMoves():
    movingDirections = [
        7,  # linksrunter
        -7,  # rechtshoch
        9,  # rechtsrunter
        -9  # linkshoch
    ]
    maxDistance = 8
    return maxDistance, movingDirections


def getPawnMoves(index, color):
    maxDistance = 1
    if color == 8:
        if 48 <= index <= 55: # stratingposition white
            maxDistance = 2
        movingDirections = [
            -8  # hoch
        ]
    else:
        if 8 <= index <= 15:  # stratingposition black
            maxDistance = 2
        movingDirections = [
            8  # runter
        ]
    # deal with capture piece
    return maxDistance, movingDirections


def getQueenMoves():
    movingDirections = [
        8,  # runter
        -8,  # hoch
        -1,  # links
        1,  # rechts
        7,  # linksrunter
        -7,  # rechtshoch
        9,  # rechtsrunter
        -9  # linkshoch
    ]
    maxDistance = 8
    return maxDistance, movingDirections


def getPossibleMoves(index, denseBoard):
    possibleFields = []
    pieceValue = denseBoard[index]
    piece = Piece(pieceValue)
    pieceType = piece.getIntPieceType()
    pieceColor = piece.getIntPieceColor()
    maxDistance = 0
    movingDirections = []

    if pieceType == 1:
        maxDistance, movingDirections = getPawnMoves(index, pieceColor)
    elif pieceType == 2:
        maxDistance, movingDirections = getRookMoves()
    elif pieceType == 3:
        maxDistance, movingDirections = getKnightMoves()
    elif pieceType == 4:
        maxDistance, movingDirections = getBishopMoves()
    elif pieceType == 5:
        maxDistance, movingDirections = getQueenMoves()
    elif pieceType == 6:
        maxDistance, movingDirections = getKingMoves(True)

    for direction in movingDirections:
        startField = index
        i = 0
        while i < maxDistance:
            targetField = startField + direction
            # piece on targetField
            if denseBoard.has_key(targetField):
                oppositePiece = denseBoard[targetField].getPieceType()
                if oppositePiece[0] != color: #different color
                    possibleFields.append(targetField)
                else: # piece with same color
                    break
            # edge of the board
            elif 1==2:
                pass
            # free field
            else:
                possibleFields.append(targetField)
            startField = targetField

    return possibleFields


def getKingMoves(moved):
    movingDirections = [
        8,  # runter
        -8,  # hoch
        -1,  # links
        1,  # rechts
        7,  # linksrunter
        -7,  # rechtshoch
        9,  # rechtsrunter
        -9  # linkshoch
    ]
    if moved is False:
        if checkCastle("kingside"):
            movingDirections.append(2)
        if checkCastle("queenside"):
            movingDirections.append(-3)
    maxDistance = 1
    return maxDistance, movingDirections

def checkCastle(side):
    return False

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
        tempPiece = self.piece
        if tempPiece > 15:
            tempPiece -= 16
        else:
            tempPiece -= 8
        return tempPiece

    def getIntPieceColor(self):
        if self.piece > 15:
            return 16
        else:
            return 8




