"""
Kevin Liu, David Zhou, and Zhangfeiyang Hao
Prof. Robert Vincent
420-LCW-MS PROGRAMMING TECHNIQUES section 2
2023-05-05

"""


import pygame
import pygame_gui
import random

pygame.init()

class chess_bot():
    '''A simple chess bot that plays agianst the human player.
    To add a chess bot, the user needs to input the difficulty and the side that the bot
    will be playing.'''

    def __init__(self, side, difficulty = 0):
        self.side = side # w or b or None
        self.difficulty = difficulty
    
    def ramdomly_move(self, board): # make a ramdom move
        """Makes a random move from all possible pieces"""
        side = self.side
        ALL_possible_moves = [] # formatted move input
        
        for square in board: # check all the square occupied by the bot 
            if board.get(square)[0] == side:
                piece = board.get(square)[1]

                if piece == 'p':
                    moves = get_pawn_moves(square, side, board)
                    for move in moves:
                        ALL_possible_moves.append(square + '-' + move)
                
                elif piece == 'N':
                    moves = get_pawn_moves(square, side, board)
                    for move in moves:
                        ALL_possible_moves.append(square + '-' + move)
                
                elif piece == 'B':
                    moves = get_bishop_moves(square, board)
                    for move in moves:
                        ALL_possible_moves.append(square + '-' + move)

                elif piece == 'Q':
                    moves = get_queen_moves(square, board)
                    for move in moves:
                        ALL_possible_moves.append(square + '-' + move)

                elif piece == 'R':
                    moves = get_rook_moves(square, board)
                    for move in moves:
                        ALL_possible_moves.append(square + '-' + move)

                elif piece == 'K':
                    moves = get_king_moves(square, side)
                    for move in moves:
                        ALL_possible_moves.append(square + '-' + move)
        
        if ALL_possible_moves:
            return ALL_possible_moves[random.randint(0, len(ALL_possible_moves) - 1)]
        else:
            return # if empty, it means the game should be over and update_moves() won't do anything

