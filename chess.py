import pygame
import pygame.locals
from tkinter import *
from tkinter import messagebox


BOARD_DEFAULTS = """rnbqkbnr
pppppppp
        
        
        
        
PPPPPPPP
RNBQKBNR""".split("\n")
##Helper Functions
def LetterToColumnIndex(letter):
    return (ord(letter.upper()) - ord('A'))#returns an integer by subtracting 2 letter via ord

def ColumnIndexToLetter(column_index):
    return chr(column_index + ord('A'))

def NumberToRowIndex(number):
    return 8 - number

def RowIndexToNumber(row_index):
    return 8 - row_index

def NumberToRowIndexToBoard(number):
    return (8 - number) * 100

def BoardToRowIndexToNumber(board_pos):
    return 8 - board_pos // 100  

def StrPleaseDontPrintNone(value):
    if value:
        return str(value)
    else:
        return " "

def IsValidSquare(letter, number): #checks if the square is valid and returns bool
    ascii_index = ord(letter.upper())
    letter_within_bounds = ord('A') <= ascii_index and ascii_index <= ord('H')
    return letter_within_bounds and 1 <= number and number <= 8

def AddIntToLetter(integer, letter):
    return chr(integer + ord(letter))

def AddIntToLetterReturnInt(integer, letter):
    return (integer + ord(letter))

def GetMoves(integer, integerDirection, letter, letterDirection, piece, valid_moves):
    if IsValidSquare (AddIntToLetter(letterDirection, letter), integer + integerDirection):
        existing_piece = piece.board.Get(AddIntToLetter(letterDirection, letter), integer + integerDirection)
        
    while IsValidSquare(AddIntToLetter(letterDirection, letter), integer + integerDirection) and not existing_piece:
        piece.AppendValidMove(AddIntToLetter(letterDirection, letter), integer + integerDirection , valid_moves)
        letter = AddIntToLetter(letterDirection, letter)
        integer += integerDirection
        if IsValidSquare(AddIntToLetter(letterDirection, letter), integer + integerDirection):
            existing_piece = piece.board.Get(AddIntToLetter(letterDirection, letter), integer + integerDirection)
    piece.AppendValidCapture(AddIntToLetter(letterDirection, letter), integer + integerDirection , valid_moves)    
    return valid_moves
        
##End of Helper Functions

##Classes
class Piece():
    def __init__(self, letter, number, color, board):
        self.letter = letter
        self.number = number
        self.color = color ## boolean; false = black = lowercase
        self.board = board
        self.valid_moves = []

    def AppendValidMove(self, letter, number, valid_moves):
        if IsValidSquare(letter, number):
            existing_piece = self.board.Get(letter, number)
            if not existing_piece:
                valid_moves.append([letter, number])

    def AppendValidCapture(self, letter, number, valid_moves):
        if IsValidSquare(letter, number):
            existing_piece = self.board.Get(letter, number)
            if existing_piece and existing_piece.color != self.color:
                valid_moves.append([letter, number])

    def GetValidMoves(self):
        ## To be Implemented by Child Class
        pass

    def __str__(self):
        ## To be Overridden by Child Class
        return "(" + self.letter + " " + str(self.number) + ")"

class Pawn(Piece):
    def __init__(self, letter, number, color, board):
        Piece.__init__(self, letter, number, color, board)
        self.start_letter = self.letter
        self.start_number = self.number

    def GetValidMoves(self):
        valid_moves = []
        direction = -1
        if self.color:
            direction = 1

        ## 1. Forward 1 square
        self.AppendValidMove(self.letter, self.number + direction, valid_moves)
        
        ## 2. Forward 2 squares
        was_able_to_move = len(valid_moves) > 0
        if was_able_to_move and ((self.color and self.number == 2) or (not self.color and self.number == 7)):
            self.AppendValidMove(self.letter, self.number + direction * 2, valid_moves)

        ## 3. Diagonal captures
        ## a) Diagonal Left
        self.AppendValidCapture(AddIntToLetter(-1, self.letter), self.number + direction, valid_moves)
        ## b) Diagonal Right
        self.AppendValidCapture(AddIntToLetter(1, self.letter), self.number + direction, valid_moves)

        return valid_moves

    def __str__(self):
        if not self.color:
            return "p"
        else:
            return "P"

