import pgzrun
import random

WIDTH = 800
HEIGHT = 400

game_over = False
score = 0
show_instructions = True
show_menu = True
sound_on = True


class Player:
    def __init__(self):
        self.images = ["run1", "run2", "run3"]
        self.image_index = 0
        self.actor = Actor(self.images[self.image_index], (100, 300))
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.on_ground = True
        self.speed = 3
        self.idle_images = ["idle1", "idle2"]
        self.idle_index = 0

    def update(self):
        if game_over or show_instructions or show_menu:
            self.idle_index = (self.idle_index + 0.05) % len(self.idle_images)
            self.actor.image = self.idle_images[int(self.idle_index)]
            return

        self.vel_y += self.gravity
        self.actor.y += self.vel_y

        if self.actor.y >= 300:
            self.actor.y = 300
            self.vel_y = 0
            self.on_ground = True

        self.actor.x += self.vel_x
        self.actor.x = max(0, min(self.actor.x, WIDTH))

        self.image_index = (self.image_index + 0.1) % len(self.images)
        self.actor.image = self.images[int(self.image_index)]

    def jump(self):
        if self.on_ground:
            self.vel_y = -26
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

    def move_left(self):
        self.vel_x = -self.speed

    def move_right(self):
        self.vel_x = self.speed

    def stop(self):
        self.vel_x = 0

    def draw(self):
        self.actor.draw()


class Enemy:
    def __init__(self, x, y, image):
        self.images = [image]
        self.image_index = 0
        self.actor = Actor(self.images[self.image_index], (x, y))
        self.speed = random.choice([-3, 3])
        self.direction = random.choice([-1, 1])

    def update(self):
        if game_over or show_instructions or show_menu:
            return

        self.actor.x += self.speed * self.direction
        if self.actor.x < 50 or self.actor.x > WIDTH - 50:
            self.direction *= -1

    def draw(self):
        self.actor.draw()


enemies = [Enemy(random.randint(400, WIDTH), 300, "enemy1"), Enemy(random.randint(400, WIDTH), 300, "enemy2")]
player = Player()


class NPC:
    def __init__(self, x, y):
        self.actor = Actor("npc", (x, y))
        self.speed = 2
        self.direction = 1

    def update(self):
        if game_over or show_instructions or show_menu:
            return

        self.actor.x += self.speed * self.direction
        if self.actor.x < 200 or self.actor.x > WIDTH - 200:
            self.direction *= -1

    def draw(self):
        self.actor.draw()


npc = NPC(600, 300)


def update():
    global game_over, score
    if show_instructions or show_menu:
        return

    player.update()
    npc.update()
    for enemy in enemies:
        enemy.update()

        if player.actor.colliderect(enemy.actor):
            game_over = True
            if sound_on:
                sounds.hit.play()

    if not game_over:
        score += 1


def draw():
    screen.clear()
    screen.fill((173, 216, 230))

    if show_menu:
        screen.draw.text("RUNNER GAME", (250, 50), fontsize=40, color="black")
        screen.draw.text("1. Oyuna Başla (BAS 'S')", (250, 150), fontsize=30, color="black")
        screen.draw.text("2. Ses Aç/Kapat (BAS 'M')", (250, 200), fontsize=30, color="black")
        screen.draw.text("3. Çıkış (BAS 'Q')", (250, 250), fontsize=30, color="black")
    elif show_instructions:
        screen.draw.text("Oyunu başlatmak için SPACE tuşuna bas!", (200, 300), fontsize=30, color="black")
        screen.draw.text("Zıplarken ileri gitmek için sağa veya sola basılı tutun!", (150, 340), fontsize=25,
                         color="black")
        screen.draw.text("Not: Kadın karakterler düşman değildir!", (150, 380), fontsize=25, color="black")
        screen.draw.text("Not 2: Feminist değilim! :)", (150, 410), fontsize=25, color="black")
    elif game_over:
        screen.draw.text("Oyun Bitti! Skor: " + str(score), (300, 180), fontsize=30, color="black")
        screen.draw.text("Tekrar başlatmak için SPACE tuşuna bas", (200, 220), fontsize=20, color="black")
    else:
        player.draw()
        for enemy in enemies:
            enemy.draw()
        npc.draw()
        screen.draw.text("Skor: " + str(score), (10, 10), fontsize=20, color="black")


def on_key_down(key):
    global show_instructions, game_over, score, show_menu, sound_on
    if show_menu:
        if key == keys.S:
            show_menu = False
        elif key == keys.M:
            sound_on = not sound_on
        elif key == keys.Q:
            exit()
        return

    if show_instructions:
        show_instructions = False
        return

    if game_over and key == keys.SPACE:
        game_over = False
        score = 0
        player.actor.x, player.actor.y = 100, 300
        for enemy in enemies:
            enemy.actor.x = random.randint(400, WIDTH)
        return

    if key == keys.SPACE:
        player.jump()
    if key == keys.LEFT:
        player.move_left()
    if key == keys.RIGHT:
        player.move_right()


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        player.stop()


pgzrun.go()
