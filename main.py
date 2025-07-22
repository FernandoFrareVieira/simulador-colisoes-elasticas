import pygame
import sys
import math
import random
from menu import menu 

pygame.init()

class Ball:
    def __init__(self, radius, pos, speed, color):
        self.radius = radius
        self.pos = pygame.math.Vector2(pos)
        self.speed = pygame.math.Vector2(speed)
        self.color = color
        self.mass = self.radius ** 2

    def move(self, width, height):
        self.pos += self.speed

        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.speed.x *= -1
        elif self.pos.x + self.radius >= width:
            self.pos.x = width - self.radius
            self.speed.x *= -1
        
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.speed.y *= -1
        elif self.pos.y + self.radius >= height:
            self.pos.y = height - self.radius
            self.speed.y *= -1

def draw_ball(window, ball):
    pygame.draw.circle(window, ball.color, (int(ball.pos.x), int(ball.pos.y)), ball.radius)

def handle_collision(ball1, ball2):
    # Vetor de distância entre os centros das bolas
    distance_vec = ball1.pos - ball2.pos
    dist = distance_vec.length()

    # Verifica se há colisão
    if dist <= ball1.radius + ball2.radius:
        overlap = ball1.radius + ball2.radius - dist
        direction_vec = distance_vec.normalize()
        ball1.pos += direction_vec * overlap / 2
        ball2.pos -= direction_vec * overlap / 2

        v1 = ball1.speed
        v2 = ball2.speed
        x1 = ball1.pos
        x2 = ball2.pos
        m1 = ball1.mass
        m2 = ball2.mass
        
        dot_product = (v1 - v2).dot(x1 - x2)
        factor = (2 / (m1 + m2)) * (dot_product / (x1 - x2).length_squared())
        
        # Atualiza as velocidades com base na formula da colisao elastica
        ball1.speed = v1 - factor * m2 * (x1 - x2)
        ball2.speed = v2 - factor * m1 * (x2 - x1)

        # Troca as cores para um efeito visual
        ball1.color, ball2.color = ball2.color, ball1.color
        
         # Retorna True se houve colisão
        return True
    return False

def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def main():
    width, height = 1600, 900
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Collision Simulator")

    try:
        collision_sound = pygame.mixer.Sound("collisionSound.wav")
        collision_sound.set_volume(0.5)
    except pygame.error:
        print("Aviso: Arquivo 'collisionSound.wav' não encontrado.")
        collision_sound = None

    number_balls, speed_balls = menu()
    balls = []
    
    for _ in range(number_balls):
        radius = 20
        while True:
            pos = (random.randint(radius, width - radius), random.randint(radius, height - radius))

            # Verifica se a nova bola não sobrepõe nenhuma existente
            is_overlapping = False
            for existing_ball in balls:
                if pygame.math.Vector2(pos).distance_to(existing_ball.pos) < radius + existing_ball.radius:
                    is_overlapping = True
                    break
            if not is_overlapping:
                break
        
        #angulo inicial para a velocidade
        angle = random.uniform(0, 2 * math.pi)

        #velocidade inicial
        speed = (math.cos(angle) * speed_balls, math.sin(angle) * speed_balls)
        
        ball = Ball(radius, pos, speed, random_color())
        balls.append(ball)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move todas as bolas
        for ball in balls:
            ball.move(width, height)

        # Checa e lida com as colisões
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if handle_collision(balls[i], balls[j]):
                    if collision_sound:
                        collision_sound.play()
        
        window.fill((30, 30, 30))
        for ball in balls:
            draw_ball(window, ball)

        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()