class Knight(Piece):
    def __init__(self, letter, number, color, board):
        Piece.__init__(self, letter, number, color, board)

    def GetValidMoves(self):
        valid_moves = []
        possible_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for move_letter,move_number in possible_moves:
            self.AppendValidMove(AddIntToLetter(move_letter, self.letter), self.number+move_number, valid_moves)
            self.AppendValidCapture(AddIntToLetter(move_letter, self.letter), self.number+move_number, valid_moves)
            
        return valid_moves

    def __str__(self):
        if not self.color:
            return "n"
        else:
            return "N"

class Bishop(Piece):
    def __init__(self, letter, number, color, board):
        Piece.__init__(self, letter, number, color, board)
    
    def GetValidMoves(self):
        diagonal_move_letter = self.letter
        diagonal_move_number = self.number
        valid_moves= []
        possible_moves = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for move_letter,move_number in possible_moves:
            GetMoves(diagonal_move_number, move_number, diagonal_move_letter, move_letter, self, valid_moves)
        return valid_moves

    def __str__(self):
        if not self.color:
            return "b"
        else:
            return "B"

class Rook(Piece):
    def __init__(self, letter, number, color, board):
        Piece.__init__(self, letter, number, color, board)
        self.move_counter = 0

    def GetStartLetter(self):
        return start_letter
    
    def GetStartNumber(self):
        return start_number

    def GetValidMoves(self):
        valid_moves = []
        diagonal_move_letter = self.letter
        diagonal_move_number = self.number
        possible_moves = [(1,0),(0,-1),(-1,0),(0,1)]
        for move_letter,move_number in possible_moves:
            GetMoves(diagonal_move_number, move_number, diagonal_move_letter, move_letter, self, valid_moves)
        return valid_moves

    def __str__(self):
        if not self.color:
            return "r"
        else:
            return "R"

