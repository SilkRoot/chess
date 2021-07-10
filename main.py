import pygame
import math
from game import Board, GraphicalBoard
from piece import Piece, GraphicalPiece

pygame.init()

display_variables = {
    "display_width": 1200,
    "display_height": 1200,
    "fieldsize": 100,
    "board_offset_x": 100,
    "board_offset_y": 100
}

BOARD_POS = (10, 10)

gameDisplay = pygame.display.set_mode((display_variables.get("display_width"), display_variables.get("display_height")))
graphicalBoard = GraphicalBoard(8, 8, display_variables)
curBoard = Board()
curBoard.importFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
graphicalBoard.importBoard(curBoard)

pygame.display.set_caption('Chess')

#boardImg = pygame.image.load('img/board.png')
#boardImg = pygame.transform.scale(boardImg, (8 * display_variables.get("fieldsize"), 8 * display_variables.get("fieldsize")))


def create_board_surf():
    board_surf = pygame.Surface((display_variables.get("fieldsize")*8, display_variables.get("fieldsize")*8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*display_variables.get("fieldsize"), y*display_variables.get("fieldsize"),
                               display_variables.get("fieldsize"), display_variables.get("fieldsize"))
            pygame.draw.rect(board_surf, pygame.Color((212, 140, 68) if dark else (252, 204, 156)), rect)
            dark = not dark
        dark = not dark
    return board_surf



def redrawGameWindow():
    global gameDisplay
    global graphicalBoard
    #gameDisplay.blit(boardImg, (display_variables.get("board_offset_x"), display_variables.get("board_offset_y")))
    graphicalBoard.draw(gameDisplay)
    pygame.display.update()


#def click(pos):
#    x = pos[0]
#    y = pos[1]
#
#    row = math.floor((y - display_variables.get("board_offset_y"))/display_variables.get("fieldsize"))
#    column = math.floor((x - display_variables.get("board_offset_x")) / display_variables.get("fieldsize"))
#
#    piecetype = graphicalBoard.get_piece(row, column).getType()
#    print(piecetype)


def get_square_under_mouse():
    pos = pygame.Vector2(pygame.mouse.get_pos())
    x = pos[0]
    y = pos[1]
   # print(f"Mouseposition: x={x} y={y}")
    if x < display_variables.get("board_offset_x") or y < display_variables.get("board_offset_y") or x > display_variables.get("board_offset_x") + display_variables.get("fieldsize") * 8 or y > display_variables.get("board_offset_y") + display_variables.get("fieldsize") * 8:
        return None, None
    col = math.floor((x - display_variables.get("board_offset_x")) / display_variables.get("fieldsize"))
    row = math.floor((y - display_variables.get("board_offset_y")) / display_variables.get("fieldsize"))
    #print(f"Mouse over col {col} and row {row}")
    return col, row


#def draw_pieces(screen, board, font):
#    for y in range(8):
#        for x in range(8):
#            piece = board[y][x]
#            if piece:
#                color, type = piece
#                s1 = font.render(type[0], True, pygame.Color(color))
#                s2 = font.render(type[0], True, pygame.Color('darkgrey'))
#                pos = pygame.Rect(display_variables.get("board_offset_x") + x * display_variables.get("fieldsize")+1,
#                                  display_variables.get("board_offset_y") + y * display_variables.get("fieldsize") + 1,
#                                  display_variables.get("fieldsize"), display_variables.get("fieldsize"))
#                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
#                screen.blit(s1, s1.get_rect(center=pos.center))

def draw_selector(screen, graphicalBoard, col, row):
    #print(f"There's a {graphicalBoard.getPiece(row, col).getType()} on row {row} and col {col}")
    rect = (display_variables.get("board_offset_x") + col * display_variables.get("fieldsize"),
            display_variables.get("board_offset_y") + row * display_variables.get("fieldsize"),
            display_variables.get("fieldsize"), display_variables.get("fieldsize"))
    if graphicalBoard.getPiece(row, col).getType() != 'none':
        pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
    else:
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, graphicalBoard, selected_piece, font):
    if selected_piece:
        col, row = get_square_under_mouse()
        if graphicalBoard.getPiece(row, col) != None:
            rect = (display_variables.get("board_offset_x") + col * display_variables.get("fieldsize"),
                display_variables.get("board_offset_y") + row * display_variables.get("fieldsize"),
                display_variables.get("fieldsize"), display_variables.get("fieldsize"))
            pygame.draw.rect(screen, (0, 0, 255, 50), rect, 2)

#        color, type = selected_piece[0]
#        print(color, type)
#        s1 = font.render(type[0], True, pygame.Color(color))
#        s2 = font.render(type[0], True, pygame.Color('darkgrey'))
        pos = pygame.Vector2(pygame.mouse.get_pos())

#        drawThis = graphicalBoard.getPiece(row, col).getImageToDraw()

#        screen.blit(drawThis, s2.get_rect(center=pos + (1, 1)))
#        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(display_variables.get("board_offset_x") + selected_piece[1] * display_variables.get("fieldsize"),
                                    display_variables.get("board_offset_y") + selected_piece[2] * display_variables.get("fieldsize"),
                                    display_variables.get("fieldsize"), display_variables.get("fieldsize"))
        pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return (col, row)


def main():
    clock = pygame.time.Clock()
    board_surf = create_board_surf()

    font = pygame.font.SysFont('', 32)
    selected_piece = None
    drop_pos = None

    while True:
        redrawGameWindow()
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                return

        col, row = get_square_under_mouse()

        if row != None:
            rect = (display_variables.get("board_offset_x") + col * display_variables.get("fieldsize"),
                    display_variables.get("board_offset_y") + row * display_variables.get("fieldsize"),
                    display_variables.get("fieldsize"), display_variables.get("fieldsize"))
            pygame.draw.rect(gameDisplay, (255, 0, 0, 50), rect, 2)

        #if e.type == pygame.MOUSEBUTTONDOWN:
        #    pos = pygame.mouse.get_pos()
        #    click(pos)

        if e.type == pygame.MOUSEBUTTONDOWN:
            if graphicalBoard.getPiece(row, col) != None:
                selected_piece = graphicalBoard.getPiece(row, col), col, row
               # print(f"the following piece was selected: {selected_piece[0].getType()}")

        if e.type == pygame.MOUSEBUTTONUP:
            if drop_pos:
                tempGraphicalPiece, colOld, rowOld = selected_piece
                curBoard.setPiece(0, tempGraphicalPiece.getBoardIndex(colOld, rowOld))
                curBoard.setPiece(tempGraphicalPiece.getIntType(), tempGraphicalPiece.getBoardIndex(col, row))
                graphicalBoard.importBoard(curBoard)
                #graphicalBoard.setPiece(graphicalPiece = GraphicalPiece(0, i, display_variables), old_y, old_x)
                #new_x, new_y = drop_pos
                #print(graphicalBoard)
                #print(f"new position: {new_x}, {new_y}")
                #graphicalBoard.setPiece(tempGraphicalPiece, new_y, new_x)
                selected_piece = None
                drop_pos = None

        gameDisplay.fill(pygame.Color('grey'))
        gameDisplay.blit(board_surf, (display_variables.get("board_offset_x"), display_variables.get("board_offset_y")))

        #draw_pieces(gameDisplay, board, font)
        if row != None:
            draw_selector(gameDisplay, graphicalBoard, col, row)
        drop_pos = draw_drag(gameDisplay, graphicalBoard, selected_piece, font)

        clock.tick(60)



main()
pygame.quit()
quit()