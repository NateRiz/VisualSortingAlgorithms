import pygame
import sys
from random import shuffle
from math import sqrt, ceil
from time import sleep
from threading import Thread, Timer
from queue import Queue

pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
unsorted = [i for i in range(300)]
shuffle(unsorted)
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 5 / 1000  # Milli
q = Queue()


def main():
    for i in range(n):
        pygame.draw.rect(screen, WHITE,
                         (i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()

    current = 0
    SleepSort(unsorted)
    while not QUIT_SIGNAL:
        if not q.empty():
            get = q.get()
            if get == current:
                UpdateDisplay(current, get, (0, 255, 0))
            else:
                UpdateDisplay(current, get, (255, 0, 0))
            current += 1


def SleepSort(unsorted):
    for i, j in enumerate(unsorted):
        Timer(j / 25, q.put, [j]).start()


def CheckInput():
    global QUIT_SIGNAL
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT_SIGNAL = True
                return
        sleep(1)


def UpdateDisplay(i, j, color=(255, 255, 255)):
    pygame.draw.rect(screen, BLACK, (i * (width / n), 0, (width / n) - offset, height))
    pygame.draw.rect(screen, color, (i * (width / n), height - (j * (height / n)), (width / n) - offset, height))
    pygame.display.update()


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
