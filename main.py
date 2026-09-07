from src.chess_engine import GameState, Move
import pygame as p
import time
import os

p.init()
BG = p.Color('#2FAFF5')
width = height = 480
DIMENSIONS = 8
sq_size = height // DIMENSIONS
max_fps = 15

images = {}
clock = p.time.Clock()
gs = GameState()

CLOCK_WIDTH = 150
CLOCK_HEIGHT = 60
clock_font = None  
# Clock times in seconds (10 minutes each)
white_time = 120
black_time = 120
last_move_time = None
clock_running = False
# Add this with other global variables
game_over = False
game_result = None
game_message = None

#screen changed for clock
screen = p.display.set_mode((width + CLOCK_WIDTH + 20, height))
#for adding captured pieces
captured_white = []  # pieces captured by black
captured_black = []


def draw_clock(screen, white_time, black_time, white_to_move):
    """
    Draw chess clocks for both players.
    White's clock at bottom-right, Black's clock at top-right.
    Active player's clock is highlighted.
    """
    global clock_font
    clock_bg_color = 'darkgreen'
    # Draw time warning if below 1 minute
    if white_time < 60 and white_active:
        clock_bg_color = 'red'
    if black_time < 60 and black_active:
        clock_bg_color = 'red'
    # Position clocks at top-right and bottom-right of the board
    black_clock_rect = p.Rect(width + 10, 10, CLOCK_WIDTH, CLOCK_HEIGHT)
    white_clock_rect = p.Rect(width + 10, height - CLOCK_HEIGHT - 10, CLOCK_WIDTH, CLOCK_HEIGHT)
    
    # Determine which clock is active
    white_active = white_to_move and clock_running
    black_active = not white_to_move and clock_running
    
    # Draw black clock (top-right)
    black_bg_color = p.Color(clock_bg_color) if black_active else p.Color('gray30')
    p.draw.rect(screen, black_bg_color, black_clock_rect)
    p.draw.rect(screen, p.Color('white'), black_clock_rect, 3)
    
    # Format and draw black time
    black_mins = int(black_time // 60)
    black_secs = int(black_time % 60)
    black_text = clock_font.render(f"{black_mins}:{black_secs:02d}", True, p.Color('white'))
    black_text_rect = black_text.get_rect(center=black_clock_rect.center)
    screen.blit(black_text, black_text_rect)
            
    # Draw white clock (bottom-right)
    white_bg_color = p.Color(clock_bg_color) if white_active else p.Color('gray30')
    p.draw.rect(screen, white_bg_color, white_clock_rect)
    p.draw.rect(screen, p.Color('white'), white_clock_rect, 3)
    
    # Format and draw white time
    white_mins = int(white_time // 60)
    white_secs = int(white_time % 60)
    white_text = clock_font.render(f"{white_mins}:{white_secs:02d}", True, p.Color('white'))
    white_text_rect = white_text.get_rect(center=white_clock_rect.center)
    screen.blit(white_text, white_text_rect)
        




def draw_end_game(screen, result, message):
    """    
    Display end game result with a semi-transparent overlay.    
    result: "1-0" (White wins), "0-1" (Black wins), or "1/2-1/2" (Draw)
    message: Additional message like "Checkmate", "Stalemate", "Time out"
    """
    # Create semi-transparent overlay
    overlay = p.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(200)
    overlay.fill(p.Color('gray40'))
    screen.blit(overlay, (0, 0))
    
    # Result text (large)
    result_font = p.font.SysFont("Arial", 80, True, False)
    result_text = result_font.render(result, True, p.Color('white'))
    result_rect = result_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
    screen.blit(result_text, result_rect)
    
    # Message text (medium)
    message_font = p.font.SysFont("Arial", 36, False, False)
    message_text = message_font.render(message, True, p.Color('lightgray'))
    message_rect = message_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
    screen.blit(message_text, message_rect)
    
    # Instruction text (small)
    instruction_font = p.font.SysFont("Arial", 20, False, False)
    instruction_text = instruction_font.render("Press 'R' to restart", True, p.Color('yellow'))
    instruction_rect = instruction_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    screen.blit(instruction_text, instruction_rect)


'''
PIECE HIGHLIGHT
'''
def highlight(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            border_color = p.Color('yellow')
            border_rect = p.Rect(c * sq_size, r * sq_size, sq_size, sq_size)
            p.draw.rect(screen, border_color, border_rect, 4)
            
            for move in valid_moves:
                if move.start_r == r and move.start_c == c:
                    center_x = move.end_c * sq_size + sq_size // 2
                    center_y = move.end_r * sq_size + sq_size // 2
                    radius = sq_size // 7
                    
                    surface = p.Surface((sq_size, sq_size))
                    surface.set_alpha(180)
                    surface.fill(p.Color('white') if (move.end_r + move.end_c) % 2 == 0 else p.Color('brown'))
                    
                    p.draw.circle(surface, p.Color('black'), (sq_size // 2, sq_size // 2), radius)
                    
                    screen.blit(surface, (move.end_c * sq_size, move.end_r * sq_size))



def animate_move(screen, board, move, clock):
    """Animates a piece smoothly while keeping the sidebar visible."""
    d_r = move.end_r - move.start_r
    d_c = move.end_c - move.start_c
    frames_per_square = 5
    frame_count = max(1, (abs(d_r) + abs(d_c)) * frames_per_square)

    for frame in range(frame_count + 1):
        # interpolated position in squares
        r = move.start_r + d_r * frame / frame_count
        c = move.start_c + d_c * frame / frame_count

        # Fill background using the same BG as main loop
        screen.fill(BG)

        # draw board + highlights + all static pieces (except the piece being animated)
        draw_board(screen)
        # draw other UI elements that should be visible during animation
        draw_captured_pieces(screen)
        # draw pieces (skip the start square where the moving piece originates)
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                piece = board[row][col]
                if piece != "--":
                    if not (row == move.start_r and col == move.start_c):
                        screen.blit(images[piece], (col * sq_size, row * sq_size))

        # draw the moving piece at interpolated pixel coords (use ints)
        x = int(c * sq_size)
        y = int(r * sq_size)
        screen.blit(images[move.piece_moved], (x, y))

        # draw clocks last so they sit on top of everything
        draw_clock(screen, white_time, black_time, gs.white_to_move)

        p.display.flip()
        clock.tick(60)

def draw_captured_pieces(screen):
    """Display captured pieces beside the board."""
    padding = 10
    piece_size = sq_size // 1.5
    start_x = width + 10
    white_start_y = height - CLOCK_HEIGHT - 10 - piece_size - 10  # below white clock
    black_start_y = CLOCK_HEIGHT + 20  # below black clock area

    # Draw black’s captured pieces (white pieces taken)
    x, y = start_x, black_start_y
    for piece in captured_white:
        img = p.transform.scale(images[piece], (piece_size, piece_size))
        screen.blit(img, (x, y))
        x += piece_size + 5
        if x + piece_size > width + CLOCK_WIDTH + 10:
            x = start_x
            y += piece_size + 5

    # Draw white’s captured pieces (black pieces taken)
    x, y = start_x, white_start_y
    for piece in captured_black:
        img = p.transform.scale(images[piece], (piece_size, piece_size))
        screen.blit(img, (x, y))
        x += piece_size + 5
        if x + piece_size > width + CLOCK_WIDTH + 10:
            x = start_x
            y -= piece_size + 5  # stack upwards


#Promotion UI
def choose_promotion(screen, color):    
    # Piece Icon
    choices = ["q", "r", "b", "n"]
    piece_rects = []
    for i, piece in enumerate(choices):
        x = width // 2 - 100 + i * 60
        y = height // 2 - 30
        img = images[color + piece]
        rect = p.Rect(x, y, sq_size, sq_size)
        piece_rects.append((rect, piece))

        p.draw.rect(screen, p.Color("gray"), rect)
        screen.blit(img, (x, y))
    
    p.display.flip()

    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                for rect, piece in piece_rects:
                    if rect.collidepoint(pos):
                        return piece

#loading pieces
def load_images():
    pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]
    piece_path = r"C:\Users\DELL\GITHUB\2-player-chess-gui\assets\bases"
    for piece in pieces:
        image_path = os.path.join(piece_path, f"{piece}.png")
        images[piece] = p.transform.scale(p.image.load(image_path), (sq_size, sq_size))

#Drawing Board
def draw_board(screen):
    colors = [p.Color("white"), p.Color("brown")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, (c * sq_size, r * sq_size, sq_size, sq_size))

#Drawing Pieces
def draw_pieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], (c * sq_size, r * sq_size))

#game state
def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    highlight(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)



#Combining all functions
def main():
    global white_time, black_time, last_move_time, clock_running, clock_font, gs
    global game_over, game_result, game_message
    
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
        
        # Update clock only if game is not over
        if clock_running and last_move_time is not None and not game_over:
            current_time = time.time()
            elapsed = current_time - last_move_time
            last_move_time = current_time
            
            if gs.white_to_move:
                white_time -= elapsed
                if white_time <= 0:
                    white_time = 0
                    clock_running = False
                    game_over = True
                    game_result = "0-1"
                    game_message = "Black wins on time"
                    print("\nBlack wins on time!")
            else:
                black_time -= elapsed
                if black_time <= 0:
                    black_time = 0
                    clock_running = False
                    game_over = True
                    game_result = "1-0"
                    game_message = "White wins on time"
                    print("\nWhite wins on time!")
        
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            
            # Mouse click handler
            elif event.type == p.MOUSEBUTTONDOWN and not game_over:
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
                                #adding captured piece of opponent to list
                                captured_piece = gs.board[i.end_r][i.end_c]
                                if captured_piece != "--":
                                    if captured_piece[0] == 'w':
                                        captured_white.append(captured_piece)
                                    else:
                                        captured_black.append(captured_piece)

                                # Start clock on first move
                                if last_move_time is None:
                                    last_move_time = time.time()
                                    clock_running = True
                                
                                #animating the moves
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
                    # Reset game over state
                    game_over = False
                    game_result = None
                    game_message = None
                    #clear the captured pieces
                    captured_white.clear()
                    captured_black.clear()

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
            
            # Check for checkmate/stalemate
            if gs.checkmate:
                clock_running = False
                game_over = True
                if gs.white_to_move:
                    game_result = "0-1"
                    game_message = "Black wins by checkmate"
                    print(f"\nCheckmate! Black wins!")
                else:
                    game_result = "1-0"
                    game_message = "White wins by checkmate"
                    print(f"\nCheckmate! White wins!")
            elif gs.stalemate:
                clock_running = False
                game_over = True
                game_result = "1/2-1/2"
                game_message = "Draw by stalemate"
                print("\nStalemate!")
        
        # Draw everything
        screen.fill(BG)  # Clear screen first
        draw_game_state(screen, gs, valid_moves, selected_sq)
        draw_clock(screen, white_time, black_time, gs.white_to_move)
        draw_captured_pieces(screen)

        # Draw end game overlay if game is over
        if game_over:
            draw_end_game(screen, game_result, game_message)
        
        clock.tick(max_fps)
        p.display.flip()

    p.quit()


if __name__ == "__main__":
    main()
