"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame

import MusicCode

from SpriteSheet import SpriteSheet

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super(Enemy, self).__init__()

        width = 60
        height = 90

        self.image = pygame.Surface([width, height])
        self.image.fill(YELLOW)

        self.EnemySpriteSheet = SpriteSheet("../Sprites/RushNAttackEnemies.png")

        self.EnemySpriteRunning = [self.EnemySpriteSheet.get_image(5, 8, 22, 35), self.EnemySpriteSheet.get_image(27, 8, 22, 35), self.EnemySpriteSheet.get_image(52, 8, 22, 35), self.EnemySpriteSheet.get_image(77, 8, 22, 35)]

        self.x = 0

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.level = None

        self.change_x = -1
        self.change_y = 0

        self.counter = 0

    def update(self):

        self.updateAnims()
        self.calculate_gravity()


        self.change_x = -3

        self.rect.x += self.change_x
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for item in hit_list:
            if self.change_x > 0:
                self.rect.right = item.rect.left
            elif self.change_x < 0:
                self.rect.left = item.rect.right

        self.rect.y += self.change_y
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for item in hit_list:
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom

            self.change_y = 0


    def calculate_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        # On the ground?
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def updateAnims(self):
        self.counter += 1
        if (self.counter % 7) == 0:
            if self.x < len(self.EnemySpriteRunning):
                self.image = self.EnemySpriteRunning[self.x]
                self.image = pygame.transform.scale(self.image, (60, 90))
                self.image = pygame.transform.flip(self.image, True, False)
                self.x = self.x + 1
            else:
                self.x = 0



class Player(pygame.sprite.Sprite):
    def __init__(self):

        self.PlayerSpriteSheet = SpriteSheet("../Sprites/RushNAttackPlayer.png")

        self.SpriteRunning = [self.PlayerSpriteSheet.get_image(16, 111, 20, 35), self.PlayerSpriteSheet.get_image(39, 111, 20, 35), self.PlayerSpriteSheet.get_image(63, 111, 20, 35), self.PlayerSpriteSheet.get_image(85, 111, 20, 35)]

        self.SpriteDeath = [self.PlayerSpriteSheet.get_image(364, 111, 20, 35), self.PlayerSpriteSheet.get_image(390, 111, 35, 35)]

        self.SpriteClimb = [self.PlayerSpriteSheet.get_image(126, 111, 20, 35), self.PlayerSpriteSheet.get_image(151, 111, 20, 35)]

        self.jumping = True

        self.isClimbing = False

        self.running_frames = []

        self.DeathPlayed = False

        self.knifing = False

        super(Player, self).__init__()

        width = 60
        height = 90

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(self.image, (60, 90))

        self.image = self.PlayerSpriteSheet.get_image(16, 111, 20, 35)
        self.image = pygame.transform.scale(self.image, (60, 90))

        self.change_x = 0
        self.change_y = 0

        self.level = None

        self.counter = 0


        self.x = 0


        self.action = "Idle"

    def update(self):
        self.calculate_gravity()

        self.updateAnims()
        self.rect.x += self.change_x
        if self.DeathPlayed == False:
            if self.change_x > 0:
                self.action = "RunningRight"
            elif self.change_x < 0:
                self.action = "RunningLeft"
        else:
            self.action = "Dead"
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for item in hit_list:
            if self.change_x > 0:
                self.rect.right = item.rect.left
            elif self.change_x < 0:
                self.rect.left = item.rect.right

        self.rect.y += self.change_y
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for item in hit_list:
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
                self.jumping = False
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom

            self.change_y = 0

        ladderhit_list = pygame.sprite.spritecollide(self, self.level.ladder_list, False)

        if len(ladderhit_list) == 0:
            self.isClimbing = False
        else:
            self.isClimbing = True

        enemyhit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)


        for item in enemyhit_list:
            if self.knifing == False:
                if self.DeathPlayed == False:
                    self.DeathPlayed = True
                    self.x = 0
                    deathsound = pygame.mixer.Sound("../Sounds/DeathSound.wav")
                    deathsound.play()
                    pygame.mixer.music.stop()
                    self.change_x = 0
                    self.change_y = 0
            else:
                item.kill()
                self.knifing = False


    def go_right(self):
        if self.DeathPlayed == False:
            self.change_x = 6



    def go_left(self):
        if self.DeathPlayed == False:
            self.change_x = -6

    def stop(self):
        self.change_x = 0

    def attack(self):
        if self.DeathPlayed == False:
            self.counter = 0
            self.knifing = True
            knifestab = pygame.mixer.Sound("../Sounds/KnifeSlice3Louder.wav")
            knifestab.play()


    def jump(self):
        if self.isClimbing == False:
            if self.DeathPlayed == False:
                if self.jumping == False:
                    self.jumping = True
                    self.change_y = -10
        else:
            if self.DeathPlayed == False:
                self.change_y = -6
                self.jumping = True

    def updateAnims(self):
        self.counter += 1
        if (self.counter % 7) == 0:
            if self.action == "RunningRight":
                if self.x < len(self.SpriteRunning):
                    self.image = self.SpriteRunning[self.x]
                    self.image = pygame.transform.scale(self.image, (60, 90))
                    self.x = self.x + 1
                else:
                    self.x = 0
            elif self.action == "RunningLeft":
                if self.x < len(self.SpriteRunning):
                    self.image = self.SpriteRunning[self.x]
                    self.image = pygame.transform.scale(self.image, (60, 90))
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.x = self.x + 1
                else:
                    self.x = 0

        if (self.counter % 22) == 0:
            if self.action == "Dead":
                if self.x < len(self.SpriteDeath):
                    self.image = self.SpriteDeath[self.x]
                    if self.x == 0:
                        self.image = pygame.transform.scale(self.image, (60, 90))
                    else:
                        self.image = pygame.transform.scale(self.image, (90, 90))
                    self.x = self.x + 1

        if self.knifing == True:
            self.image = self.PlayerSpriteSheet.get_image(190, 111, 35, 35)
            self.image = pygame.transform.scale(self.image, (90, 90))
            self.x = self.x + 1
            if (self.counter % 21) == 0:
                self.knifing = False
                self.image = self.PlayerSpriteSheet.get_image(16, 111, 20, 35)
                self.image = pygame.transform.scale(self.image, (60, 90))

        if (self.counter % 7) == 0:
            if self.isClimbing == True:
                if self.DeathPlayed == False:
                    if self.x < len(self.SpriteDeath):
                        self.image = self.SpriteClimb[self.x]
                        self.image = pygame.transform.scale(self.image, (60, 90))
                        self.x = self.x + 1
                    else:
                        self.x = 0

        self.action = "Idle"

    def calculate_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        # On the ground?
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height


