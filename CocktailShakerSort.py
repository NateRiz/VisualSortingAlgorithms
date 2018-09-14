import pygame
import sys
from random import shuffle
from math import sqrt, ceil
from time import sleep
from threading import Thread

pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
unsorted = [i for i in range(1, 180)]
shuffle(unsorted)
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 4 / 1000  # Milli


def main():
    for i in range(n):
        pygame.draw.rect(screen, WHITE,
                         (i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()

    while not QUIT_SIGNAL:
        if sorted(unsorted) != unsorted:
            CocktailShakerSort(unsorted)


def CocktailShakerSort(unsorted):
    swapped = True
    start = 0
    end = len(unsorted)
    decrement=1
    while swapped:
        swapped = False
        for i in range(start, end - 1):
            decrement+=1
            if unsorted[i] > unsorted[i + 1]:
                unsorted[i], unsorted[i + 1] = unsorted[i + 1], unsorted[i]
                decrement=1
                UpdateDisplay(i)
                UpdateDisplay(i + 1)
                swapped = True
                sleep(delay)
                if QUIT_SIGNAL:
                    return
        end -= decrement
        [UpdateDisplay(i, (0, 255, 0)) for i in range(end+decrement-1, end-1, -1)]

        for i in range(end, start, -1):
            decrement+=1
            if unsorted[i - 1] > unsorted[i]:
                decrement=1
                unsorted[i], unsorted[i - 1] = unsorted[i - 1], unsorted[i]
                UpdateDisplay(i)
                UpdateDisplay(i - 1)
                swapped = True
                sleep(delay)
                if QUIT_SIGNAL:
                    return
        [UpdateDisplay(i, (0, 255, 0)) for i in range(start, start+decrement)]
        start += decrement

    [UpdateDisplay(i,(0,255,0)) for i in range(n)]


def CheckInput():
    global QUIT_SIGNAL
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT_SIGNAL = True
                return
        sleep(1)


def UpdateDisplay(i, color=(255, 255, 255)):
    pygame.draw.rect(screen, BLACK, (i * (width / n), 0, (width / n) - offset, height))
    pygame.draw.rect(screen, color,
                     (i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