#board variables
board_size = (400, 400)
square_size = (board_size[0] // 8, board_size[1] // 8)
white_color = (255, 255, 255)
grey_color = (80, 80, 80)
base_font = pygame.font.Font(None, 32)

turn = "w" #This determines whether it is white's move or black's in order to make sure one player does not move multiple times in a row

#All the pieces' and their respective images
pieces = {
    "bR": pygame.image.load("images/bR.png"),
    "bN": pygame.image.load("images/bN.png"),
    "bB": pygame.image.load("images/bB.png"),
    "bQ": pygame.image.load("images/bQ.png"),
    "bK": pygame.image.load("images/bK.png"),
    "bp": pygame.image.load("images/bp.png"),
    "wR": pygame.image.load("images/wR.png"),
    "wN": pygame.image.load("images/wN.png"),
    "wB": pygame.image.load("images/wB.png"),
    "wQ": pygame.image.load("images/wQ.png"),
    "wK": pygame.image.load("images/wK.png"),
    "wp": pygame.image.load("images/wp.png")
}

#screen of the game
screen = pygame.display.set_mode((1000, 600))
manager = pygame_gui.UIManager((600, 1000))

#Standard chess notation to indicate the starting board state with placed pieces in their initial positions
playing_board = {
    "a8": "bR", "b8": "bN", "c8": "bB", "d8": "bQ", "e8": "bK", "f8": "bB", "g8": "bN", "h8": "bR",
    "a7": "bp", "b7": "bp", "c7": "bp", "d7": "bp", "e7": "bp", "f7": "bp", "g7": "bp", "h7": "bp",
    "a6": "-", "b6": "-", "c6": "-", "d6": "-", "e6": "-", "f6": "-", "g6": "-", "h6": "-",
    "a5": "-", "b5": "-", "c5": "-", "d5": "-", "e5": "-", "f5": "-", "g5": "-", "h5": "-",
    "a4": "-", "b4": "-", "c4": "-", "d4": "-", "e4": "-", "f4": "-", "g4": "-", "h4": "-",
    "a3": "-", "b3": "-", "c3": "-", "d3": "-", "e3": "-", "f3": "-", "g3": "-", "h3": "-",
    "a2": "wp", "b2": "wp", "c2": "wp", "d2": "wp", "e2": "wp", "f2": "wp", "g2": "wp", "h2": "wp",
    "a1": "wR", "b1": "wN", "c1": "wB", "d1": "wQ", "e1": "wK", "f1": "wB", "g1": "wN", "h1": "wR",
}

#Create the chess board
board = pygame.Surface(board_size)
board_position = []
board_position_builder = []

for i in range(8, 0, -1):
    for j in "abcdefgh":
        square = str(j) + str(i)
        board_position_builder.append(square)
        if len(board_position_builder) == 8:
            board_position.append(board_position_builder)
            board_position_builder = []



#Create the squares
for i in range(8):
    for j in range(8):
        square_color = white_color if (i + j) % 2 == 0 else grey_color
        square_rect = pygame.Rect(j * square_size[0], i * square_size[1], square_size[0], square_size[1])
        pygame.draw.rect(board, square_color, square_rect)


#Create the input box
input_rect = pygame.Rect(0, 450, 400, 50)
text_box = pygame_gui.elements.UITextEntryLine(
    relative_rect = pygame.Rect(0, 450, 400, 50),
    manager = manager
)
input = ''


def position_drawer():
    """Draws the current state of the board"""
    for i in range(8):
        for j in range(8):
            piece = playing_board.get(board_position[i][j])
            if piece != "-":
                piece_image = pieces[piece]
                piece_rect = piece_image.get_rect()
                piece_rect.center = ((j + 0.5) * square_size[0], (i + 0.5) * square_size[1])
                screen.blit(piece_image, piece_rect)

pygame.display.update()


def update_move(input):
    """Takes in the user input and plays the move on the playing board"""
    global turn

    has_moved() #This checks at each move, whether the king or the rook has moved or not, if so then they cannot castle
    
    if input == None:
        print('no moves to make for the bot')
        return
    
    moves = input.split("-")
    initial_square = moves[0] #Starting position
    final_square = moves[1] #Final position

    piece_type = get_piece_type(initial_square)

    if playing_board[initial_square][0] == turn: #Checks whether it is the right turn or not
        """
        For all the pieces, the logic works as follow:
        1. Store all the legal moves for the starting move's piece type in a list
        e.g. Let's say we typed e2-e4, the piece on e2 is a white pawn, so we get all the legal moves that this e2 white pawn can move to
        2. We check whether the final position input by the user is in the "legal moves" list 
        3. If it's not, the console prints "Illegal Move" and nothing gets played
        4. If it's in the list, that means the move that the user inputed was legal, then the move gets played
        5. The move gets played by putting the final position's value to the piece and by giving the initial position '-' which means an empty tile
        6. Updates the turns
        7. Draw the new position
        """
        if piece_type == 'wp' or piece_type == 'bp': #Pawns 
            pawn_legal_moves = get_pawn_moves(initial_square, get_piece_color(initial_square), playing_board)

            if final_square not in pawn_legal_moves:
                print('Illegal move')

            elif final_square in pawn_legal_moves:
                playing_board[initial_square] = "-"
                playing_board[final_square] = piece_type
                turn = "b" if turn == "w" else "w"
                position_drawer()

        elif piece_type[1] == 'N': #Knights
            knight_legal_moves = get_knight_moves(initial_square, get_piece_color(initial_square), playing_board)

            if final_square not in knight_legal_moves:
                print('Illegal move')

            elif final_square in knight_legal_moves:
                playing_board[initial_square] = "-"
                playing_board[final_square] = piece_type
                turn = "b" if turn == "w" else "w"
                position_drawer()

        elif piece_type[1] == 'R': #Rooks
            rook_legal_moves = get_rook_moves(initial_square, playing_board)

            if final_square not in rook_legal_moves:
                print('Illegal move')

            elif final_square in rook_legal_moves:
                playing_board[initial_square] = "-"
                playing_board[final_square] = piece_type
                turn = "b" if turn == "w" else "w"
                position_drawer()

        elif piece_type[1] == 'B': #Bishop
            bishop_legal_moves = get_bishop_moves(initial_square, playing_board)

            if final_square not in bishop_legal_moves:
                print('Illegal move')

            elif final_square in bishop_legal_moves:
                playing_board[initial_square] = "-"
                playing_board[final_square] = piece_type
                turn = "b" if turn == "w" else "w"
                position_drawer()

        elif piece_type[1] == 'Q': #Queen
            queen_legal_moves = get_queen_moves(initial_square, playing_board)

            if final_square not in queen_legal_moves:
                print('Illegal move')

            elif final_square in queen_legal_moves:
                playing_board[initial_square] = "-"
                playing_board[final_square] = piece_type
                turn = "b" if turn == "w" else "w"
                position_drawer()

        elif piece_type[1] == 'K': #King
            """
            The King's move is a little bit different as it can also castle unlike the other pieces
            However, the only difference is that if the user's input is '1' or '0', we make a castle instead of just swapping the rook's and the king's position
            since a castle behaves differently than normal move.
            """
            king_legal_moves = get_king_moves(initial_square, get_piece_color(initial_square))

            if final_square not in king_legal_moves:
                print('Illegal move')

            elif final_square == '0' or final_square == '1':
                if turn == 'w': 
                    if final_square == '0':
                        rook = playing_board['h1']
                        king = playing_board['e1']

                        playing_board['g1'] = king
                        playing_board['f1'] = rook
                        playing_board['e1'] = "-"
                        playing_board['h1'] = '-'

                        turn = "b" if turn == "w" else "w"
                        position_drawer()

                    elif final_square == '1':
                        rook = playing_board['a1']
                        king = playing_board['e1']

                        playing_board['c1'] = king
                        playing_board['d1'] = rook
                        playing_board['a1'] = '-'
                        playing_board['e1'] = '-'
                        
                        turn = "b" if turn == "w" else "w"
                        position_drawer()

                elif turn == 'b':
                    if final_square == '0':
                        rook = playing_board['h8']
                        king = playing_board['e8']

                        playing_board['g8'] = king
                        playing_board['f8'] = rook
                        playing_board['e8'] = "-"
                        playing_board['h8'] = '-'

                        turn = "b" if turn == "w" else "w"
                        position_drawer()

                    elif final_square == '1':
                        rook = playing_board['a8']
                        king = playing_board['e8']

                        playing_board['c8'] = king
                        playing_board['d8'] = rook
                        playing_board['a8'] = "-"
                        playing_board['e8'] = '-'

                        turn = "b" if turn == "w" else "w"
                        position_drawer()

            elif final_square in king_legal_moves:
                    playing_board[initial_square] = "-"
                    playing_board[final_square] = piece_type
                    turn = "b" if turn == "w" else "w"
                    position_drawer()

    else:
        print("Illegal move")

def get_piece_type(position):
    """Function that returns the piece type"""
    piece = playing_board[position]
    if piece == '-':
        return None

    return piece


def get_piece_color(position):
    """Function that returns the piece's color"""
    piece = playing_board[position]
    if piece == '-':
        return None
    else:
        color = piece[0]
    return color

winner = ''
def game_win(board):
    """Function that determines whether there is a winner or not by checking if there is still a king on the board or not"""
    global winner
    all_pieces = []
    for square in board:
        all_pieces.append(board[square])
    
    if 'wK' not in all_pieces:
        winner = 'b'
    elif 'bK' not in all_pieces:
        winner = 'w'

a1 = True
h1 = True
a8 = True
h8 = True
e1 = True
e8 = True

def has_moved():
    """
    This functions checks whether the king or the rook has moved or not to determine if the king can castle either queenside or kingside. This is done by tracking the keys on their initial
    square: When the square becomes empty, we know that it must have moved so we set their square to False.
    """
    global a1
    global h1
    global a8
    global h8
    global e1
    global e8

    if playing_board['a1'] == "-":
        a1 = False
    elif playing_board['h1'] == "-":
        h1 = False
    elif playing_board['h8'] == "-":
        h8 = False
    elif playing_board['a8'] == "-":
        a8 = False
    elif playing_board['e1'] == "-":
        e1 = False
    elif playing_board['e8'] == "-":
        e8 = False

def get_king_moves(position, color):
    """
    Function that returns all the king's move in a list
    """
    file, rank = position[0], int(position[1])
    legal_moves = []
    possible_moves = [
        file + str(rank + 1), file + str(rank - 1), #Up and down
        chr(ord(file) + 1) + str(rank), chr(ord(file) - 1) + str(rank), #left and right
        chr(ord(file) + 1) + str(rank + 1), chr(ord(file) + 1) + str(rank - 1), #diagonals
        chr(ord(file) - 1) + str(rank + 1), chr(ord(file) - 1) + str(rank - 1)
    ] #We check for one tile distance in all directions

    for move in possible_moves: #Eliminate moves that are illegal
        if playing_board.get(move) is not None:
            if playing_board.get(move) == '-' and color != (playing_board.get(move) == 'w'): #Same color or empty square
                legal_moves.append(move)

    def castle_kingside(color):
        """
        Function that determines whether a king can short castle or not depending on whether the king or the rook has moved and if the squares separating them are empty
        """
        if color == "w":
            if e1 == True and h1 == True and playing_board['e1'] == "wK" and playing_board['f1'] == '-' and playing_board['g1'] == '-' and playing_board['h1'] == 'wR':
                return True
            else:
                return False
        elif color == 'b':
            if e8 == True and h8 == True and playing_board['e8'] == "bK" and playing_board['f8'] == '-' and playing_board['g8'] == '-' and playing_board['h8'] == 'bR':
                return True
            else:
                return False

    def castle_queenside(color):
        """
        Function that determines whether a king can long castle or not depending on whether the king or the rook has moved and if the squares separating them are empty
        """
        if color == 'w':
            if e1 == True and a1 == True and playing_board['e1'] == 'wK' and playing_board['d1'] == '-' and playing_board['c1'] == '-' and playing_board['b1'] \
            and playing_board['a1'] == 'wR':
                return True
            else: return False
        if color == 'b':
            if e1 == True and a1 == True and playing_board['e8'] == 'bK' and playing_board['d8'] == '-' and playing_board['c8'] == '-' and playing_board['b8'] \
            and playing_board['a8'] == 'bR':
                return True
            else: return False

    #Check if castling moves are legal, if they are, the king should always have the option to castle
    if castle_kingside(color):
        if color == 'w':
            legal_moves.append('0')
        elif color == 'b':
            legal_moves.append('0')
    if castle_queenside(color):
        if color == 'w':
            legal_moves.append('1')
        elif color == 'b':
            legal_moves.append('1')
    
    return legal_moves


def get_knight_moves(position, color, playing_board):
    """
    Function that returns all the knight's move in a list
    """
    file, rank = position[0], int(position[1])
    legal_moves = []
    offsets = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)] #All possible moves

    for offset in offsets: #Removing illegal moves
        target_file = ord(file) + offset[0]
        target_rank = rank + offset[1]
        if target_file < ord('a') or target_file > ord('h') or target_rank < 1 or target_rank > 8: #On the board or not
            continue
        target_position = chr(target_file) + str(target_rank)
        target_piece = playing_board.get(target_position)
        if not target_piece or (target_piece[0] != color): #Same color or not
            legal_moves.append(target_position)

    return legal_moves


