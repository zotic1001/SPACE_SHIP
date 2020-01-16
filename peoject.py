import os
import pygame
import sys
import random

levels = 5
FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 800, 600
STEP = 10
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
player = None
lvl_name = "lvl1.txt"
ship_name = "ship1.png"

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
anim_sprites = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
point = 0


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


def start_game():
    pygame.mouse.set_visible(False)
    global lvl_name, point
    text = "Счёт:" + str(point) + "                                                           " \
                                  "                                 Жизни: " + str(player_group.sprites()[0].hp)
    fon = pygame.transform.scale(load_image(lvl_name[0:-4] + ".jpg"), (WIDTH, HEIGHT))
    running = True
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color('purple'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 0
    intro_rect.x = 10
    while running:
        text = "Счёт:" + str(point) + "                                                           " \
                                      "                                 Жизни: " + str(player_group.sprites()[0].hp)
        string_rendered = font.render(text, 1, pygame.Color('purple'))
        intro_rect = string_rendered.get_rect()
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
                if event.key == pygame.K_1:
                    win_menu()
            elif event.type == pygame.USEREVENT:
                shooting_mob()
                anim_sprites.remove(*anim_sprites.sprites())
        if len(enemy_group) == 0:
            win_menu()
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, intro_rect)
        all_sprites.update()
        anim_sprites.update()
        all_sprites.draw(screen)
        anim_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(anim_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def dead_anim(x, y):
    dead = AnimatedSprite(load_image("dead.png", -1), 3, 4, x, y)


def level_change():
    global lvl_name
    pygame.mouse.set_visible(True)
    menu_text = ["Уровень 1",
                 'Уровень 2',
                 "Уровень 3",
                 "Уровень 4",
                 "Уровень 5",
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(110, 135):
                        lvl_name = "lvl1.txt"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(145, 170):
                        lvl_name = "lvl2.txt"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(160, 205):
                        lvl_name = "lvl3.txt"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(235, 255):
                        lvl_name = "lvl4.txt"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(265, 290):
                        lvl_name = "lvl5.txt"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(310, 330):
                        menu()
            pygame.display.flip()


def ship_change():
    pygame.mouse.set_visible(True)
    global ship_name, player_image
    intro_text = ["     Выбрать корабль",
                  "",
                  "Корабль 1",
                  "Корабль 2",
                  "Корабль 3",
                  "В главное меню"]

    fon = pygame.transform.scale(load_image('menu.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('purple'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        ship1 = load_image('ship1.png')
        ship1r = ship1.get_rect(bottomright=(400, 200))
        ship2 = load_image('ship2.png')
        ship2r = ship2.get_rect(bottomright=(400, 280))
        ship3 = load_image('ship3.png')
        ship3r = ship3.get_rect(bottomright=(400, 330))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] in range(0, 200) and event.pos[1] in range(180, 220):
                        ship_name = "ship1.png"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(230, 260):
                        ship_name = "ship2.png"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(270, 305):
                        ship_name = "ship3.png"
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(310, 360):
                        menu()
        player_image = load_image(ship_name)
        screen.blit(ship2, ship2r)
        screen.blit(ship1, ship1r)
        screen.blit(ship3, ship3r)
        pygame.display.flip()
        clock.tick(FPS)


def rules():
    pygame.mouse.set_visible(True)
    intro_text = ["Правила",
                  "1.Ваша цель убить всех врагов на уровне",
                  "2.Перемещаться с помощью стрелок",
                  "3. SPACE - выстрел",
                  "4. Если враги попадут по вам 3 раза ,то вы проиграете",
                  "В главное меню"]

    fon = pygame.transform.scale(load_image('menu.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
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
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(280, 350):
                        menu()
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def shooting_mob():
    if len(enemy_group) > 20:
        shoot_mob = random.choice(enemy_group.sprites())
        bullet = Bullet(shoot_mob.rect.x, shoot_mob.rect.y, 1)
        bullet.shoot()

        shoot_mob1 = random.choice(enemy_group.sprites())
        bullet1 = Bullet(shoot_mob1.rect.x, shoot_mob1.rect.y, 1)
        bullet1.shoot()

        shoot_mob2 = random.choice(enemy_group.sprites())
        bullet2 = Bullet(shoot_mob2.rect.x, shoot_mob2.rect.y, 1)
        bullet2.shoot()

        shoot_mob3 = random.choice(enemy_group.sprites())
        bullet3 = Bullet(shoot_mob3.rect.x, shoot_mob3.rect.y, 1)
        bullet3.shoot()
    elif len(enemy_group) > 10:
        shoot_mob = random.choice(enemy_group.sprites())
        bullet = Bullet(shoot_mob.rect.x, shoot_mob.rect.y, 1)
        bullet.shoot()

        shoot_mob1 = random.choice(enemy_group.sprites())
        bullet1 = Bullet(shoot_mob1.rect.x, shoot_mob1.rect.y, 1)
        bullet1.shoot()

        shoot_mob2 = random.choice(enemy_group.sprites())
        bullet2 = Bullet(shoot_mob2.rect.x, shoot_mob2.rect.y, 1)
        bullet2.shoot()

    elif len(enemy_group) > 5:
        shoot_mob = random.choice(enemy_group.sprites())
        bullet = Bullet(shoot_mob.rect.x, shoot_mob.rect.y, 1)
        bullet.shoot()

        shoot_mob1 = random.choice(enemy_group.sprites())
        bullet1 = Bullet(shoot_mob1.rect.x, shoot_mob1.rect.y, 1)
        bullet1.shoot()

    elif len(enemy_group) == 0:
        return
    elif len(enemy_group) > 0:
        shoot_mob = random.choice(enemy_group.sprites())
        bullet = Bullet(shoot_mob.rect.x, shoot_mob.rect.y, 1)
        bullet.shoot()


def start_screen():
    pygame.mouse.set_visible(False)
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
        self.image.fill(pygame.color.Color("red"))
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
        if self.vel == -1:
            if len(bullet_group) < 2:
                bullet = Bullet(self.rect.x, self.rect.y, self.vel)
                all_sprites.add(bullet)
                bullet_group.add(bullet)
        else:
            bullet = Bullet(self.rect.x, self.rect.y, self.vel)
            all_sprites.add(bullet)
            enemybullet_group.add(bullet)


def menu():
    pygame.mouse.set_visible(True)
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
                        restart_game()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(230, 260):
                        level_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(270, 305):
                        ship_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(310, 360):
                        rules()
            pygame.display.flip()


tile_images = {'wall1': load_image('wall1.jpg'), 'wall2': load_image('wall2.jpg'), 'wall3': load_image('wall3.jpg'),
               "mob1": load_image("mob1.png"), "mob2": load_image("mob2.png"), "space": load_image("space.png")}
player_image = load_image(ship_name)
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
    pygame.mouse.set_visible(True)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
            self.enemy = True
        else:
            super().__init__(tiles_group, all_sprites)
            self.enemy = False
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.hp = hp

    def damage(self):
        global point
        self.hp -= 1
        if self.hp == 0:
            if self.tile_type == "mob1" or self.tile_type == "mob2":
                point += 50
                dead_anim(self.rect.x, self.rect.y)
                self.kill()
            else:
                dead_anim(self.rect.x, self.rect.y)
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


def win_menu():
    pygame.mouse.set_visible(True)
    menu_text = ["Уровень пройден",
                 "",
                 "Следующий уровень",
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(180, 220):
                        win()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(230, 260):
                        level_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(270, 305):
                        ship_change()
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(310, 360):
                        menu()
        pygame.display.flip()
        clock.tick(FPS)


def win_all():
    pygame.mouse.set_visible(True)
    menu_text = ["",
                 "",
                 "В главное меню",
                 "",
                 "",
                 ""]

    fon = pygame.transform.scale(load_image('win.jpg'), (800, 600))
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
                    if event.pos[0] in range(0, 250) and event.pos[1] in range(180, 210):
                        menu()
        pygame.display.flip()
        clock.tick(FPS)


def win():
    global lvl_name, levels
    if int(lvl_name[3]) < levels:
        lvl_name = 'lvl' + str(int(lvl_name[3]) + 1) + '.txt'
        restart_game()
    else:
        win_all()


def restart_game():
    global player, level_x, level_y, lvl_name
    all_sprites.remove(*all_sprites.sprites())
    tiles_group.remove(*tiles_group.sprites())
    player_group.remove(*player_group.sprites())
    bullet_group.remove(*bullet_group.sprites())
    enemy_group.remove(*enemy_group.sprites())
    anim_sprites.remove(*anim_sprites.sprites())
    player, level_x, level_y = generate_level(load_level(lvl_name))
    start_game()


player, level_x, level_y = generate_level(load_level(lvl_name))

start_screen()
menu()
terminate()
