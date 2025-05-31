import pygame
import json


pygame.init()

size = 800
width = size
height = size

tile_size = 40

game_over = 0
clock = pygame.time.Clock()
fps = 60

image2 = pygame.image.load('images/bg7.png')
rect2 = image2.get_rect()

level = 1
max_level = 4
score = 0

sound_jump = pygame.mixer.Sound('music/jump.wav')
sound_game_over = pygame.mixer.Sound('music/game_over.wav')
sound_coin = pygame.mixer.Sound('music/coin.wav')


def reset_level():
    global score
    score = 0
    player.rect.x = 100
    player.rect.y = height - 130
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    with open(f'levels/level{level}.json', 'r') as file:
        world_data = json.load(file)
    world = World(world_data)
    return world


display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mario')
with open('levels/level1.json', 'r') as file:
    world_data = json.load(file)


def draw_text(text, icon, color=(250, 250, 250), icon_position='left', size=30, x=40, y=10):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))
    image = pygame.image.load(icon)
    image = pygame.transform.scale(image, (20, 30))
    rect = image.get_rect()
    if icon_position == 'left':
        img_x = x - 30
    elif icon_position == 'right':
        img_x = x + 30
    img_y = y
    rect.x = img_x
    rect.y = img_y
    display.blit(image, (img_x, img_y))


class Player:
    def __init__(self):
        self.ghost = pygame.image.load(f'images/ghost.png')
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 1
        for num in range(1, 4):
            img_right = pygame.image.load(f'images/player{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        # self.image = pygame.image.load('images/player1.png')
        # self.image = pygame.transform.scale(self.image, (40, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 130
        self.gravity = 0
        self.jumped = False
        self.is_alive = True
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        global game_over
        walk_speed = 10
        x = 0
        y = 0
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and self.jumped == False:
                self.gravity = -15
                self.jumped = True
                sound_jump.play()
            if key[pygame.K_a]:
                x -= 4
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                x += 4
                self.direction = 1
                self.counter += 1
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]
            # self.rect.x += self.direction
            # if self.rect.right > width or self.rect.left < 0:
            #     self.direction *= -1

            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity
            if self.rect.bottom > height:
                self.rect.bottom = height
                self.gravity = 0
            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > width:
                self.rect.right = width

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y, self.width, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False
            self.rect.x += x
            self.rect.y += y

            if pygame.sprite.spritecollide(self, lava_group, False):
                self.is_alive = False
                if not self.is_alive:
                    sound_game_over.play()
                    self.is_alive = True
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

        elif game_over == -1:
            print('game over')

            self.image = self.ghost
            self.rect.y -= 3

        display.blit(self.image, self.rect)


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('images/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


lava_group = pygame.sprite.Group()


class World:
    def __init__(self, data):
        img_grass = pygame.image.load('images/grass.png')
        img_dirt = pygame.image.load('images/dirt.png')
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {1: img_dirt, 2: img_grass}
                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size))
                    exit_group.add(exit)
                elif tile == 6:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])


class Button:
    def __init__(self, x, y, image, width=120, height=42):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        display.blit(self.image, self.rect)
        return action


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/door.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


exit_group = pygame.sprite.Group()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/coin.png')
        self.image = pygame.transform.scale(self.image, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        self.rect.center = (x, y)


coin_group = pygame.sprite.Group()

restart_btn = Button(width // 2 - 70, height // 2, 'images/restart.png')
start_btn = Button(width // 2, height // 2 - 25, 'images/start.png')
exit_btn_main_menu = Button(width // 2, height // 2 + 25, 'images/exit.png')
exit_btn_game = Button(width // 2 + 70, height // 2, 'images/exit.png')

player = Player()
# world = World(world_data)
run = True
main_menu = True
lives = 0
while run:
    clock.tick(fps)
    # display.fill('#7acafc')
    display.blit(image2, rect2)
    if main_menu:
        if start_btn.draw():
            main_menu = False
            level = 1
            world = reset_level()
            lives = 3
            game_over = 0
        if exit_btn_main_menu.draw():
            run = False
    else:
        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)
        coin_group.draw(display)
        draw_text(str(score), 'images/coin.png')
        draw_text(str(lives), 'images/lives.png', x=100)
        player.update()
        if pygame.sprite.spritecollide(player, coin_group, True):
            sound_coin.play()
            score += 1
            print(score)
        if game_over == -1:
            if restart_btn.draw():
                player = Player()
                world = reset_level()
                game_over = 0
                lives -= 1
                if lives == 0:
                    main_menu = True
            elif exit_btn_game.draw():
                player = Player()
                world = World(world_data)
                break
        if game_over == 1:
            game_over = 0
            if level < max_level:
                level += 1
                world = reset_level()
            else:
                main_menu = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