def get_pawn_moves(position, color, playing_board):
    """Function that returns all legal moves for a pawn in a list"""
    legal_moves = []
    file, rank = position[0], int(position[1])

    #Make sure that black pawn moves downwards, and white ones, upwards
    if color == 'w':
        direction = 1
    else:
        direction = -1

    if playing_board[position] == 'wp' or playing_board[position] == 'bp':
        if playing_board.get(file + str(rank + direction)) == '-': #1 tile distance empty or not
            legal_moves.append(file + str(rank + direction))
            if (rank == 2 or rank == 7) and playing_board.get(file + (str(rank + 2 * direction))) == "-": #2 tiles distance empty or not
                legal_moves.append(file + str(rank + 2 * direction))


    if turn == 'w':
        if playing_board.get(chr(ord(file) + 1) + str(rank + direction)) is not None: #Checks if diagonals are capturable or not
            if playing_board.get(chr(ord(file) + 1) + str(rank + direction)) != '-' and 'w' != (get_piece_color(chr(ord(file) + 1) + str(rank + direction))):
                legal_moves.append(chr(ord(file) + 1) + str(rank + direction))

        if playing_board.get(chr(ord(file) - 1) + str(rank + direction)) is not None:
            if playing_board.get(chr(ord(file) - 1) + str(rank + direction)) != '-' and 'w' != (get_piece_color(chr(ord(file) - 1) + str(rank + direction))):
                legal_moves.append(chr(ord(file) - 1) + str(rank + direction))

    elif turn == "b":
        if playing_board.get(chr(ord(file) + 1) + str(rank + direction)) is not None: #Checks if diagonals are capturable or not
            if playing_board.get(chr(ord(file) + 1) + str(rank + direction)) != '-' and 'b' != (get_piece_color(chr(ord(file) + 1) + str(rank + direction))):
                legal_moves.append(chr(ord(file) + 1) + str(rank + direction))

        if playing_board.get(chr(ord(file) - 1) + str(rank + direction)) is not None:
            if playing_board.get(chr(ord(file) - 1) + str(rank + direction)) != '-' and 'b' != (get_piece_color(chr(ord(file) - 1) + str(rank + direction))):
                legal_moves.append(chr(ord(file) - 1) + str(rank + direction))

    return legal_moves

