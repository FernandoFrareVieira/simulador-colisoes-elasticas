import pygame
import sys

def drawText(text, font, color, surface, x, y):
    textObj = font.render(text, True, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

def menu():
    
    width, height = 1600, 900
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Collision Simulator")
    font = pygame.font.Font(None, 36)
    
    inputActive1 = False
    inputActive2 = False
    inputText1 = ''
    inputText2 = ''
    colorInactive = pygame.Color('lightskyblue3')
    colorActive = pygame.Color((228, 67, 63))
    color1 = colorInactive
    color2 = colorInactive
    inputBox1 = pygame.Rect(0, 0, 140, 32)
    inputBox2 = pygame.Rect(0, 0, 140, 32)
    button = pygame.Rect(0, 0, 100, 50)
    
    while True:
        window.fill((30, 30, 30))
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputBox1.collidepoint(mx, my):
                    inputActive1 = not inputActive1
                else:
                    inputActive1 = False
                if inputBox2.collidepoint(mx, my):
                    inputActive2 = not inputActive2
                else:
                    inputActive2 = False
                if button.collidepoint(mx, my):
                    try:
                        num_balls = int(inputText1)
                        speed = int(inputText2)
                        return num_balls, speed
                    except ValueError:
                        pass
                color1 = colorActive if inputActive1 else colorInactive
                color2 = colorActive if inputActive2 else colorInactive
            if event.type == pygame.KEYDOWN:
                if inputActive1:
                    if event.key == pygame.K_BACKSPACE:
                        inputText1 = inputText1[:-1]
                    else:
                        inputText1 += event.unicode
                if inputActive2:
                    if event.key == pygame.K_BACKSPACE:
                        inputText2 = inputText2[:-1]
                    else:
                        inputText2 += event.unicode
        
        inputBox1.center = (window.get_width() // 2, window.get_height() // 2 - 50)
        inputBox2.center = (window.get_width() // 2, window.get_height() // 2 + 50)
        button.center = (window.get_width() // 2, window.get_height() // 2 + 150)
        
        pygame.draw.rect(window, color1, inputBox1, 2)
        pygame.draw.rect(window, color2, inputBox2, 2)
        pygame.draw.rect(window, (228,67,63), button)
        
        drawText('Número de Bolas:', font, (255, 255, 255), window, window.get_width() // 2 - 110, window.get_height() // 2 - 100)
        drawText('Velocidade das Bolas:', font, (255, 255, 255), window, window.get_width() // 2 - 135, window.get_height() // 2)
        drawText('Iniciar', font, (255, 255, 255), window, button.centerx - 35, button.y + 15)
        
        txtSurface1 = font.render(inputText1, True, color1)
        txtSurface2 = font.render(inputText2, True, color2)
        window.blit(txtSurface1, (inputBox1.x + 5, inputBox1.y + 5))
        window.blit(txtSurface2, (inputBox2.x + 5, inputBox2.y + 5))
        inputBox1.w = max(140, txtSurface1.get_width() + 10)
        inputBox2.w = max(140, txtSurface2.get_width() + 10)
        
        pygame.display.flip()