class Ladder(pygame.sprite.Sprite):
    def __init__(self, width, height):

        super(Ladder, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):

        super(Platform, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Level(object):

    global ScrollAdd
    ScrollAdd = 0

    timer = 0

    def __init__(self):
        super(Level, self).__init__()

        self.platform_list = pygame.sprite.Group()

        self.ladder_list = pygame.sprite.Group()

        self.enemy_list = pygame.sprite.Group()

        self.world_shift = 0

        self.timer = 0


    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

        self.current = pygame.time.get_ticks()

        if self.current - self.timer > 1499:
            add_enemy = Enemy(1250, 50)
            add_enemy.level = self
            self.enemy_list.add(add_enemy)
            self.timer = self.current



    def draw(self, screen):
        screen.fill(BLUE)

        screen.blit(self.background, ((-2400 + ScrollAdd),-145))

        #self.platform_list.draw(screen)

        #self.ladder_list.draw(screen)

        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x

        global ScrollAdd

        ScrollAdd += shift_x

        for item in self.platform_list:
            item.rect.x += shift_x

        for item in self.ladder_list:
            item.rect.x += shift_x

        for item in self.enemy_list:
            item.rect.x += shift_x

class Level_01(Level):
    def __init__(self):

        Level.__init__(self)

        self.level_limit = -500


        levels = [[9000, 70, -50, 730],
                  [540, 20, 330, 490],
                  [150, 20, 630, 290],
                  [310, 20, 960, 490],
                  [150, 20, 1040, 290],
                  [320, 20, 1350, 490],
                  [150, 20, 1420, 290],
                  [310, 20, 1760, 490],
                  [150, 20, 1830, 290],
                  [320, 20, 2160, 490],
                  [150, 20, 2220, 290],
                  [300, 20, 2160, 490],
                  [350, 20, 2570, 490],
                  [150, 20, 2620, 290],
                  [70, 20, 4060, 520],
                  [230, 20, 4230, 520],
                  [70, 20, 4680, 520],
                  [230, 20, 4830, 520],
                  [70, 20, 5280, 520],
                  [230, 20, 5430, 520],
                  [70, 20, 5870, 520],
                  [230, 20, 6030, 520],
                 ]

        ladders = [
                    [70, 250, 252, 480],
                    [70, 250, 880, 480],
                    [70, 170, 565, 300],
                    [40, 170, 990, 300],
                    [70, 250, 1280, 480],
                    [40, 170, 1370, 300],
                    [70, 250, 1680, 480],
                    [40, 170, 1780, 300],
                    [70, 250, 2080, 480],
                    [40, 170, 2170, 300],
                    [70, 250, 2490, 480],
                    [40, 170, 2560, 300],
                    [70, 250, 2930, 480],
                    [70, 200, 4150, 510],
                    [70, 200, 4750, 510],
                    [70, 200, 5350, 510],
                    [70, 200, 5950, 510],
                  ]

        self.background = pygame.image.load("../Sprites/Level1.png")
        self.background = pygame.transform.scale(self.background, (12000, 1000))


        for level in levels:
            platform = Platform(level[0], level[1])
            platform.rect.x = level[2]
            platform.rect.y = level[3]
            self.platform_list.add(platform)

        for level in ladders:
            platform = Ladder(level[0], level[1])
            platform.rect.x = level[2]
            platform.rect.y = level[3]
            self.ladder_list.add(platform)




def main():
    pygame.init()
    pygame.mixer.init()

    # Set the width and height of the screen [width, height]
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Rush N' Attack")


    level = Level_01()

    player = Player()
    player.rect.x = 100
    player.rect.y = 100
    player.level = level

    MusicCode.MusicPlayer()

    sprites_list = pygame.sprite.Group()
    sprites_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    CanGoLeft = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_SPACE:
                    player.attack()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.stop()

        if player.rect.right >= 500:
            diff = player.rect.right - 500
            level.shift_world(-diff)
            player.rect.right = 500

        if player.rect.left <= 120:
            if CanGoLeft == True:
                diff = 120 - player.rect.left
                level.shift_world(diff)
                player.rect.left = 120

        if player.rect.left < 1:
            player.rect.right = 70


        # --- Game logic should go here
        sprites_list.update()
        level.update()

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        #screen.fill(WHITE)

        # --- Drawing code should go here
        level.draw(screen)
        sprites_list.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

if __name__ == "__main__":
    main()