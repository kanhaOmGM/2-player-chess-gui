from chess_engine import GameState, Move
import pygame as p
import time


p.init()
width = height = 480
DIMENSIONS = 8
sq_size = height // DIMENSIONS
max_fps = 15
screen = p.display.set_mode((width, height))
images = {}
clock = p.time.Clock()
gs = GameState()

CLOCK_WIDTH = 150
CLOCK_HEIGHT = 60
clock_font = None  # Will be initialized in main()

# Clock times in seconds (10 minutes each)
white_time = 600
black_time = 600
last_move_time = None
clock_running = False



def draw_clock(screen, white_time, black_time, white_to_move):
    """
    Draw chess clocks for both players. Chess.com style
    """
    global clock_font
    
    # Position clocks on the right side of the board
    white_clock_rect = p.Rect(width + 10, height - CLOCK_HEIGHT - 10, CLOCK_WIDTH, CLOCK_HEIGHT)
    black_clock_rect = p.Rect(width + 10, 10, CLOCK_WIDTH, CLOCK_HEIGHT)
    
    # Determine which clock is active
    white_active = white_to_move and clock_running
    black_active = not white_to_move and clock_running
    
    # Draw black clock (top)
    black_bg_color = p.Color('darkgreen') if black_active else p.Color('gray30')
    p.draw.rect(screen, black_bg_color, black_clock_rect)
    p.draw.rect(screen, p.Color('white'), black_clock_rect, 3)
    
    # Format and draw black time
    black_mins = int(black_time // 60)
    black_secs = int(black_time % 60)
    black_text = clock_font.render(f"{black_mins}:{black_secs:02d}", True, p.Color('white'))
    black_text_rect = black_text.get_rect(center=black_clock_rect.center)
    screen.blit(black_text, black_text_rect)
    
    # Draw "BLACK" label
    label_font = p.font.SysFont("Arial", 16, False, False)
    black_label = label_font.render("BLACK", True, p.Color('lightgray'))
    screen.blit(black_label, (white_clock_rect.x + 5, black_clock_rect.y + 5))
    
    # Draw white clock (bottom)
    white_bg_color = p.Color('darkgreen') if white_active else p.Color('gray30')
    p.draw.rect(screen, white_bg_color, white_clock_rect)
    p.draw.rect(screen, p.Color('white'), white_clock_rect, 3)
    
    # Format and draw white time
    white_mins = int(white_time // 60)
    white_secs = int(white_time % 60)
    white_text = clock_font.render(f"{white_mins}:{white_secs:02d}", True, p.Color('white'))
    white_text_rect = white_text.get_rect(center=white_clock_rect.center)
    screen.blit(white_text, white_text_rect)
    
    # Draw "WHITE" label
    white_label = label_font.render("WHITE", True, p.Color('lightgray'))
    screen.blit(white_label, (white_clock_rect.x + 5, white_clock_rect.y + 5))
    
    # Draw time warning if below 1 minute
    if white_time < 60 and white_active:
        p.draw.rect(screen, p.Color('red'), white_clock_rect, 5)
    if black_time < 60 and black_active:
        p.draw.rect(screen, p.Color('red'), black_clock_rect, 5)




def choose_promotion(screen, color):    

    # Piece Icon
    choices = ["q", "r", "b", "n"]
    piece_rects = []
    for i, piece in enumerate(choices):
        #size
        x = width // 2 - 100 + i * 60
        y = height // 2 - 30
        #image icon 
        img = images[color + piece]
        #creating icon
        rect = p.Rect(x, y, sq_size, sq_size)
        #inserting the piece into list
        piece_rects.append((rect, piece))

        p.draw.rect(screen, p.Color("gray"), rect)
        #inserting image
        screen.blit(img, (x, y))
    
    p.display.flip()

    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                for rect, piece in piece_rects:
                    if rect.collidepoint(pos):
                        # Return "q", "r", "b", or "n"
                        return piece  


def load_images():
    pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]
    for piece in pieces:
        images[piece] = p.transform.scale(
            p.image.load("chess-engine/pieces/bases/" + piece + ".png"), (sq_size, sq_size)  
        )


def draw_board(screen):
    colors = [p.Color("white"), p.Color("brown")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, (c * sq_size, r * sq_size, sq_size, sq_size))


def draw_pieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], (c * sq_size, r * sq_size))


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def main():
    global white_time, black_time, last_move_time, clock_running, clock_font, gs
    
    set_of_move = 0
    move_made = False
    
    # Initialize clock font
    clock_font = p.font.SysFont("Arial", 32, True, False)
    
    load_images()
    running = True

    selected_sq = ()
    player_clicks = []
    valid_moves = gs.get_valid_moves()

    while running:
        
        # Update clock
        if clock_running and last_move_time is not None:
            current_time = time.time()
            elapsed = current_time - last_move_time
            last_move_time = current_time
            
            if gs.white_to_move:
                white_time -= elapsed
                if white_time <= 0:
                    white_time = 0
                    clock_running = False
                    print("\nBlack wins on time!")
            else:
                black_time -= elapsed
                if black_time <= 0:
                    black_time = 0
                    clock_running = False
                    print("\nWhite wins on time!")
        
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            
            # Mouse click handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                
                # Only process clicks on the board (not on clock area)
                if location[0] < width:
                    col = location[0] // sq_size
                    row = location[1] // sq_size

                    # Square selected
                    if selected_sq == (row, col):
                        selected_sq = ()
                        player_clicks = []
                    else:
                        selected_sq = (row, col)
                        player_clicks.append(selected_sq)

                    # When start and destination squares been selected
                    if len(player_clicks) == 2:
                        move = Move(player_clicks[0], player_clicks[1], gs.board)
                        
                        for i in valid_moves:
                            if move == i:
                                # Start clock on first move
                                if last_move_time is None:
                                    last_move_time = time.time()
                                    clock_running = True
                                
                                animate_move(screen, gs.board, i, clock)
                                move_made = True
                                gs.make_move(i)
                                print(i.get_chess_notation(), end="   ")
                                set_of_move += 1

                                # Pawn promotion
                                if i.is_pawn_promotion:
                                    piece_choice = choose_promotion(screen, i.piece_moved[0])
                                    gs.board[i.end_r][i.end_c] = i.piece_moved[0] + piece_choice
                                
                                if set_of_move == 2:
                                    print()
                                    set_of_move = 0
                                break

                        if not move_made:
                            player_clicks = [selected_sq]

                        selected_sq = ()
                        player_clicks = []
            
            # Keyboard controls
            elif event.type == p.KEYDOWN:
                if event.key == p.K_r:  # Reset game
                    gs = GameState()
                    valid_moves = gs.get_valid_moves()
                    selected_sq = ()
                    player_clicks = []
                    move_made = False
                    # Reset clock
                    white_time = 600
                    black_time = 600
                    last_move_time = None
                    clock_running = False
        
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
            
            # Check for checkmate/stalemate
            if gs.checkmate:
                clock_running = False
                winner = "Black" if gs.white_to_move else "White"
                print(f"\nCheckmate! {winner} wins!")
            elif gs.stalemate:
                clock_running = False
                print("\nStalemate!")
        
        # Draw everything
        draw_game_state(screen, gs, valid_moves, selected_sq)
        draw_clock(screen, white_time, black_time, gs.white_to_move)
        
        clock.tick(max_fps)
        p.display.flip()

    p.quit()


if __name__ == "__main__":
    main()
