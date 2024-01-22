import os
import random
import sys
import time
import datetime
import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()
start_time = pygame.time.get_ticks()
end_time = 0

size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
# Начиная со следующий строчки, идёт код, связанный с кнопками
font = pygame.font.SysFont('Arial', 40)
wind_sound = pygame.mixer.Sound("data/wind.ogg")
step_sound = pygame.mixer.Sound("data/step.ogg")
enemy_punch_sound = pygame.mixer.Sound("data/enemy_punch.ogg")
eat_sound = pygame.mixer.Sound("data/eat.wav")
start_menu_music = pygame.mixer.Sound("data/start_music.ogg")
hero_death_music = pygame.mixer.Sound("data/hero_death.ogg")
hero_death_sound = pygame.mixer.Sound("data/hero_death_sound.ogg")
objects = []
number_of_apples = 0

left = False
right = False
animCount = 0


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
# history_button = Button(width / 2 - 150, height / 5 + height / 5, 300, 75, 'История', call_func2)
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


fon = pygame.transform.scale(load_image('fon.jpg'), (size))

def win_screeen():
    pygame.mixer.pause()
    pygame.draw.rect(fon, (255, 130, 0, 65), (0, 0, width, height))
    screen.blit(fon, (0, 0))
    blit_text(screen, 'ВЫ  ПРОШЛИ  ИГРУ!', (width // 2 - 400, height // 2 - 70), pygame.font.Font(None, 150),
              color=pygame.Color('black'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
def end_screen():
    hero_death_music.play()
    hero_death_sound.play()
    pygame.draw.rect(fon, (255, 0, 0, 65), (0, 0, width, height))
    screen.blit(fon, (0, 0))
    blit_text(screen, 'GAME     OVER', (width // 2 - 400, height // 2 - 70), pygame.font.Font(None, 150),
              color=pygame.Color('black'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    start_menu_music.play(-1)
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        for elem in objects:  # Отображаем кнопки на экране
            elem.process()
            if start_button.alreadyPressed:  # Функция кнопки старт
                wind_sound.set_volume(0.5)
                wind_sound.play(-1)
                start_menu_music.stop()
                return
            if exit_button.alreadyPressed:  # Функция кнопки выйти
                terminate()
            # if history_button.alreadyPressed:
            #     file = open('data/history_results.txt', 'r', encoding='utf-16')
            #     for line in file:
            #         instructText = font.render(line, True, 'WHITE')
            #         screen.blit(instructText,
            #                 ((400 - (instructText.get_width() / 2)), (300 - (instructText.get_height() / 2))))
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
level02 = load_level('map1.txt')

blocks = []
for i in range(100, 107):
    blocks.append(pygame.transform.scale(load_image(f'blocks/image_part_{i}.png'), (50, 50)))

tile_images = {
    'wall': pygame.transform.scale(load_image('winter_wall.png'), (50, 50)),
    'empty': pygame.transform.scale(load_image('snow1.png'), (90, 90)),
    'tree': pygame.transform.scale(load_image('winter_tree.png'), (50, 50)),
    'tree1': pygame.transform.scale(load_image('winter_tree1.png'), (50, 50)),
    'block_door': blocks,
    'sand_wall': pygame.transform.scale(load_image('sand_wall.png'), (50, 50)),
    'sand': pygame.transform.scale(load_image('sand1.png'), (50, 50))
}
level1on = True
player_size = 60, 60
walkLeft = [pygame.transform.scale(load_image('hero_left/5.png'), (player_size)),
            pygame.transform.scale(load_image('hero_left/4.png'), (player_size)),
            pygame.transform.scale(load_image('hero_left/3.png'), (player_size)),
            pygame.transform.scale(load_image('hero_left/2.png'), (player_size)),
            pygame.transform.scale(load_image('hero_left/1.png'), (player_size))]

walkRight = [pygame.transform.scale(load_image('hero_right/1.png'), (player_size)),
             pygame.transform.scale(load_image('hero_right/2.png'), (player_size)),
             pygame.transform.scale(load_image('hero_right/3.png'), (player_size)),
             pygame.transform.scale(load_image('hero_right/4.png'), (player_size)),
             pygame.transform.scale(load_image('hero_right/5.png'), (player_size))]

hero_Attack = [pygame.transform.scale(load_image('hero_attack/1.png'), (player_size)),
               pygame.transform.scale(load_image('hero_attack/2.png'), (player_size)),
               pygame.transform.scale(load_image('hero_attack/3.png'), (player_size))]

portal_img = [pygame.transform.scale(load_image('portal/1.png'), (50, 80)),
              pygame.transform.scale(load_image('portal/2.png'), (50, 80)),
              pygame.transform.scale(load_image('portal/3.png'), (50, 80)),
              pygame.transform.scale(load_image('portal/4.png'), (50, 80))]

hero_Stand = [pygame.transform.scale(load_image('stop_hero.png'), (33, 33))]
hero_Dead = [pygame.transform.scale(load_image('hero_dead.png'), (50, 50))]

enemy_size = 280, 280
enemyAttack = [pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_008.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_007.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_006.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_005.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_004.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_004 (1).png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_003.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_002.png'), (enemy_size)),
               pygame.transform.scale(load_image('Fantasy Warrior/attack/image_part_001.png'), (enemy_size))]

enemyStand = [pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_001.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_002.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_003.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_004.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_005.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_006.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_007.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_008.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_009.png'), (enemy_size)),
              pygame.transform.scale(load_image('Fantasy Warrior/idle/image_part_010.png'), (enemy_size))]

tile_width = tile_height = 50


class DecorCreate(pygame.sprite.Sprite):  # Класс для создания декораторов
    def __init__(self, pos_x, pos_y, file_name, size):
        super().__init__(decor_group, all_sprites)
        self.image = pygame.transform.scale(load_image(file_name), (size))  # Adjust the size as needed
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, file_name, size):
        super().__init__(portal_group, all_sprites)
        self.images = portal_img
        self.index = 0
        self.image = pygame.transform.scale(portal_img[self.index],
                                            (50, 80))  # 'image' is the current image of the animation.
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y)

        self.animation_time = 0.05
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, anim, str_key):
        super().__init__(tiles_group, all_sprites)
        self.anim_work = anim
        self.str_key = str_key
        if self.anim_work:
            self.anim_work = True
            self.images = blocks
            self.index = 0
            self.image = pygame.transform.scale(blocks[self.index],
                                                (90, 90))  # 'image' is the current image of the animation.
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 15, tile_height * pos_y)

            self.animation_time = 0.05
            self.current_time = 0

            self.animation_frames = 6
            self.current_frame = 0

        else:
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    def update(self, dt):
        if self.anim_work:
            self.current_time += dt
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]
        else:
            if level1on:
                self.image = tile_images['empty']
            else:
                self.image = tile_images['sand']


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
    def __init__(self, tile_type, pos_x, pos_y):  # str_key нужен для привязки двери к определенному врагу
        super().__init__(block_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class HealingApple(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, file_name, size):
        super().__init__(healing_apples_group, all_sprites)
        self.image = pygame.transform.scale(load_image(file_name), (size))  # Adjust the size as needed
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def heal(self):
        global number_of_apples
        if self.rect.colliderect(player.rect):
            k = 0
            eat_sound.play()
            while k < 30:
                if player.health < 100:
                    player.health += 1
                k += 1
            number_of_apples += 1
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.vy = 0
        self.vx = 0
        self.move = False
        self.can_move = True
        self.health = 100
        images = walkLeft + walkRight + hero_Stand + hero_Dead
        if self.health <= 0:
            self.images = hero_Dead
            end_time = pygame.time.get_ticks()
        self.images = images
        self.images_right = images[0:5]
        self.images_left = images[5:10]
        self.images_stop = [images[-2]]
        self.images_dead = [images[-1]]
        self.index = 0
        self.image = pygame.transform.scale(images[self.index],
                                            (30, 30))  # 'image' is the current image of the animation.
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y)

        self.animation_time = 0.05
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def attack(self):
        # self.images = hero_Attack
        enemies = pygame.sprite.spritecollide(self, enemy_group, False)
        for enemy in enemies:
            enemy.health -= 50

    def update_time_dependent(self, dt):
        if self.health <= 0:
            self.images = hero_Dead
            self.index = 0
            self.image = self.images[0]
        else:
            if self.vx < 0 or self.vy > 0 and self.health != 0:  # Use the right images if sprite is moving right.
                self.images = self.images_right
            elif self.vx > 0 or self.vy < 0 and self.health != 0:
                self.images = self.images_left
            elif self.vx == 0 and self.vy == 0 and self.health != 0:
                self.images = self.images_stop

            self.current_time += dt
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

    def update_frame_dependent(self):
        if self.health <= 0:
            self.images = hero_Dead
            self.index = 0
            self.image = self.images[0]
        else:
            if self.vx < 0 and self.health != 0:  # Use the right images if sprite is moving right.
                self.images = self.images_right
            elif self.vx > 0 and self.health != 0:
                self.images = self.images_left
            elif self.vx == 0 and self.vy == 0 and self.health != 0:
                self.images = self.images_stop

            self.current_frame += 1
            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

    def draw(self, surf):
        if self.health < 0:
            self.health = 0
        BAR_LENGTH_1 = 100
        BAR_HEIGHT_1 = 15
        fill_1 = (self.health / 100) * BAR_LENGTH_1
        outline_rect_1 = pygame.Rect(self.rect.x - 45 / 2, self.rect.y - 25, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.x - 45 / 2, self.rect.y - 25, fill_1, BAR_HEIGHT_1)
        if self.health >= 50:
            pygame.draw.rect(surf, 'green', fill_rect_1)
        else:
            pygame.draw.rect(surf, 'red', fill_rect_1)
        pygame.draw.rect(surf, 'white', outline_rect_1, 2)

    def update(self):
        global start_time
        global end_time
        if self.health <= 0:
            self.images = hero_Dead
            self.index = 0
            self.image = self.images[0]
            self.can_move = False
            end_time = pygame.time.get_ticks()
            delta_time = end_time - start_time
        else:
            if self.move:
                old_x = self.rect.x
                old_y = self.rect.y

                if self.rect.x + self.vx <= width - width // 3 and self.rect.x + self.vx >= width // 3:  # Движение "внутри рамки" по горизонтали
                    self.rect.x += self.vx
                else:  # Если персонаж "выходит за рамку" по горизонтали
                    if self.rect.x + self.vx < width // 3:  # Движение налево
                        for sprite in tiles_group:
                            sprite.rect.x -= self.vx

                        for sprite in block_tiles_group:
                            sprite.rect.x -= self.vx

                        for sprite in decor_group:
                            sprite.rect.x -= self.vx

                        for sprite in enemy_group:
                            sprite.rect.x -= self.vx

                        for sprite in healing_apples_group:
                            sprite.rect.x -= self.vx

                        for sprite in portal_group:
                            sprite.rect.x -= self.vx

                    if self.rect.x + self.vx > width - width // 3:  # Движение направо
                        for sprite in tiles_group:
                            sprite.rect.x -= self.vx

                        for sprite in block_tiles_group:
                            sprite.rect.x -= self.vx

                        for sprite in decor_group:
                            sprite.rect.x -= self.vx

                        for sprite in enemy_group:
                            sprite.rect.x -= self.vx

                        for sprite in healing_apples_group:
                            sprite.rect.x -= self.vx

                        for sprite in portal_group:
                            sprite.rect.x -= self.vx
                    collision_sprites = [
                        sprite for sprite in pygame.sprite.spritecollide(self, tiles_group, False)  # коллизия с дверьми
                        if sprite.anim_work
                    ]
                    collision_sprites += pygame.sprite.spritecollide(self, block_tiles_group, False)
                    for sprite in collision_sprites:
                        if sprite != self:
                            for sprite in tiles_group:
                                sprite.rect.x += self.vx

                            for sprite in block_tiles_group:
                                sprite.rect.x += self.vx

                            for sprite in decor_group:
                                sprite.rect.x += self.vx

                            for sprite in enemy_group:
                                sprite.rect.x += self.vx

                            for sprite in healing_apples_group:
                                sprite.rect.x += self.vx

                            for sprite in portal_group:
                                sprite.rect.x += self.vx

                if self.rect.y + self.vy <= height - height // 2 and self.rect.y + self.vy >= height // 2:  # Движение "внутри рамки" по вертикали
                    self.rect.y += self.vy
                else:  # Если персонаж "выходит за рамку" по вертикали
                    if self.rect.y + self.vy < height // 2:  # Движение наверх
                        for sprite in tiles_group:
                            sprite.rect.y -= self.vy

                        for sprite in block_tiles_group:
                            sprite.rect.y -= self.vy

                        for sprite in decor_group:
                            sprite.rect.y -= self.vy

                        for sprite in enemy_group:
                            sprite.rect.y -= self.vy

                        for sprite in healing_apples_group:
                            sprite.rect.y -= self.vy

                        for sprite in portal_group:
                            sprite.rect.y -= self.vy

                    if self.rect.y + self.vy > height - height // 3:  # Движение вниз
                        for sprite in tiles_group:
                            sprite.rect.y -= self.vy

                        for sprite in block_tiles_group:
                            sprite.rect.y -= self.vy

                        for sprite in decor_group:
                            sprite.rect.y -= self.vy

                        for sprite in enemy_group:
                            sprite.rect.y -= self.vy

                        for sprite in healing_apples_group:
                            sprite.rect.y -= self.vy

                        for sprite in portal_group:
                            sprite.rect.y -= self.vy

                    # Проверка на столкновение с препятствиями
                    collision_sprites = [
                        sprite for sprite in pygame.sprite.spritecollide(self, tiles_group, False)  # коллизия с дверьми
                        if sprite.anim_work
                    ]
                    collision_sprites += pygame.sprite.spritecollide(self, block_tiles_group, False)
                    for sprite in collision_sprites:
                        if sprite != self:
                            for sprite in tiles_group:
                                sprite.rect.y += self.vy

                            for sprite in block_tiles_group:
                                sprite.rect.y += self.vy

                            for sprite in decor_group:
                                sprite.rect.y += self.vy

                            for sprite in enemy_group:
                                sprite.rect.y += self.vy

                            for sprite in healing_apples_group:
                                sprite.rect.y += self.vy

                            for sprite in portal_group:
                                sprite.rect.y += self.vy

                collision_sprites = [
                    sprite for sprite in pygame.sprite.spritecollide(self, tiles_group, False)  # коллизия с дверьми
                    if sprite.anim_work
                ]
                collision_sprites += pygame.sprite.spritecollide(self, block_tiles_group, False)
                for sprite in collision_sprites:
                    if sprite != self:
                        self.rect.x = old_x
                        self.rect.y = old_y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, str_key):  # str_key - массив с координатами нужных дверей
        super().__init__(enemy_group, all_sprites)
        self.make_check = True  # проверять ли двери после смерти (для оптимизации)
        self.str_key_block = str_key
        self.move = False
        self.health = 100
        self.can_attack = False
        images = enemyAttack + enemyStand
        self.rect = pygame.Rect((pos_x, pos_y), (160, 160))
        self.images = images
        self.images_attack = images[0:8]
        self.images_idle = images[10:16]
        self.index = 0
        self.last_attack_time = 0

        self.image = pygame.transform.scale(images[self.index],
                                            (5, 5))  # 'image' is the current image of the animation.
        # Переопределяем координаты коллизии

        self.animation_time = 0.05
        self.current_time = 0

        self.timee = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        if self.rect.colliderect(player.rect) and player.health != 0:
            # Check if it has been at least 5 seconds since the last attack
            if self.can_attack:
                self.images = self.images_attack

            else:
                self.images = self.images_idle
        else:
            self.images = self.images_idle

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            if self.image == self.images_attack[0]:
                self.last_attack_time = self.timee
                player.health -= 10
                enemy_punch_sound.play()

    def draw(self, surf):
        if self.health < 0:
            self.health = 0
        BAR_LENGTH_1 = 100
        BAR_HEIGHT_1 = 15
        fill_1 = (self.health / 100) * BAR_LENGTH_1
        outline_rect_1 = pygame.Rect(self.rect.x + 110, self.rect.y + 70, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.x + 110, self.rect.y + 70, fill_1, BAR_HEIGHT_1)
        if self.health >= 50:
            pygame.draw.rect(surf, 'green', fill_rect_1)
        else:
            pygame.draw.rect(surf, 'red', fill_rect_1)
        pygame.draw.rect(surf, 'white', outline_rect_1, 2)

    def update_frame_dependent(self):
        pass

    def update(self):
        k = 0
        self.timee = pygame.time.get_ticks()
        if self.timee - self.last_attack_time >= 1000:
            self.can_attack = True
        else:
            self.can_attack = False
        if self.health == 0 and self.make_check:
            for x_y_key in self.str_key_block:
                for block in tiles_group:
                    if block.anim_work == True:
                        if block.str_key == str(x_y_key):
                            block.anim_work = False
                            k += 1

        if k == 2:  # если обе двери уничтожены, больше не проверять их наличие
            self.make_check = False
        if self.health == 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, str_key):  # str_key - массив с координатами нужных дверей
        super().__init__(enemy_group, all_sprites)
        self.make_check = True  # проверять ли двери после смерти (для оптимизации)
        self.str_key_block = str_key
        self.move = False
        self.health = 300
        self.can_attack = False
        images = enemyAttack + enemyStand
        self.rect = pygame.Rect((pos_x, pos_y), (480, 480))
        self.images = images
        self.images_attack = images[0:8]
        self.images_idle = images[10:16]
        self.index = 0
        self.last_attack_time = 0

        self.image = pygame.transform.scale(images[self.index],
                                            (5, 5))  # 'image' is the current image of the animation.
        # Переопределяем координаты коллизии

        self.animation_time = 0.05
        self.current_time = 0

        self.timee = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        if self.rect.colliderect(player.rect) and player.health != 0:
            # Check if it has been at least 5 seconds since the last attack
            if self.can_attack:
                self.images = self.images_attack

            else:
                self.images = self.images_idle
        else:
            self.images = self.images_idle

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            if self.image == self.images_attack[0]:
                self.last_attack_time = self.timee
                player.health -= 10
                enemy_punch_sound.play()

    def draw(self, surf):
        if self.health < 0:
            self.health = 0
        BAR_LENGTH_1 = 100
        BAR_HEIGHT_1 = 15
        fill_1 = (self.health / 100) * BAR_LENGTH_1
        outline_rect_1 = pygame.Rect(self.rect.x + 110, self.rect.y + 70, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.x + 110, self.rect.y + 70, fill_1, BAR_HEIGHT_1)
        if self.health >= 50:
            pygame.draw.rect(surf, 'green', fill_rect_1)
        else:
            pygame.draw.rect(surf, 'red', fill_rect_1)
        pygame.draw.rect(surf, 'white', outline_rect_1, 2)

    def update_frame_dependent(self):
        pass

    def update(self):
        k = 0
        self.timee = pygame.time.get_ticks()
        if self.timee - self.last_attack_time >= 1000:
            self.can_attack = True
        else:
            self.can_attack = False
        if self.health == 0 and self.make_check:
            for x_y_key in self.str_key_block:
                for block in tiles_group:
                    if block.anim_work == True:
                        if block.str_key == str(x_y_key):
                            block.anim_work = False
                            k += 1

        if k == 2:  # если обе двери уничтожены, больше не проверять их наличие
            self.make_check = False
        if self.health == 0:
            self.kill()


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
                Tile('empty', x, y, False, '')
            if level[y][x] == '!':
                Tile('empty', x, y, False, '')
                Tile('tree', x, y, False, '')
            if level[y][x] == '1':
                Tile('empty', x, y, False, '')
                Tile('tree1', x, y, False, '')
            elif level[y][x] == '#':
                BlockTile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y, False, '')
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y, True, (str(x) + str(y)))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def level1():
    # группа, содержащая все спрайты
    all_sprites = pygame.sprite.Group()
    running = True
    clock = pygame.time.Clock()
    sign_image = pygame.transform.scale(load_image('sign.png'), (450, 120))
    sign_rect = sign_image.get_rect(center=(700, 500))

    text0 = ("""Привет, незнакомец! Ты попал 
    в лабиринт, который находится 
    вне времени и пространства...""")
    text1 = ("""Чтобы выйти отсюда, тебе 
    придётся устранить 
    босса...""")
    text2 = ("""Однако к нему не так
    просто подобраться: тебя
    встретит его охрана""")
    displayed_text = ""
    counter = 0
    counter_text = 0
    while running:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        if portal.rect.colliderect(player.rect):
            portal_group.empty()
            tiles_group.empty()
            enemy_group.empty()
            decor_group.empty()
            player_group.empty()
            healing_apples_group.empty()
            block_tiles_group.empty()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack()
                player.image = hero_Attack[2]
            if event.type == pygame.KEYDOWN and player.can_move:
                player.move = True
                if event.key == pygame.K_s:
                    player.attack()
                    player.image = hero_Attack[2]
                if event.key == pygame.K_LEFT:
                    step_sound.play(-1)
                    player.vx = -8
                    left = True
                    right = False
                elif event.key == pygame.K_RIGHT:
                    step_sound.play(-1)
                    player.vx = 8
                    left = False
                    right = True
                elif event.key == pygame.K_UP:
                    step_sound.play(-1)
                    player.vy = -8
                    left = False
                    right = True
                elif event.key == pygame.K_DOWN:
                    step_sound.play(-1)
                    player.vy = 8
                    left = False
                    right = True
                else:
                    left = False
                    right = False
                    animCount = 0
            if event.type == pygame.KEYUP:
                step_sound.stop()
                player.move = False
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.vx = 0
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player.vy = 0

        all_sprites.update(dt)
        for enemy_class in enemy_group:  # Действие для каждого врага
            enemy_class.update()
            enemy_class.draw(screen)
            enemy_class.update_time_dependent(dt)
            enemy_class.update_frame_dependent()

        player.update()
        portal.update(dt)
        player.update_time_dependent(dt)
        player.update_frame_dependent()
        black_l.update()
        all_sprites.update()
        screen.fill('Black')
        for block in tiles_group:
            block.update(dt)
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        block_tiles_group.draw(screen)
        enemy_group.draw(screen)
        decor_group.draw(screen)
        healing_apples_group.draw(screen)
        portal_group.draw(screen)
        for apple in healing_apples_group:
            apple.heal()
        for enemy_class in enemy_group:  # Действие для каждого врага
            enemy_class.draw(screen)

        player_group.draw(screen)
        player.draw(screen)
        screen.blit(sign_image, sign_rect)
        text = [text0, text1, text2][counter_text]
        if counter < len(text) + 15:
            if counter < len(text):
                displayed_text += text[counter]
            counter += 1
        if counter == len(text) + 15 and counter_text < 2:
            counter = 0
            counter_text += 1
            displayed_text = ''
        blit_text(screen, displayed_text, (490, 450), pygame.font.Font(None, 36))
        if player.health <= 0:
            file = open('data/history_results.txt', 'r', encoding='utf-16')
            text = file.readlines()
            file = open('data/history_results.txt', 'w', encoding='utf-16')
            file.write(f'{''.join(text)}\n'
                       f'----------------------------------------------------\n'
                       f'----------------------------------------------------\n'
                       f'----------------------------------------------------\n'
                       f'{str(datetime.datetime.now())}\n'
                       f'Время в игре: {round(end_time / 1000 - 3, 1)} секунд\n'
                       f'Статус игры: Поражение')
            player.index = 0
            player.images = player.images_dead
            player.image = player.images[0]
            player_group.draw(screen)
            player.can_move = False
            pygame.mixer.pause()
            end_screen()
            break
        clock.tick(FPS)
        pygame.display.flip()


