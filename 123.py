import os
import random
import sys

import pygame

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
# Начиная со следующий строчки, идёт код, связанный с кнопками
font = pygame.font.SysFont('Arial', 40)

objects = []


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False

        self.fillColors = {
            'normal': 'blue',
            'hover': '#674666',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def call_func1():
    return


def call_func2():
    return


def call_func3():
    return


start_button = Button(width / 2 - 150, height / 5, 300, 75, 'Старт!', call_func1)
history_button = Button(width / 2 - 150, height / 5 + height / 5, 300, 75, 'История', call_func2)
exit_button = Button(width / 2 - 150, height / 5 + 2 * height / 5, 300, 75, 'Выйти', call_func3)

# Конец кода с кнопками

def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (size))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        for elem in objects:  # Отображаем кнопки на экране
            elem.process()
            if start_button.alreadyPressed:  # Функция кнопки старт
                return
            if exit_button.alreadyPressed:  # Функция кнопки выйти
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level('map0.txt')

tile_images = {
    'wall': pygame.transform.scale(load_image('winter_wall.png'), (50, 50)),
    'empty': pygame.transform.scale(load_image('snow1.png'), (90, 90)),
    'tree': pygame.transform.scale(load_image('winter_tree.png'), (50, 50)),
    'tree1': pygame.transform.scale(load_image('winter_tree1.png'), (50, 50)),
}
player_image = pygame.transform.scale(load_image('mainch.png'), (43, 43))

tile_width = tile_height = 50


class DecorCreate(pygame.sprite.Sprite):  # Класс для создания декораторов
    def __init__(self, pos_x, pos_y, file_name, size):
        super().__init__(decor_group, all_sprites)
        self.image = pygame.transform.scale(load_image(file_name), (size))  # Adjust the size as needed
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Black(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(load_image('black_light.png'),
                                            (4000, 4000))  # Загрузка и масштабирование изображения
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        self.rect.x = player.rect.x - 2000
        self.rect.y = player.rect.y - 2000


class BlockTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(block_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.vy = 0
        self.vx = 0
        self.move = False
        self.health = 100
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def draw(self):
        self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57)
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # NEW
        pygame.draw.rect(screen, (0, 128, 0),
                         (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))  # NEW

    def update(self):
        if self.move:
            old_x = self.rect.x
            old_y = self.rect.y

            if self.rect.x + self.vx <= width - width // 6 and self.rect.x + self.vx >= width // 6:
                self.rect.x += self.vx
            else:
                if self.rect.x + self.vx < width // 5:
                    for sprite in tiles_group:
                        sprite.rect.x -= self.vx

                    for sprite in block_tiles_group:
                        sprite.rect.x -= self.vx

                    for sprite in decor_group:
                        sprite.rect.x -= self.vx

                if self.rect.x + self.vx > width - width // 5:
                    for sprite in tiles_group:
                        sprite.rect.x -= self.vx

                    for sprite in block_tiles_group:
                        sprite.rect.x -= self.vx

                    for sprite in decor_group:
                        sprite.rect.x -= self.vx
                collision_sprites = pygame.sprite.spritecollide(self, block_tiles_group, False)
                for sprite in collision_sprites:
                    if sprite != self:
                        for sprite in tiles_group:
                            sprite.rect.x += self.vx

                        for sprite in block_tiles_group:
                            sprite.rect.x += self.vx

                        for sprite in decor_group:
                            sprite.rect.x += self.vx
            if self.rect.y + self.vy <= height - height // 6 and self.rect.y + self.vy >= height // 6:
                self.rect.y += self.vy
            else:
                if self.rect.y + self.vy < height // 5:
                    for sprite in tiles_group:
                        sprite.rect.y -= self.vy

                    for sprite in block_tiles_group:
                        sprite.rect.y -= self.vy

                    for sprite in decor_group:
                        sprite.rect.y -= self.vy

                if self.rect.y + self.vy > height - height // 5:
                    for sprite in tiles_group:
                        sprite.rect.y -= self.vy

                    for sprite in block_tiles_group:
                        sprite.rect.y -= self.vy

                    for sprite in decor_group:
                        sprite.rect.y -= self.vy

                # Проверка на столкновение с препятствиями
                collision_sprites = pygame.sprite.spritecollide(self, block_tiles_group, False)
                for sprite in collision_sprites:
                    if sprite != self:
                        for sprite in tiles_group:
                            sprite.rect.y += self.vy

                        for sprite in block_tiles_group:
                            sprite.rect.y += self.vy

                        for sprite in decor_group:
                            sprite.rect.y += self.vy
            collision_sprites = pygame.sprite.spritecollide(self, block_tiles_group, False)
            for sprite in collision_sprites:
                if sprite != self:
                    self.rect.x = old_x
                    self.rect.y = old_y


player = None
decor_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
block_tiles_group = pygame.sprite.Group()
black_l = Black(0, 0)
bonfire = DecorCreate(4, 2, 'bonfire.png', (80, 80))
house = DecorCreate(8.3, 0.5, 'wooden_house.png', (120, 120))
big_trees = [(0, 1), (6, 0), (1, 6), (16, 4)]  # Массив с координатами деревьев
for e in big_trees:  # Проходимся по массиву и создаём деревья
    new_tree = DecorCreate(e[0], e[1], 'winter_tree.png', (150, 150))


def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == '!':
                Tile('empty', x, y)
                Tile('tree', x, y)
            if level[y][x] == '1':
                Tile('empty', x, y)
                Tile('tree1', x, y)
            elif level[y][x] == '#':
                BlockTile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('map0.txt'))

# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()
running = True
clock = pygame.time.Clock()
player.draw()
sign_image = pygame.transform.scale(load_image('sign.png'), (450, 120))
sign_rect = sign_image.get_rect(center=(700, 500))

text = ("""Привет, незнакомец! Ты попал 
в лабиринт, который находится 
вне времени и пространства...""")
displayed_text = ""
counter = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.move = True
            if event.key == pygame.K_LEFT:
                player.vx = -8
            elif event.key == pygame.K_RIGHT:
                player.vx = 8
            elif event.key == pygame.K_UP:
                player.vy = -8
            elif event.key == pygame.K_DOWN:
                player.vy = 8
        if event.type == pygame.KEYUP:
            player.move = False
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.vx = 0
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                player.vy = 0

    player.update()
    black_l.update()
    all_sprites.update()
    screen.fill('Blue')

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    block_tiles_group.draw(screen)
    decor_group.draw(screen)
    player_group.draw(screen)
    screen.blit(sign_image, sign_rect)
    if counter < len(text):
        displayed_text += text[counter]
        counter += 1
    blit_text(screen, displayed_text, (490, 450), pygame.font.Font(None, 36))

    clock.tick(30)
    pygame.display.flip()

pygame.quit()