class Queen(Piece):
    def __init__(self, letter, number, color, board):
        Piece.__init__(self, letter, number, color, board)

    def GetValidMoves(self):
        diagonal_move_letter = self.letter
        diagonal_move_number = self.number
        valid_moves= []
        possible_moves = [(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for move_letter,move_number in possible_moves:
            GetMoves(diagonal_move_number, move_number, diagonal_move_letter, move_letter, self, valid_moves)
        return valid_moves

    def __str__(self):
        if not self.color:
            return "q"
        else:
            return "Q"

class King(Piece):
    def __init__(self, letter, number, color, board):
        Piece.__init__(self, letter, number, color, board)
        self.move_counter = 0
        
    def GetStartLetter(self):
        return start_letter
    
    def GetStartNumber(self):
        return start_number
    
    def GetValidMoves(self):
        valid_moves = []
        possible_moves = [(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for move_letter,move_number in possible_moves:
            self.AppendValidMove(AddIntToLetter(move_letter, self.letter), self.number+move_number, valid_moves)
            self.AppendValidCapture(AddIntToLetter(move_letter, self.letter), self.number+move_number, valid_moves)
        return valid_moves
    def __str__(self):
        if not self.color:
            return "k"
        else:
            return "K"

def GeneratePiece(character, letter, number, board):
    if character.lower() == "p":
        return Pawn(letter, number, character.upper() == character, board) #character.upper() == character returns a boolean. If its a lower case, returns false, else true.
    elif character.lower() == "n":
        return Knight(letter, number, character.upper() == character, board)
    elif character.lower() == "b":
        return Bishop(letter, number, character.upper() == character, board)
    elif character.lower() == "r":
        return Rook(letter, number, character.upper() == character, board)
    elif character.lower() == "q":
        return Queen(letter, number, character.upper() == character, board)
    elif character.lower() == "k":
        return King(letter, number, character.upper() == character, board)
    else:
        return None

class Board():
    def __init__(self):
        self.grid = []
        self.en_passant_victim = None

        for i in range(8):
            row = []

            for j in range(8):
                letter = ColumnIndexToLetter(j)
                number = RowIndexToNumber(i)
                valid_moves = []
                row.append(GeneratePiece(BOARD_DEFAULTS[i][j], letter, number, self))
 
            self.grid.append(row)

    ## Get the piece located at letter, number
    def Get(self, letter, number):
        return self.grid[NumberToRowIndex(number)][LetterToColumnIndex(letter)]

    ## Set the piece located at letter, number, clobbering previous contents
    def Set(self, letter, number, piece):
        self.grid[NumberToRowIndex(number)][LetterToColumnIndex(letter)] = piece
        if piece:
            piece.letter = letter.upper()
            piece.number = number

    ## Assumes positions are correct when making the move
    def Move(self, start_letter, start_number, end_letter, end_number):
        piece_to_move = self.Get(start_letter, start_number)
                        
        ## Handle en passant
        if isinstance(piece_to_move, Pawn) and end_letter != start_letter and not self.Get(end_letter, end_number):
            self.Set(self.en_passant_victim.letter, self.en_passant_victim.number, None)
        
        if isinstance(piece_to_move, Pawn) and abs(end_number - piece_to_move.start_number) == 2:
            self.en_passant_victim = piece_to_move
        else:
            self.en_passant_victim = None

        ##Handle Castle
        if isinstance(piece_to_move, King) and abs(AddIntToLetterReturnInt(0, end_letter) - AddIntToLetterReturnInt(0, piece_to_move.letter)) == 2:
            for row in self.grid:
                for rook in row:
                    if isinstance(rook, Rook) and piece_to_move.color == rook.color:
                        
                        if piece_to_move.color:
                            if end_letter == 'G' and end_number == 1 and rook.letter == 'H' and rook.number == 1:
                                self.Set('F',1,rook)
                                rook.move_counter = True
                                self.Set('H', 1, None)
                            if end_letter == 'C' and end_number == 1  and rook.letter == 'A' and rook.number == 1:
                                self.Set('D',1,rook)
                                rook.move_counter = True
                                self.Set('A', 1, None)
                        else:
                            if end_letter == 'G' and end_number == 8  and rook.letter == 'H' and rook.number == 8:
                                self.Set('F',8,rook)
                                rook.move_counter = True
                                self.Set('H', 8, None)
                            if end_letter == 'C' and end_number == 8  and rook.letter == 'A' and rook.number == 8:
                                self.Set('D',8,rook)
                                rook.move_counter = True
                                self.Set('A', 8, None)
                    piece_to_move.move_counter += 1
                    
        if isinstance(piece_to_move, King):
            piece_to_move.move_counter += 1
        elif isinstance(piece_to_move, Rook):
            piece_to_move.move_counter += 1

        ## Handle Promoting of a pawn

        if isinstance(piece_to_move, Pawn):
            if piece_to_move.color:
                if end_number == 8:
                    while True:
                        promotion = input("Pick a piece: Q, R, B, N")
                        print(promotion)
                        if promotion in ['Q','R','B','N']:
                            break
                        else:
                            print("Invalid choice")

                    if promotion.upper() == 'Q':
                        new_piece = Queen(end_letter, end_number, True, self)
                    elif promotion.upper() == 'R':
                        new_piece = Rook(end_letter, end_number, True, self)
                    elif promotion.upper() == 'B':
                        new_piece = Bishop(end_letter, end_number, True, self)
                    elif promotion.upper() == 'N':
                        new_piece = Knight(end_letter, end_number, True, self)
                    self.Set(end_letter, end_number, new_piece)
                    self.Set(start_letter, start_number, None)
                            
            if not piece_to_move.color:
                if end_number == 1:
                    while True:
                        promotion = input("Pick a piece: Q, R, B, N")
                        print(promotion)
                        if promotion in ['Q','R','B','N']:
                            break
                        else:
                            print("Invalid choice")
                            
                    if promotion.upper() == 'Q':
                        new_queen = Queen(end_letter, end_number, False, self)
                    if promotion.upper() == 'Q':
                        new_piece = Queen(end_letter, end_number, False, self)
                    elif promotion.upper() == 'R':
                        new_piece = Rook(end_letter, end_number, False, self)
                    elif promotion.upper() == 'B':
                        new_piece = Bishop(end_letter, end_number, False, self)
                    elif promotion.upper() == 'N':
                        new_piece = Knight(end_letter, end_number, False, self)
                    self.Set(end_letter, end_number, new_piece)
                    self.Set(start_letter, start_number, None)
                            
        if isinstance(piece_to_move, Pawn):
            if end_number == 8 and piece_to_move.color:
                pass
            elif end_number == 1 and not piece_to_move.color:
                pass
            else:
                self.Set(end_letter, end_number, piece_to_move)
                self.Set(start_letter, start_number, None)
        else:
            self.Set(end_letter, end_number, piece_to_move)
            self.Set(start_letter, start_number, None)

    ## Used to differentiate an actual move or a simple check in position
    def TempMove(self, start_letter, start_number, end_letter, end_number):
        piece_to_move = self.Get(start_letter, start_number)
        self.Set(end_letter, end_number, piece_to_move)
        self.Set(start_letter, start_number, None)

    ## Finds the king of the specified color and checks to see if other pieces could move to the kings current location    
    def IsInCheck(self, king_color):
        other_valid_moves = []
        king_coord = []
        for row in self.grid:
          for piece in row:
            if isinstance(piece, King) and piece.color == king_color:
                king_coord += [piece.letter, piece.number]
            elif piece:
                if piece.color != king_color:
                    other_valid_moves += piece.GetValidMoves()
        return king_coord in other_valid_moves

    def GetLegalMoves(self):
        result = {}
        for row in self.grid:
            for piece in row:
                if piece:
                    legal_moves = [] 
                    keep_letter = piece.letter
                    keep_number = piece.number
                    
                    ## filters out possible moves and adds them to legal_moves
                    for moves in piece.GetValidMoves():
                        capture = self.Get(moves[0],moves[1])
                        save_piece = capture
                        save_piece_letter = moves[0]
                        save_piece_number = moves[1]
                        self.TempMove(piece.letter, piece.number, moves[0], moves[1])
                        if not self.IsInCheck(piece.color):
                            legal_moves.append([moves[0],moves[1]])
                        self.TempMove(piece.letter, piece.number, keep_letter, keep_number)
                        self.Set(save_piece_letter, save_piece_number, save_piece)

                    ## en passant special case
                    if isinstance(piece, Pawn):
                        if self.en_passant_victim and self.en_passant_victim.number == piece.number:
                            left_letter = AddIntToLetter(-1, piece.letter)
                            right_letter = AddIntToLetter(1, piece.letter)
                            directions = [left_letter, right_letter]
                            for direction in directions:
                                if self.en_passant_victim.letter == direction:
                                    if self.en_passant_victim.color != piece.color:
                                        if piece.color:
                                            destination_number = self.en_passant_victim.number + 1
                                        else:
                                            destination_number = self.en_passant_victim.number - 1
                                        if IsValidSquare(direction, destination_number):
                                            save_piece_letter = piece.letter
                                            save_piece_number = piece.number
                                            
                                            self.TempMove(piece.letter, piece.number, direction, destination_number)
                                            if not self.IsInCheck(piece.color):
                                                legal_moves.append([direction, destination_number])
                                            self.TempMove(piece.letter, piece.number, save_piece_letter, save_piece_number)

                    ## Castling special case
                    if isinstance(piece, King):
                        if not piece.move_counter:  ##check if king has not moved
                            if piece.color: ## check if its white or black
                                for row2 in self.grid:
                                    for rook in row2:
                                        if isinstance(rook, Rook): ## find a rook
                                            if rook.color and not rook.move_counter and rook.letter == 'H':  ## check to see if it is a white rook that hasnt moved on H1
                                                if not self.Get('F',1) and not self.Get('G',1): ## check to see if there are pieces in between rook and king
                                                    if not self.IsInCheck(piece.color): ## check to see if king is currently in check
                                                        save_piece_letter = piece.letter
                                                        save_piece_number = piece.number
                                                        squares = [('F',1),('G',1)]
                                                        
                                                        safe_square = 0
                                                        for square in squares:
                                                            self.TempMove(piece.letter, piece.number, square[0], square[1])
                                                            if not self.IsInCheck(piece.color):
                                                                safe_square += 1
                                                            self.TempMove(piece.letter, piece.number, save_piece_letter, save_piece_number)
                                                        if safe_square == 2: ## if king doesnt castle through check -> safe_square == 2
                                                            legal_moves.append(['G',1])
                                                                
                                            if rook.color and not rook.move_counter and rook.letter == 'A': ## check to see if it is a white rook that hasnt moved on A1
                                                if not self.Get('B',1) and not self.Get('C',1) and not self.Get('D',1): ## check to see if there are pieces between rook and king
                                                    if not self.IsInCheck(piece.color):
                                                        save_piece_letter = piece.letter
                                                        save_piece_number = piece.number
                                                        squares = [('C',1),('D',1)]

                                                        safe_square = 0
                                                        for square in squares:
                                                            self.TempMove(piece.letter, piece.number, square[0], square[1])
                                                            if not self.IsInCheck(piece.color):
                                                                safe_square += 1
                                                            self.TempMove(piece.letter, piece.number, save_piece_letter, save_piece_number)
                                                        if safe_square == 2:
                                                            legal_moves.append(['C',1])

                            else: ## king is black
                                for row2 in self.grid:
                                    for rook in row2: 
                                        if isinstance(rook, Rook):
                                            if not rook.color and not rook.move_counter and rook.letter == 'H': ## find a black rook that hasnt moved on H8
                                                if not self.Get('F',8) and not self.Get('G',8):
                                                    if not self.IsInCheck(piece.color):
                                                        save_piece_letter = piece.letter
                                                        save_piece_number = piece.number
                                                        squares = [('F',8),('G',8)]

                                                        safe_square = 0
                                                        for square in squares:
                                                            self.TempMove(piece.letter, piece.number, square[0], square[1])
                                                            if not self.IsInCheck(piece.color):
                                                                safe_square += 1
                                                            self.TempMove(piece.letter, piece.number, save_piece_letter, save_piece_number)
                                                        if safe_square == 2:
                                                            legal_moves.append(['G',8])

                                            if not rook.color and not rook.move_counter and rook.letter == 'A':
                                                if not self.Get('B',8) and not self.Get('C',8) and not self.Get('D',8):
                                                    if not self.IsInCheck(piece.color):
                                                        save_piece_letter = piece.letter
                                                        save_piece_number = piece.number
                                                        squares = [('C',8),('D',8)]

                                                        safe_square = 0
                                                        for square in squares:
                                                            self.TempMove(piece.letter, piece.number, square[0], square[1])
                                                            if not self.IsInCheck(piece.color):
                                                                safe_square += 1
                                                            self.TempMove(piece.letter, piece.number, save_piece_letter, save_piece_number)
                                                        if safe_square == 2:
                                                            legal_moves.append(['C',8])

                    result[piece] = legal_moves
        return result                                       

    def CheckMate(self):
        if self.IsInCheck(True) or self.IsInCheck(False):
            count = 0
            for row in self.grid:
                for piece in row:
                    if piece and isinstance(piece, King) and self.IsInCheck(piece.color):
                            store_moves = []
                            all_legal_moves = board.GetLegalMoves()
                            for item in all_legal_moves.items():
                                if item[0].color == piece.color:
                                     store_moves += item[1:]
                            for moves in store_moves:
                                if moves:
                                    count += 1     
                            if not count:
                                return True
                            else:
                                return False

    def StaleMate(self):
        store_moves = []
        store_moves_black = []
        count = 0
        count_black = 0
        all_legal_moves = board.GetLegalMoves()
        for row in self.grid:
            for piece in row:
                for item in all_legal_moves.items():
                    if item[0].color == True:
                        store_moves += item[1:]
                    else:
                        store_moves_black += item[1:]
                for moves in store_moves:
                    if moves:
                        count += 1
                if not count:
                    return True
                else:
                    return False
                for moves in store_moves_black:
                    if moves:
                        count_black += 1
                if not count:
                    return True
                else:
                    return False
 
    def __str__(self):
        s = "  |" + "A B C D E F G H|  \n"
        s += "--+---------------+--\n"
        for i in range(8):
            s += str(RowIndexToNumber(i)) + " |"
            row = self.grid[i]
            for j in range(8):
                if j > 0:
                    s += " "
                if row[j]:
                    s += str(row[j])
                else:
                    if (j + i % 2) % 2 == 0:
                        s += " "
                    else:
                        s += "*"
            s += "| " + str(RowIndexToNumber(i)) + "\n"
        s += "--+---------------+--\n"
        s += "  |" + "A B C D E F G H|  "
        return s

pygame.init()

## variables for pygame
screen = pygame.display.set_mode([800,800])
pygame.display.set_caption('Chess')
running = True
board = Board()
player_turn = True

white_pawn = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\WhitePawnNoBackground.png')
white_rook = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\WhiteRookNoBackground.png')
white_bishop = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\WhiteBishopNoBackground.png')
white_knight = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\WhiteKnightNoBackground.png')
white_king = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\WhiteKingNoBackground.png')
white_queen = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\WhiteQueenNoBackground.png')

black_pawn = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\BlackPawnNoBackground.png')
black_rook = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\BlackRookNoBackground.png')
black_bishop = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\BlackBishopNoBackground.png')
black_knight = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\BlackKnightNoBackground.png')
black_king = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\BlackKingNoBackground.png')
black_queen = pygame.image.load(r'C:\Users\elmas\Desktop\python projects\Chess\Chess Pieces\BlackQueenNoBackground.png')

future_piece_coord = None
current_piece_coord = None

def LetterToColumnIndexToBoard(letter):
    return (ord(letter.upper()) - ord('A'))*100

def BoardToColumnIndexToLetter(board_pos):
    return chr(board_pos // 100 + ord('A'))

def PieceToPicture(piece, color):

    if color:                    
        if isinstance(piece, Pawn):
            return white_pawn
        if isinstance(piece, Rook):
            return white_rook
        if isinstance(piece, Knight):
            return white_knight
        if isinstance(piece, Bishop):
            return white_bishop
        if isinstance(piece, King):
            return white_king
        if isinstance(piece, Queen):
            return white_queen

    else:
        if isinstance(piece, Pawn):
            return black_pawn
        if isinstance(piece, Rook):
            return black_rook
        if isinstance(piece, Knight):
            return black_knight
        if isinstance(piece, Bishop):
            return black_bishop
        if isinstance(piece, King):
            return black_king
        if isinstance(piece, Queen):
            return black_queen
        
Tk().wm_withdraw() #to hide the main window

while running:
    
    screen.fill((150, 200, 100))
    square_offset = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_piece_coord = future_piece_coord
            future_piece_coord = [BoardToColumnIndexToLetter(event.pos[0]), BoardToRowIndexToNumber(event.pos[1])]
            
    font = pygame.font.Font('freesansbold.ttf', 20)
    small_letter = 'a'
    small_number = '8'
    small_letter_increment = 1
    if board.CheckMate():
        messagebox.showinfo('Chess', 'CheckMate')
        running = False
    if board.StaleMate():
        messagebox.showinfo('Chess', 'StaleMate')
        running = False
    for row in range(0, 801, 100):
        for column in range(0, 801, 200):
            pygame.draw.rect(screen, (240,240,240), (row, column + square_offset, 100, 100))
            
        square_offset += 100
        text = font.render(small_letter, True, (0,0,0)) #a-h
        num = font.render(small_number, True, (0,0,0)) #1-8
        screen.blit(text, (row, 770))
        screen.blit(num, (0, row))
        small_letter = chr(ord('a') + small_letter_increment)
        small_number = chr(ord('8') - small_letter_increment)
        small_letter_increment += 1
        if square_offset > 100:
            square_offset = 0
        for row in board.grid:
            for piece in row:
                if piece:
                    letter = piece.letter
                    number = piece.number
                    color = piece.color
                    screen.blit(PieceToPicture(piece,color),(LetterToColumnIndexToBoard(letter), NumberToRowIndexToBoard(number)))

    if future_piece_coord != current_piece_coord:
        if future_piece_coord and current_piece_coord:
            current_piece = board.Get(*current_piece_coord)
            if current_piece and current_piece.color == player_turn:
                all_legal_moves = board.GetLegalMoves()
                piece_legal_moves = all_legal_moves[current_piece]
                if future_piece_coord in piece_legal_moves:
                    board.Move(current_piece_coord[0], current_piece_coord[1], future_piece_coord[0], future_piece_coord[1])
                    current_piece_coord = None
                    future_piece_coord = None
                    player_turn = not player_turn
    else:
        current_piece_coord = None
        future_piece_coord = None
            
    if future_piece_coord:  
        highlighted_piece = board.Get(*future_piece_coord)
 
        if highlighted_piece and highlighted_piece.color == player_turn:
            pygame.draw.rect(screen, (0, 255, 0), (LetterToColumnIndexToBoard(highlighted_piece.letter), NumberToRowIndexToBoard(highlighted_piece.number), 100, 100), 5)
            all_legal_moves = board.GetLegalMoves()
            piece_legal_moves = all_legal_moves[highlighted_piece]
            for moves in piece_legal_moves:
                pygame.draw.rect(screen, (0, 255, 0), (LetterToColumnIndexToBoard(moves[0]), NumberToRowIndexToBoard(moves[1]), 100, 100), 5)

    if board.IsInCheck(True) or board.IsInCheck(False):
            for row in board.grid:
                for piece in row:
                    if piece and isinstance(piece, King) and board.IsInCheck(piece.color):
                        pygame.draw.rect(screen, (255, 0, 0), (LetterToColumnIndexToBoard(piece.letter), NumberToRowIndexToBoard(piece.number), 100, 100), 5)
                        
    pygame.display.flip()

pygame.quit()
while True:
    
    print(board)
    if player_turn:
        print("White's Turn")
    else:
        print("Black's Turn")
    choose_piece = input("Choose a piece to move (example 'E1') -1 to surrender\n")
    if choose_piece == "-1":
        print("Player Surrender")
        break
    else:
        try:
            if choose_piece[0].upper() in ['A','B','C','D','E','F','G','H']:
                letter_from = choose_piece[0].upper()
                if int(choose_piece[1]) in [1,2,3,4,5,6,7,8]:
                    number_from = int(choose_piece[1])
                    if IsValidSquare(letter_from, number_from):
                        if isinstance(board.Get(letter_from, number_from), Piece):
                            if board.Get(letter_from, number_from).color == player_turn:
                                piece = board.Get(letter_from, number_from)
                                all_legal_moves = board.GetLegalMoves()
                                piece_legal_moves = all_legal_moves[piece]
                                print(piece_legal_moves)
                                player_move = input("Choose a move from the list of valid moves\n")
                                if player_move and player_move[0].upper() in ['A','B','C','D','E','F','G','H'] and player_move[1] in [1,2,3,4,5,6,7,8]:
                                    letter_to = player_move[0].upper()
                                    number_to = int(player_move[1])
                                    if [letter_to, number_to] in piece_legal_moves:
                                        board.Move(letter_from, number_from, letter_to, number_to)
                                        if player_turn:
                                            player_turn = False
                                        else:
                                            player_turn = True
                                    else:
                                        print("Invalid Move")
                                elif player_move == "-1":
                                    print("Player Surrender")
                                    break
                                else:
                                    print("You must pick a move")
                            else:
                                print("Invalid Piece")
                        else:
                            print("Pick a Valid Piece!")
                    else:
                        print("Invalid square")
                else:
                    print("Invalid number")
            else:
                print("Invalid letter")
                    
        except ValueError:
            print("Please follow the example")