def get_rook_moves(position, playing_board):
    
    """Function that returns all legal moves for a rook in a list"""
    
    legal_moves = []
    letter, number = position[0], int(position[1])
    color = str(playing_board[position][0])

    for i in range(number-1,0,-1):  #Check every square below the rook
        square = str(letter) + str(i)
        if playing_board[square] == '-':
            legal_moves.append(square)
        elif str(playing_board[square][0]) != color:
            legal_moves.append(square)
            break
        else:
            break

    for i in range(number+1,9,1):  #Check every square above the rook
        square = str(letter) + str(i)
        if playing_board[square] == '-':
            legal_moves.append(square)
        elif str(playing_board[square][0]) != color:
            legal_moves.append(square)
            break
        else:
            break

    for i in range(ord(letter)-95,9,1):  #Check every square to the right
        square = chr(int(i)+96) + str(number)
        if playing_board[square] == '-':
            legal_moves.append(square)
        elif str(playing_board[square][0]) != color:
            legal_moves.append(square)
            break
        else:
            break

    for i in range(ord(letter)-97,0,-1):  #Check every square to the left
        square = chr(int(i)+96) + str(number)
        if playing_board[square] == '-':
            legal_moves.append(square)
        elif str(playing_board[square][0]) != color:
            legal_moves.append(square)
            break
        else:
            break

    return legal_moves