def level2():
    global level1on
    level1on = False
    wind_sound.stop()
    for y in range(len(level)):
        for x in range(len(level02[y])):
            if level02[y][x] == '.':
                Tile('sand', x, y, False, '')
            if level02[y][x] == '!':
                Tile('sand', x, y, False, '')
                Tile('tree', x, y, False, '')
            if level02[y][x] == '1':
                Tile('sand', x, y, False, '')
                Tile('tree1', x, y, False, '')
            elif level02[y][x] == '#':
                BlockTile('sand_wall', x, y)
            elif level02[y][x] == '$':
                Tile('sand', x, y, True, (str(x) + str(y)))
    global player
    global level_x
    global level_y
    black_l = Black(0, 0)
    enemy1 = Enemy(480, 110, (134, 135))
    enemy2 = Enemy(1100, 160, (255, 256))
    boss = Boss(300, 400, (255, 256))
    big_trees = [(0, 1), (2, 0), (4, 0), (6, 0), (19, 3), (15, 3), (-0.3, 2), (0, 3),
                 (0.3, 4), (3, 5), (5, 5), (7, 5), (1, 5), (21, 7)]  # Массив с координатами деревьев
    apple = HealingApple(10, 10, 'apple.png', (70, 40))

    #for e in big_trees:  # Проходимся по массиву и создаём деревья
        #new_tree = DecorCreate(e[0], e[1], 'winter_tree.png', (150, 150))
    # группа, содержащая все спрайты
    all_sprites = pygame.sprite.Group()
    running = True
    clock = pygame.time.Clock()
    while running:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack()
                player.image = hero_Attack[2]
            if event.type == pygame.KEYDOWN and player.can_move:
                player.move = True
                if event.key == pygame.K_s:
                    player.attack()
                    player.image = hero_Attack[2]
                if event.key == pygame.K_LEFT:
                    step_sound.play(-1)
                    player.vx = -8
                    left = True
                    right = False
                elif event.key == pygame.K_RIGHT:
                    step_sound.play(-1)
                    player.vx = 8
                    left = False
                    right = True
                elif event.key == pygame.K_UP:
                    step_sound.play(-1)
                    player.vy = -8
                    left = False
                    right = True
                elif event.key == pygame.K_DOWN:
                    step_sound.play(-1)
                    player.vy = 8
                    left = False
                    right = True
                else:
                    left = False
                    right = False
                    animCount = 0
            if event.type == pygame.KEYUP:
                step_sound.stop()
                player.move = False
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.vx = 0
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player.vy = 0

        all_sprites.update(dt)
        for enemy_class in enemy_group:  # Действие для каждого врага
            enemy_class.update()
            enemy_class.draw(screen)
            enemy_class.update_time_dependent(dt)
            enemy_class.update_frame_dependent()

        player.update()
        portal.update(dt)
        player.update_time_dependent(dt)
        player.update_frame_dependent()
        black_l.update()
        all_sprites.update()
        screen.fill('Black')
        for block in tiles_group:
            block.update(dt)
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        block_tiles_group.draw(screen)
        enemy_group.draw(screen)
        decor_group.draw(screen)
        healing_apples_group.draw(screen)
        portal_group.draw(screen)
        for apple in healing_apples_group:
            apple.heal()
        for enemy_class in enemy_group:  # Действие для каждого врага
            enemy_class.draw(screen)

        player_group.draw(screen)
        player.draw(screen)
        if boss.health <= 0:
            file = open('data/history_results.txt', 'r', encoding='utf-16')
            text = file.readlines()
            file = open('data/history_results.txt', 'w', encoding='utf-16')
            file.write(
                f'----------------------------------------------------\n'
                f'----------------------------------------------------\n'
                f'----------------------------------------------------\n'
                f'{str(datetime.datetime.now())}\n'
                f'Время в игре: {round(end_time / 1000 - 3, 1)} секунд\n'
                f'Статус игры: Победа\n'
                f'{''.join(text)}')
            win_screeen()
            pygame.mixer.pause()
            break
        if player.health <= 0:
            file = open('data/history_results.txt', 'r', encoding='utf-16')
            text = file.readlines()
            file = open('data/history_results.txt', 'w', encoding='utf-16')
            file.write(
                       f'----------------------------------------------------\n'
                       f'----------------------------------------------------\n'
                       f'----------------------------------------------------\n'
                       f'{str(datetime.datetime.now())}\n'
                       f'Время в игре: {round(end_time / 1000 - 3, 1)} секунд\n'
                       f'Статус игры: Поражение\n'
                        f'{''.join(text)}')
            player.index = 0
            player.images = player.images_dead
            player.image = player.images[0]
            player_group.draw(screen)
            player.can_move = False
            pygame.mixer.pause()
            file = open('history_results.txt', 'w', encoding='utf-8')
            file_check = open('history_results.txt', 'r', encoding='utf-8')
            if file_check.readlines() == '':
                file.write(f'Время в игре: {round(end_time / 1000 - 3, 1)} секунд')
            end_screen()
            break
        clock.tick(FPS)
        pygame.display.flip()


player = None
decor_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
block_tiles_group = pygame.sprite.Group()
healing_apples_group = pygame.sprite.Group()
black_l = Black(0, 0)
enemy1 = Enemy(480, 110, (134, 135))
enemy2 = Enemy(1100, 160, (255, 256))
bonfire = DecorCreate(4, 3, 'bonfire.png', (80, 80))
house = DecorCreate(8.3, 0.5, 'wooden_house.png', (120, 120))
big_trees = [(0, 1), (2, 0), (4, 0), (6, 0), (19, 3), (15, 3), (-0.3, 2), (0, 3),
             (0.3, 4), (3, 5), (5, 5), (7, 5), (1, 5), (21, 7)]  # Массив с координатами деревьев
apple = HealingApple(7, 5, 'apple.png', (70, 40))
portal = Portal(35, 8, portal_img, (50, 80))
for e in big_trees:  # Проходимся по массиву и создаём деревья
    new_tree = DecorCreate(e[0], e[1], 'winter_tree.png', (150, 150))
player, level_x, level_y = generate_level(load_level('map0.txt'))
level1()
player, level_x, level_y = generate_level(load_level('map1.txt'))
level2()
pygame.quit()

#54