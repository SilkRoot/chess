import pygame
import math
from game import Board, GraphicalBoard
from piece import getBoardIndex, getPossibleMoves, Piece

pygame.init()

display_variables = {
    "display_width": 1200,
    "display_height": 1200,
    "fieldsize": 100,
    "board_offset_x": 100,
    "board_offset_y": 100
}

gameDisplay = pygame.display.set_mode((display_variables.get("display_width"), display_variables.get("display_height")))
graphicalBoard = GraphicalBoard(8, 8, display_variables)
curBoard = Board()
curBoard.importFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
graphicalBoard.importBoard(curBoard)

pygame.display.set_caption('Chess')


def create_board_surf():
    board_surf = pygame.Surface((display_variables.get("fieldsize") * 8, display_variables.get("fieldsize") * 8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * display_variables.get("fieldsize"), y * display_variables.get("fieldsize"),
                               display_variables.get("fieldsize"), display_variables.get("fieldsize"))
            pygame.draw.rect(board_surf, pygame.Color((212, 140, 68) if dark else (252, 204, 156)), rect)
            dark = not dark
        dark = not dark
    return board_surf


def redrawGameWindow():
    global gameDisplay
    global graphicalBoard
    graphicalBoard.draw(gameDisplay)
    pygame.display.update()


def get_square_under_mouse():
    pos = pygame.Vector2(pygame.mouse.get_pos())
    x = pos[0]
    y = pos[1]
    if x < display_variables.get("board_offset_x") \
            or y < display_variables.get("board_offset_y") \
            or x > display_variables.get("board_offset_x") + display_variables.get("fieldsize") * 8 \
            or y > display_variables.get("board_offset_y") + display_variables.get("fieldsize") * 8:
        return None, None
    col = math.floor((x - display_variables.get("board_offset_x")) / display_variables.get("fieldsize"))
    row = math.floor((y - display_variables.get("board_offset_y")) / display_variables.get("fieldsize"))
    return col, row


def draw_selector(screen, graphicalBoard, col, row):
    rect = (display_variables.get("board_offset_x") + col * display_variables.get("fieldsize"),
            display_variables.get("board_offset_y") + row * display_variables.get("fieldsize"),
            display_variables.get("fieldsize"), display_variables.get("fieldsize"))
    if graphicalBoard.getPiece(row, col).getType() != 'none':
        pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
    else:
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, graphicalBoard, selectedGraphicalPiece):
    if selectedGraphicalPiece:
        col, row = get_square_under_mouse()
        if graphicalBoard.getPiece(row, col) is not None:
            rect = (display_variables.get("board_offset_x") + col * display_variables.get("fieldsize"),
                    display_variables.get("board_offset_y") + row * display_variables.get("fieldsize"),
                    display_variables.get("fieldsize"), display_variables.get("fieldsize"))
            pygame.draw.rect(screen, (0, 0, 255, 50), rect, 2)
            #        s1 = font.render(type[0], True, pygame.Color(color))
            #        s2 = font.render(type[0], True, pygame.Color('darkgrey'))
            pos = pygame.Vector2(pygame.mouse.get_pos())
            #drawThis = graphicalBoard.getPiece(row, col).getImageToDraw()
            #screen.blit(drawThis, s2.get_rect(center=pos + (1, 1)))
            #        screen.blit(s1, s1.get_rect(center=pos))
            selected_rect = pygame.Rect(
            display_variables.get("board_offset_x") + selectedGraphicalPiece[1] * display_variables.get("fieldsize"),
            display_variables.get("board_offset_y") + selectedGraphicalPiece[2] * display_variables.get("fieldsize"),
            display_variables.get("fieldsize"), display_variables.get("fieldsize"))
        pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return col, row


def main():
    clock = pygame.time.Clock()
    board_surf = create_board_surf()

    selectedGraphicalPiece = None
    drop_pos = None

    while True:
        redrawGameWindow()
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                return

        col, row = get_square_under_mouse()

        if row is not None:
            rect = (display_variables.get("board_offset_x") + col * display_variables.get("fieldsize"),
                    display_variables.get("board_offset_y") + row * display_variables.get("fieldsize"),
                    display_variables.get("fieldsize"), display_variables.get("fieldsize"))
            pygame.draw.rect(gameDisplay, (255, 0, 0, 50), rect, 2)

        if e.type == pygame.MOUSEBUTTONDOWN:
            if graphicalBoard.getPiece(row, col) is not None:
                selectedGraphicalPiece = graphicalBoard.getPiece(row, col)
                selectedpiece = Piece(selectedGraphicalPiece.getIntType())
                getPossibleMoves(selectedGraphicalPiece.getFieldIndex(), curBoard.generateDenseBoard())

        if e.type == pygame.MOUSEBUTTONUP:
            if drop_pos:
                tempGraphicalPiece, colOld, rowOld = selectedGraphicalPiece
                curBoard.setPiece(0, getBoardIndex(colOld, rowOld))
                curBoard.setPiece(tempGraphicalPiece.getIntType(), getBoardIndex(col, row))
                graphicalBoard.importBoard(curBoard)
                selectedGraphicalPiece = None
                drop_pos = None

        gameDisplay.fill(pygame.Color('grey'))
        gameDisplay.blit(board_surf, (display_variables.get("board_offset_x"), display_variables.get("board_offset_y")))

        if row is not None:
            draw_selector(gameDisplay, graphicalBoard, col, row)
        drop_pos = draw_drag(gameDisplay, graphicalBoard, selectedGraphicalPiece)

        clock.tick(60)


main()
pygame.quit()
quit()
