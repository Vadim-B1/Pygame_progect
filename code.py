# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
import pygame
import os
import random


def load_image(name, size_bottom, size_side, colorkey=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return pygame.transform.scale(image, (size_bottom, size_side))


def decode_money(money):
    sp = ['', 'К', 'Мл', 'Мр', 'Тр', 'Кв']
    col = 0
    while money >= 1000:
        money /= 1000
        col += 1
    if col > len(sp) - 1:
        col = len(sp) - 1
    return f'{round(money)}{sp[col]}'


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[''] * width for _ in range(height)]
        self.sp_plants = ['sunflower.png', 'fighter_chamomile.png', 'Venerina_muholovka.png', 'potato.png']
        self.last_choice_plant = ''
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.minus = 0
        self.sl = {
            'sunflower4.png': 10,
            'fighter_chamomile2.png': 30,
            'Venerina_muholovka2.png': 40,
            'potato2.png': 20}

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render_cells(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(load_image('grass.png', 60, 60),
                            (x * self.cell_size + self.left, y * self.cell_size + self.top))

    def render_plants(self, screen, screen2, screen3, coords):
        x, y = coords
        if self.board[y][x] != '':
            x1 = x * self.cell_size + self.left
            y1 = y * self.cell_size + self.top
            screen3.blit(load_image(self.board[y][x], 60, 60, -1), (0, 0))
            screen.blit(screen3, (x1, y1))
            screen2.blit(screen3, (x1, y1))
            screen3.blit(load_image('grass.png', 60, 60), (0, 0))

    def chk_money(self):
        if self.last_choice_plant != '' and self.last_choice_plant != 'grass.png':
            return self.sl[self.last_choice_plant]
        else:
            return 0

    def rtrn_minus_money(self):
        return self.minus

    def get_cell(self, mouse_pos):
        width, height = pygame.display.get_surface().get_size()
        x_mouse, y_mouse = mouse_pos
        if x_mouse < self.left or x_mouse > (self.left + self.cell_size * self.width) or \
                (y_mouse < self.top) or (y_mouse > (self.top + self.cell_size * self.height)):
            rtrn = None
        else:
            rtrn = ((x_mouse - self.left) // self.cell_size, (y_mouse - self.top) // self.cell_size)
        return rtrn

    def on_click(self, cell_coords, money):
        if cell_coords != None:
            x, y = cell_coords
            if money >= self.chk_money():
                if self.last_choice_plant != '' and (
                        self.board[y][x] == '' or self.last_choice_plant == 'grass.png' or self.board[y][x] == 'grass.png') \
                        and self.board[y][x] != self.last_choice_plant:
                    self.board[y][x] = self.last_choice_plant
                    self.minus = self.chk_money()
            else:
                self.minus = 0

    def get_click(self, mouse_pos, money1):
        self.on_click(self.get_cell(mouse_pos), money1)

    def change_last_choice_plant(self, plant):
        self.last_choice_plant = plant

    def rtrn_board(self):
        return self.board

    def chk_sun_fl(self):
        count = 0
        for brd in self.board:
            for i in range(9):
                if brd[i] == 'sunflower4.png':
                    count += 1
        return count

    def die_plant(self, x, y):
        self.board[x][y] = 'grass.png'

    def clear(self):
        self.board = [['grass.png'] * self.width for _ in range(self.height)]
        self.last_choice_plant = ''
        self.minus = 0


class ChoicePlant:
    # создание поля
    def __init__(self, height):
        self.height = height
        self.board = [[0] * height]
        self.plants = ['sunflower.png', 'fighter_chamomile.png', 'Venerina_muholovka.png', 'potato.png']
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 40

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            screen.blit(load_image(self.plants[y], 50, 50), (10, self.top + self.cell_size * y))
            pygame.draw.rect(screen, (0, 0, 0),
                             [(self.left, y * self.cell_size + self.top),
                              (self.cell_size, self.cell_size)], 1)

    def get_cell(self, mouse_pos):
        x_mouse, y_mouse = mouse_pos
        if x_mouse < self.left or x_mouse > (self.left + self.cell_size) or \
                (y_mouse < self.top) or (y_mouse > (self.top + self.cell_size * self.height)):
            rtrn = None
        else:
            rtrn = ((x_mouse - self.left) // self.cell_size, (y_mouse - self.top) // self.cell_size)
        return rtrn

    def on_click(self, cell_coords):
        if cell_coords != None:
            x, y = cell_coords
            if y == 0:
                return 'sunflower4.png'
            elif y == 1:
                return 'fighter_chamomile2.png'
            elif y == 2:
                return 'Venerina_muholovka2.png'
            elif y == 3:
                return 'potato2.png'

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell)

    def clear(self):
        self.board = [[0] * self.height]


class Shovel:
    def __init__(self):
        self.lopata = 'lopata.png'
        self.left = 20
        self.top = 20
        self.cell_size = 50

    def render_shovel(self, screen):
        screen.blit(load_image(self.lopata, 50, 50), (20, 20))
        pygame.draw.rect(screen, (0, 0, 0), [(20, 20), (50, 50)], 1)

    def get_cell(self, mouse_pos):
        x_mouse, y_mouse = mouse_pos
        if x_mouse < self.left or x_mouse > (self.left + self.cell_size) or \
                (y_mouse < self.top) or (y_mouse > (self.top + self.cell_size)):
            rtrn = None
        else:
            rtrn = ((x_mouse - self.left) // self.cell_size, (y_mouse - self.top) // self.cell_size)
        return rtrn

    def rtrn_shovel(self):
        return 'grass.png'


class ControlPanel:
    def __init__(self):
        self.money = 15

    def render(self, screen):
        pygame.draw.rect(screen, (150, 75, 0), [(200, 5), (100, 40)], False)
        font = pygame.font.Font(None, 30)
        text = font.render(decode_money(self.money), True, (255, 255, 255))
        screen.blit(text, (250, 25))
        screen.blit(load_image('money.jpg', 50, 50, -1), (198, 0))

    def sum_money(self, koef):
        self.money += koef * 5

    def rtrn_money(self):
        return self.money

    def minus_money(self, minus):
        self.money -= minus

    def clear(self):
        self.money = 15


# class PointsAppear:
#   def__init__(self):


EVENTMOVEENEMY = pygame.USEREVENT + 1
SUMSUNFLOWERS = pygame.USEREVENT + 2
STARTGAME = pygame.USEREVENT + 3
EATPLANTS = pygame.USEREVENT + 4

pygame.time.set_timer(STARTGAME, 12000)
pygame.time.set_timer(EVENTMOVEENEMY, 50)
pygame.time.set_timer(SUMSUNFLOWERS, 3000)


class Animals:
    def __init__(self, col):
        self.fl_chk_lose = False
        self.delay_move_animal = 45
        self.map = [0, 0, 0, 0, 0]
        self.map[random.randrange(0, 4)] = 1
        self.sp_pl = ['', '', '', '', '']
        self.y = 60
        self.x = 730
        self.top = 50
        self.fl = True
        self.attack = 0
        self.pos = 0
        self.flag_rtrn_square = False
        self.square = 0
        self.hp = 0
        self.hp_animal = 100
        self.col = col
        self.map_plants = []
        self.hp_all_animals = [[''] * 9 for _ in range(5)]
        self.sl_attack_plants = {
            'sunflower4.png': 0,
            'fighter_chamomile2.png': 100,
            'Venerina_muholovka2.png': 40,
            'potato2.png': 0}
        self.sl_hp_plants = {
            'sunflower4.png': 20,
            'fighter_chamomile2.png': 0,
            'Venerina_muholovka2.png': 20,
            'potato2.png': 70}

        for i in range(col):
            self.map_plants.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    def render(self, screen):
        if self.hp_animal > 0:
            for y in range(self.col):
                if self.map[y] == 1:
                    screen.blit(load_image('ball.png', 60, 65, -1), (self.x, self.top + self.y * y))
            if self.fl:
                self.x -= 1

    def check_go_left(self):
        return self.x > 80

    def check_left(self):
        return self.x == 80

    def check_plant(self, board):
        col = 0
        self.pos = 0
        sp_pl = []
        for sp in board:
            if self.map[col] != 0:
                square1 = (self.x - 20) // 60
                if square1 < 9:
                    if sp[square1] != '' and sp[square1] != 'grass.png':
                        sp_pl.append(sp[square1])
                        self.pos = col
                        self.square = square1
                    else:
                        sp_pl.append('')
                else:
                    sp_pl.append('')
            else:
                sp_pl.append('')
            col += 1
        if sp_pl != self.sp_pl:
            self.sp_pl = sp_pl
            if sp_pl != ['', '', '', '', '']:
                pygame.time.set_timer(EATPLANTS, 2000)
                self.reaction_on_plant()

    def reaction_on_plant(self):
        if self.fl:
            self.fl = False
        self.hp = self.sl_hp_plants[self.sp_pl[self.pos]]
        self.attack = self.sl_attack_plants[self.sp_pl[self.pos]]

    def change_plants(self):
        self.hp -= 10
        self.hp_animal -= self.attack
        if self.hp <= 0:
            self.flag_rtrn_square = True
            pygame.time.set_timer(EATPLANTS, 0)
            self.fl = True
        if self.hp_animal <= 0:
            self.fl = False
            self.clear()

    def rtrn_tile(self):
        if self.flag_rtrn_square:
            self.flag_rtrn_square = False
            ps = self.pos
            sqr = self.square
        else:
            ps = None
            sqr = None
        self.pos = 0
        self.square = 0
        return ps, sqr

    def clear(self):
        pygame.time.set_timer(EVENTMOVEENEMY, self.delay_move_animal)
        if self.delay_move_animal > 5:
            self.delay_move_animal -= 5
        self.map = [0, 0, 0, 0, 0]
        self.map[random.randrange(0, 4)] = 1
        self.sp_pl = ['', '', '', '', '']
        self.y = 60
        self.x = 730
        self.top = 50
        self.fl = True
        self.attack = 0
        self.hp = 0
        self.hp_animal = 100
        self.map_plants = []
        for i in range(self.col):
            self.map_plants.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    def chk_win(self):
        return self.delay_move_animal == 5


def main():
    size_window_length = 700
    size_window_width = 400
    quantity_length = 9
    quantity_width = 5
    size_cell = 60
    size_cell_plant = 50

    pygame.init()
    screen = pygame.display.set_mode((size_window_length, size_window_width))
    screen2 = pygame.Surface(screen.get_size())
    screen3 = pygame.Surface((60, 60))
    screen4 = pygame.Surface((screen.get_size()))
    screen5 = pygame.Surface((screen.get_size()))
    screen6 = pygame.Surface((screen.get_size()))
    screen4.blit(pygame.image.load(os.path.join('images', 'you_win.png')), (0, 0))
    screen5.blit(pygame.image.load(os.path.join('images', 'you_lose.png')), (0, 0))
    screen6.blit(pygame.image.load(os.path.join('images', 'game_start.png')), (0, 0))
    screen3.blit(load_image('grass.png', 60, 60), (0, 0))
    board = Board(quantity_length, quantity_width)
    choiceplant = ChoicePlant(4)
    shovel = Shovel()
    animals = Animals(quantity_width)
    controlpanel = ControlPanel()

    sleva = (size_window_length - quantity_length * size_cell) // 2
    sverhu = (size_window_width - quantity_width * size_cell) // 2
    board.set_view(sleva, sverhu, size_cell)
    choiceplant.set_view(10, ((size_window_width - 4 * size_cell_plant) // 2), size_cell_plant)
    pygame.display.set_caption('plants vs animals')
    running = True
    screen.fill((255, 255, 255))
    screen.blit(load_image('plit_dorogka3.jpg', size_window_length, size_window_width), (0, 0))
    board.render_cells(screen)
    choiceplant.render(screen)
    shovel.render_shovel(screen)
    controlpanel.render(screen)
    screen2.blit(screen, (0, 0))
    pygame.display.flip()
    strt_gm = False
    win = False
    lose = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == STARTGAME:
                if strt_gm == False:
                    strt_gm = True
            if not strt_gm and not win and not lose:
                screen.blit(screen6, (0, 0))
            if event.type == pygame.MOUSEBUTTONUP and not strt_gm and (win or lose):
                x, y = event.pos
                if text_x <= x <= (text_x + text_w) and text_y <= y <= (text_y + text_h):
                    strt_gm = True
                    win = False
                    lose = False
                    board.clear()
                    board.render_cells(screen2)
                    controlpanel.clear()
                    animals.clear()
                    screen.blit(screen2, (0, 0))
            if strt_gm:
                if event.type == pygame.MOUSEBUTTONUP:
                    if board.get_cell(event.pos) is not None:
                        board.get_click(event.pos, controlpanel.rtrn_money())
                        board.render_plants(screen, screen2, screen3, board.get_cell(event.pos))
                        controlpanel.minus_money(board.rtrn_minus_money())
                        controlpanel.render(screen2)
                    if choiceplant.get_cell(event.pos) is not None:
                        board.change_last_choice_plant(choiceplant.get_click(event.pos))
                    if shovel.get_cell(event.pos) is not None:
                        board.change_last_choice_plant(shovel.rtrn_shovel())
                        screen.blit(screen2, (0, 0))
                    if board.get_cell(event.pos) is None:
                        screen.blit(screen2, (0, 0))
                if event.type == EVENTMOVEENEMY:
                    if animals.check_go_left():
                        screen.blit(screen2, (0, 0))
                        animals.render(screen)
                        animals.check_plant(board.rtrn_board())
                    if animals.check_left():
                        screen.blit(screen2, (0, 0))
                if event.type == SUMSUNFLOWERS:
                    money1 = board.chk_sun_fl()
                    if money1 > 0:
                        controlpanel.sum_money(money1)
                        controlpanel.render(screen2)
                        board.chk_money()
                if event.type == EATPLANTS:
                    animals.change_plants()
                    a, b = animals.rtrn_tile()
                    if a != None:
                        board.die_plant(a, b)
                        board.render_plants(screen, screen2, screen3, (b, a))

        pygame.display.flip()
        win = animals.chk_win()
        lose = animals.check_left()
        if win:
            strt_gm = False
            font = pygame.font.Font(None, 30)
            text = font.render('Start', True, (0, 0, 0))
            text_x = 700 // 2 - text.get_width() // 2
            text_y = 400 // 2 - text.get_height() // 2 + 110
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen4, (255, 255, 255), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20))
            pygame.draw.rect(screen4, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 3)
            screen4.blit(text, (text_x, text_y))
            screen4.blit(text, (250, 25))
            screen.blit(screen4, (0, 0))
        if lose:
            strt_gm = False
            font = pygame.font.Font(None, 30)
            text = font.render('Start', True, (0, 0, 0))
            text_x = 700 // 2 - text.get_width() // 2
            text_y = 400 // 2 - text.get_height() // 2 + 110
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen5, (255, 255, 255), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20))
            pygame.draw.rect(screen5, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 3)
            screen5.blit(text, (text_x, text_y))
            screen5.blit(text, (250, 25))
            screen.blit(screen5, (0, 0))


if __name__ == "__main__":
    main()