def get_bishop_moves(position, playing_board):
    """Function that returns all legal moves for a bishop in a list"""
    legal_moves = []
    letter, number = position[0], int(position[1])
    color = str(playing_board[position][0])
    count = 1

    for i in range(number - 1, 0, -1):  #Check every square bottom-left
        if (ord(letter) - count) > 96:
            square = str(chr(ord(letter)-count)) + str(i)
            count += 1
            if playing_board[square] == '-':
                legal_moves.append(square)
            elif str(playing_board[square][0]) != color:
                legal_moves.append(square)
                break
            else:
                break
        else:
            break

    count = 1

    for i in range(number - 1, 0, -1):  #Check every square bottom-right
        if (ord(letter) + count) < 105:
            square = str(chr(ord(letter)+count)) + str(i)
            count += 1
            if playing_board[square] == '-':
                legal_moves.append(square)
            elif str(playing_board[square][0]) != color:
                legal_moves.append(square)
                break
            else:
                break
        else:
            break

    count = 1

    for i in range(number + 1, 9, 1):  #Check every square top-left
        if (ord(letter) - count) > 96:
            square = str(chr(ord(letter)-count)) + str(i)
            count += 1
            if playing_board[square] == '-':
                legal_moves.append(square)
            elif str(playing_board[square][0]) != color:
                legal_moves.append(square)
                break
            else:
                break
        else:
            break

    count = 1

    for i in range(number + 1, 9, 1):  #Check every square top-right
        if (ord(letter) + count) < 105:
            square = str(chr(ord(letter)+count)) + str(i)
            count += 1
            if playing_board[square] == '-':
                legal_moves.append(square)
            elif str(playing_board[square][0]) != color:
                legal_moves.append(square)
                break
            else:
                break
        else:
            break

    return legal_moves

