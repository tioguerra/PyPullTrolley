#!/usr/bin/env python3
# -*- coding: utf-8 -*-import pygame

# Importa a biblioteca gráfica/interativa
import pygame
import numpy as np

# Constantes cosméticas
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_CAPTION = 'PyPullTrolley'
BACKGROUND_COLOR = 128, 128, 128
CAR_COLOR = 255, 255, 255

class Car:
  '''
  Simula um carro usando modelo cinemático
  de uma bicicleta
  '''
  def __init__(self, init_pos=(0.0,0.0,0.0)):
    self.x, self.y, self.angle = init_pos
    self.vel = 0.0
    self.steer = 0.0
    self.length = 50
  def update(self):
    L = self.length
    lr = self.length / 2.0
    tansteer = np.tan(self.steer)
    beta = np.arctan2(lr * tansteer, L)
    angvel = self.vel * tansteer * np.cos(beta) / L
    dx = self.vel * np.sin(self.angle + beta + np.pi)
    dy = self.vel * np.cos(self.angle + beta + np.pi)
    self.x += dx
    self.y += dy
    self.angle += angvel

class Simulation:
  def __init__(self, screen_width=SCREEN_WIDTH, \
               screen_height=SCREEN_HEIGHT, \
               window_caption=WINDOW_CAPTION):
    '''
    Inicializa o ambiente do PyGame
    '''
    pygame.init()

    # Largura e altura da janela, em pixels
    self.screen_width = screen_width
    self.screen_height = screen_height

    # Define o título da janela
    pygame.display.set_caption(window_caption)

    # Cria a janela da simulação
    self.screen = pygame.display.set_mode(\
                                    [self.screen_width, \
                                     self.screen_height])

    # Cor de fundo
    self.screen.fill(BACKGROUND_COLOR)

    # Cria o timer para controlar o framerate
    self.clock = pygame.time.Clock()

    # A simulação vai encerrar o laço principal
    # quando essa flag for verdadeira.
    self.exit = False

    # Lista de objetos a serem simulados
    self.objs = list()

    # Cria os objetos
    self.create_objects()

  def create_objects(self):
    '''
    Creates the simulated objects
    '''
    self.car = Car((400,300,0.0))
    self.objs.append(self.car)

  def handle_events(self):
    '''
    Detecta e trata os eventos interativos
    do PyGame.
    '''

    # Examina os eventos acumulados na fila
    # de eventos, um a um
    for event in pygame.event.get():
        
      # Evento de encerrar a aplicação, por exemplo
      # fechando a janela.
      if event.type == pygame.QUIT:
        self.exit = True

      # Eventos de pressionamento de teclas
      elif event.type == pygame.KEYUP:

        # Tecla ESC encerra a aplicação
        if event.key == pygame.K_ESCAPE:
          self.exit = True
        # Controles para dirigir o carro
        elif event.key == pygame.K_UP:
          self.car.vel += 1.0
        elif event.key == pygame.K_DOWN:
          self.car.vel -= 1.0
        elif event.key == pygame.K_RIGHT:
          self.car.steer -= 0.5
        elif event.key == pygame.K_LEFT:
          self.car.steer += 0.5
        elif event.key == pygame.K_SPACE:
          self.car.vel = 0.0
          self.car.steer = 0.0

  def draw_car(self, car):
    '''
    Desenha um objeto da classe Car
    '''
    self.draw_rect(30, car.length, CAR_COLOR, \
                   car.x, car.y, car.angle)

  def draw_rect(self, w, h, color, x, y, angle):
    '''
    Desenha um retângulo de largura w, altura h,
    posicionado com centro em x, y e angulo angle.
    '''
    corners = [ (w/2,-h/2), (w/2,h/2), \
                (-w/2,h/2), (-w/2,-h/2) ]
    points = list()
    for corner in corners:
      px, py = corner
      alpha = np.arctan2(px, py) + angle
      d = np.sqrt(px**2+py**2)
      px = x + d*np.sin(alpha)
      py = y + d*np.cos(alpha)
      points.append((px, py))
    pygame.draw.aalines(self.screen, color, True, points)

  def run(self):
    '''
    Laço principal do programa
    '''
    while not self.exit:
      self.screen.fill(BACKGROUND_COLOR)
      for obj in self.objs:
        obj.update()
      self.draw_car(self.car)
      pygame.display.update()
      self.handle_events()
      self.clock.tick(30)

if __name__ == '__main__':
  sim = Simulation()
  sim.run()
