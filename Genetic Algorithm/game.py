import random
from ai import Ai
import pygame, sys
from gui import Gui

# The configuration
cell_size =   30
cols =        10
rows =        22
maxfps =      30
maxPiece =    1000

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

def rotate_clockwise(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1

def new_board():
    board = [[0 for x in range(cols)] for y in range(rows)]
    return board

class TetrisApp(object):
    def __init__(self, playWithUI, seed):
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.nbPiece = 0
        random.seed(seed)
        self.next_stone = tetris_shapes[random.randint(0, len(tetris_shapes)-1)]
        self.playWithUI = playWithUI
        self.fast_mode = True
        if playWithUI:
            self.gui = Gui()
            self.fast_mode = False
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[random.randint(0, len(tetris_shapes)-1)]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0
        self.nbPiece += 1
        self.computed = False

        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.score = 0
        self.lines = 0

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n]

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self):
        if not self.gameover and not self.paused:
            self.stone_y += 1
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                index = 0

                while index < len(self.board):
                    if 0 not in self.board[index]:
                        self.board = remove_row(self.board, index)
                        cleared_rows += 1
                    else:
                        index += 1

                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop()):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def quit(self):
        if self.playWithUI:
            self.gui.center_msg("Exiting...")
            pygame.display.update()
        sys.exit()

    def speed_up(self):
        self.fast_mode = not self.fast_mode
        if self.fast_mode:
            pygame.time.set_timer(pygame.USEREVENT+1, 25)
        else:
            pygame.time.set_timer(pygame.USEREVENT+1, 25)

    def executes_moves(self, moves):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':      lambda:self.move(-1),
            'RIGHT':     lambda:self.move(+1),
            'DOWN':      lambda:self.drop(True),
            'UP':        self.rotate_stone,
            'p':         self.toggle_pause,
            'SPACE':     self.start_game,
            'RETURN':    self.insta_drop
        }
        for action in moves:
            key_actions[action]()

        if self.fast_mode:
            self.insta_drop()

    def run(self, weights, limitPiece):
        self.gameover = False
        self.paused = False

        while True:

            if self.nbPiece >= limitPiece and limitPiece > 0:
                self.gameover = True

            if self.playWithUI:
                self.gui.update(self)

            if self.gameover:
                return [self.score, self.lines]

            if not self.computed:
                self.computed = True
                Ai.choose(self.board, self.stone, self.next_stone, self.stone_x, weights, self)

            if self.playWithUI:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT+1:
                        self.drop()
                    elif event.type == pygame.QUIT:
                        self.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == eval("pygame.K_s"):
                            self.speed_up()
                        elif event.key == eval("pygame.K_p"):
                            self.toggle_pause()
                        elif event.key == eval("pygame.K_SPACE"):
                            self.start_game()
                            self.gameover = False

if __name__ == '__main__':
    weights = [-2.2268862791675303, -6.527023049342569, -4.8851725039618, -6.150232265388193, -6.134705856372433, -7.205694655068404, -4.427393458309603, -7.828557967297206, -6.850482218171508, 4.178560181139742, -22.14167827267813, -17.386638876889148, -7.098384096524167, 3.136155081751003, -19.51250940083621, -4.55770314757205, -7.354191024692507, -8.919046897690391, -3.180578501796273, -0.6254030222106595, -13.941116652069747, -4.560431733919553, 0.8385323823006321, -2.6755385569378847, -7.188791585137601, -7.119681524600553, -3.3078322546770305, -4.087987056660519, -7.238035241110791, -1.6841055499667088, 9.831803601686591, -8.059307553980682, -8.94266939117442, 3.2521591398329193] 
    starting_seed = random.randint(1, 10000000000000000)
    print(TetrisApp(True, starting_seed).run(weights, -1))
        