def get_queen_moves(position, playing_board):
    """Function that returns all legal moves for a queen in a list"""
    #Queens move like a bishop+rook
    legal_moves = []
    rook_moves = get_rook_moves(position, playing_board)
    for i in rook_moves:
        legal_moves.append(i)
    bishop_moves = get_bishop_moves(position,playing_board)
    for i in bishop_moves:
        legal_moves.append(i)

    return legal_moves

clock = pygame.time.Clock()
bot = chess_bot(None) # bot disabled by default
bot_status = 'OFF'
w_n = 1

while True:
    game_win(playing_board)
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        elif winner:
            if winner == 'b':
                input = 'Black wins!'
            elif winner == 'w':
                input = 'White wins!'

        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode == '-':  # check if key is a letter,digit,or -
                input += event.unicode.lower()
            elif event.key == pygame.K_BACKSPACE:  # check for backspace
                input = input[:-1]
            elif event.key == pygame.K_RETURN:  # check for enter
                update_move(input)

                if bot_status == 'ON' and (bot.side == 'w' or bot.side == 'b'): # bot moves after the user moves
                    bots_move = bot.ramdomly_move(playing_board)
                    print(bots_move)
                    update_move(bots_move)

                input = ''
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if on_surf.collidepoint(event.pos):
                bot_status = 'ON'
                print("bot enabled")
                
                if bot.side == 'w' and w_n: # first move should make by the bot when it plays white
                    bots_move = bot.ramdomly_move(playing_board)
                    print(bots_move)
                    update_move(bots_move)
                    w_n = None

            elif off_surf.collidepoint(event.pos):
                bot_status = 'OFF'
                print("bot disabled")
            elif white_surf.collidepoint(event.pos):
                bot.side = 'w'
                print("bot is playing white")
                
                if bot_status == 'ON' and w_n: # first move should make by the bot when it plays white
                    bots_move = bot.ramdomly_move(playing_board)
                    print(bots_move)
                    update_move(bots_move)
                    w_n = None
                
            elif black_surf.collidepoint(event.pos):
                bot.side = 'b'
                print("bot is playing black")

        manager.process_events(event)

    manager.update(time_delta)
    
    
    #Draw the screen
    screen.fill((0, 0, 0))

    #Draw the chess board on the screen
    screen.blit(board, (0, 0))
    position_drawer()

    #Draw the input box
    text_surface = base_font.render(input, True, (255, 255, 255))
    screen.blit(text_surface, (10, 460))

    #Draw horizontal labels
    for i in range(8):
        letters = ['a','b','c','d','e','f','g','h']
        label_rect_h = pygame.Rect(0 + i * 50, 400, 50, 50) #Rectangle size
        pygame.draw.rect(screen, (215,193,150), label_rect_h) #Draw it
        h_labels = base_font.render(letters[i], True, (0,0,0)) #create the labels
        screen.blit(h_labels, (20 + i * 50, 415)) 

    #Draw vertical labels
    for i in range(8):
        numbers = ['1','2','3','4','5','6','7','8']
        label_rect_v = pygame.Rect(400, 350 - i * 50, 50, 50)
        pygame.draw.rect(screen, (215,193,150), label_rect_v)
        v_labels = base_font.render(numbers[i], True, (0,0,0))
        screen.blit(v_labels, (420 , 365 - i * 50))
    
    # draw a corner
    corner = pygame.Rect(400, 400, 50, 50)
    pygame.draw.rect(screen, (215,193,150), corner)

    # surface for add bot? and side option
    add_bot_surf = pygame.Rect(0, 500, 450, 100)
    pygame.draw.rect(screen, grey_color, add_bot_surf)
    options_text1 = 'Add bot?' 
    options_text2 = "Bot's side:"
    text_draw1 = base_font.render(options_text1, True, (255, 255, 255))
    text_draw2 = base_font.render(options_text2, True, (255, 255, 255))

    screen.blit(text_draw1, (20, 510))
    screen.blit(text_draw2, (20, 560))

    # On and Off blocks
    on_surf = pygame.Rect(185, 500, 70, 40)
    off_surf = pygame.Rect(288, 500, 70, 40)
    
    if bot_status == 'OFF':
        pygame.draw.rect(screen, grey_color, on_surf)
        pygame.draw.rect(screen, (50,50,50), off_surf)
    elif bot_status == 'ON':
        pygame.draw.rect(screen, (50,50,50), on_surf)
        pygame.draw.rect(screen, grey_color, off_surf)

    ON_text = 'ON' 
    OFF_text = "OFF"
    On_draw = base_font.render(ON_text, True, (255, 255, 255))
    Off_draw = base_font.render(OFF_text, True, (255, 255, 255))

    screen.blit(On_draw, (200, 510))
    screen.blit(Off_draw, (300, 510))

    # Side choices blocks
    white_surf = pygame.Rect(181, 555, 70, 40)
    black_surf = pygame.Rect(283, 555, 70, 40)
    
    if bot.side == None:
        pygame.draw.rect(screen, grey_color, white_surf)
        pygame.draw.rect(screen, grey_color, black_surf)
    elif bot.side == 'w':
        pygame.draw.rect(screen, (50,50,50), white_surf)
        pygame.draw.rect(screen, grey_color, black_surf)
    elif bot.side == 'b':
        pygame.draw.rect(screen, grey_color, white_surf)
        pygame.draw.rect(screen, (50,50,50), black_surf)
    
    white_text = 'white' 
    black_text = "black"
    white_draw = base_font.render(white_text, True, (255, 255, 255))
    black_draw = base_font.render(black_text, True, (255, 255, 255))

    screen.blit(white_draw, (185, 560))
    screen.blit(black_draw, (288, 560))

    #Title
    instruction_font_title = pygame.font.Font(None, 60) 

    box1 = 'How to play'
    label_rect_title = pygame.Rect(450, 0, 550, 150)
    pygame.draw.rect(screen, grey_color, label_rect_title)

    fontUnderline = instruction_font_title
    fontUnderline.set_underline(True)
    textUnderline = fontUnderline.render(box1, True, (255,255,255))

    screen.blit(textUnderline, (620, 50))

    #Instructions
    instruction_font = pygame.font.Font(None, 22)
    for i in range(7):
        box2 = ['1. Enter your move in the black box below the board using the coordinates', '2. Type the initial square followed by a hyphen and the ending square \n (e.g. e2-e4)',
                '3. For long castle, put 1 as your final position and for short castle, 0 \n(e.g. e1-1 for white king long castle)', "4. This chess is using blitz rules which means you have to capture\n your opponent's king to win",
                '5. When a move is illegal, the move will not be played', '6. The bot will automatically play after your move',"7. Please do not modify the bot's settings once the game has started"]

        box2_rect_h = pygame.Rect(450,  120 + i*50, 550, 75)
        pygame.draw.rect(screen, grey_color, box2_rect_h)
        box2_rect = instruction_font.render(box2[i], True, (255,255,255))
        screen.blit(box2_rect, (460, 125 + i*50))
    
    #Good Luck
    glhf_font = pygame.font.Font(None, 35)
    glhf = 'Good luck and have fun!'
    glhf_label = pygame.Rect(450, 100+8*45, 550, 50)
    pygame.draw.rect(screen, grey_color, glhf_label)
    
    fontItalic= glhf_font
    fontItalic.set_italic(True)

    textItalic = fontItalic.render(glhf, True, (255, 255, 255))
    
    #Trademark
    trademark_font = pygame.font.Font(None, 16)
    names = 'By Kevin Liu, David Zhou, and Zhangfeiyang Hao ®'
    label_names_title = pygame.Rect(450, 450, 550, 150)
    pygame.draw.rect(screen, grey_color, label_names_title)
    label_name = trademark_font.render(names, True, (255,255,255))
    screen.blit(label_name, (715, 585))

    screen.blit(textItalic, (590, 500))

    pygame.display.update()