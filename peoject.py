import os
import pygame
import sys
import random

FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 800, 600
STEP = 10
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
player = None
lvl_name = "lvl1.txt"
ship_name = "ship2.png"

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_game(level=lvl_name):
    fon = pygame.transform.scale(load_image(level[0:-4] + ".jpg"), (WIDTH, HEIGHT))
    running = True
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.rect.x += STEP
                if event.key == pygame.K_LEFT:
                    player.rect.x -= STEP
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.x, player.rect.y, -1)
                    bullet.shoot()
                    player.damage()
            if event.type == pygame.USEREVENT:
                shooting_mob()

        screen.blit(fon, (0, 0))
        all_sprites.update()
        bullet_group.update()
        all_sprites.draw(screen)
        bullet_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def level_change():
    print('Выбор уровня')


def ship_change():
    print("Выбор корабля")


def rules():
    print("Правила")


def terminate():
    pygame.quit()
    sys.exit()


def shooting_mob():
    shoot_mob = random.choice(enemy_group.sprites())
    bullet = Bullet(shoot_mob.rect.x, shoot_mob.rect.y, 1)
    bullet.shoot()


def start_screen():
    intro_text = ["",
                  "",
                  "",
                  "",
                  "                                             STAR SHIP"]

    fon = pygame.transform.scale(load_image('start.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        pygame.sprite.Sprite.__init__(self)
        self.vel = vel
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 5
        self.rect.centerx = x + 15

    def update(self):
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.y < 0:
            self.kill()
        if self.rect.y > 600:
            self.kill()
        if self.vel < 0:
            if not pygame.sprite.spritecollide(self, tiles_group, False):
                self.rect.y += 2 * self.vel
            else:
                self.kill()
                pygame.sprite.spritecollide(self, tiles_group, False)[0].damage()
        if self.vel > 0:
            if not pygame.sprite.spritecollide(self, player_group, False):
                self.rect.y += 3 * self.vel
            else:
                self.kill()
                pygame.sprite.spritecollide(self, player_group, False)[0].damage()

    def shoot(self):
        if len(bullet_group) < 5:
            bullet = Bullet(self.rect.x, self.rect.y, self.vel)
            all_sprites.add(bullet)
            bullet_group.add(bullet)


def menu():
    menu_text = ["           Меню",
                 "",
                 "Начать игру",
                 "Выбрать уровень",
                 "Выбрать корабль",
                 "Правила игры"]

    fon = pygame.transform.scale(load_image('menu.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in menu_text:
        string_rendered = font.render(line, 1, pygame.Color('purple'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] in range(0, 200) and event.pos[1] in range(180, 220):
                        start_game()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(230, 260):
                        level_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(270, 305):
                        ship_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(310, 360):
                        rules()
            pygame.display.flip()


tile_images = {'wall1': load_image('wall1.jpg'), 'wall2': load_image('wall2.jpg'), 'wall3': load_image('wall3.jpg'),
               "mob1": load_image("mob1.png"), "mob2": load_image("mob2.png"), "space": load_image("space.png")}
player_image = load_image(ship_name, (255, 255, 255))
tile_width = tile_height = 50


def game_over():
    fon = pygame.transform.scale(load_image('game_over.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_over_menu()
        pygame.display.flip()
        clock.tick(FPS)


def game_over_menu():
    menu_text = ["Игра окончена",
                 "",
                 "Начать игру сначала",
                 "Выбрать уровень",
                 "Выбрать корабль",
                 "В главное меню"]

    fon = pygame.transform.scale(load_image('menu.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100

    for line in menu_text:
        string_rendered = font.render(line, 1, pygame.Color('purple'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        mouse1 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if event.button == 1:
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(180, 220):
                        restart_game()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(230, 260):
                        level_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(270, 305):
                        ship_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(310, 360):
                        menu()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, hp):
        if tile_type == "mob1" or tile_type == "mob 2":
            super().__init__(enemy_group, tiles_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.hp = hp

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.hp = 5

    def damage(self):
        self.hp -= 1
        if self.hp == 1:
            game_over()


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('mob1', x, y, 3)
            elif level[y][x] == '@':
                Tile('mob2', x, y, 1)
            elif level[y][x] == ',':
                Tile('wall1', x, y, 1)
            elif level[y][x] == '/':
                Tile('wall2', x, y, 2)
            elif level[y][x] == '-':
                Tile('wall3', x, y, 3)
            elif level[y][x] == "%":
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def restart_game(lvl_name=lvl_name):
    global player, level_x, level_y
    all_sprites.remove(*all_sprites.sprites())
    tiles_group.remove(*tiles_group.sprites())
    player_group.remove(*player_group.sprites())
    bullet_group.remove(*bullet_group.sprites())
    player, level_x, level_y = generate_level(load_level(lvl_name))
    start_game()


player, level_x, level_y = generate_level(load_level(lvl_name))

start_screen()
menu()
terminate()
