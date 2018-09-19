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
unsorted = [i for i in range(1, 3000)]
shuffle(unsorted)
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 50 / 1000  # Milli


def main():
    for i in range(n):
        pygame.draw.rect(screen, WHITE,(i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))

    pygame.display.update()
    while not QUIT_SIGNAL:
        if sorted(unsorted) != unsorted:
            RadixSort(unsorted)


def RadixSort(unsorted):
    digits = len(str(max(unsorted)))
    buckets = [[] for _ in range(10)]

    for j in range(digits):
        for i in unsorted:
            buckets[int(str(i).rjust(digits, "0")[digits-j-1])].append(i)

        unsorted.clear()
        for i in buckets:
            unsorted += i

        [i.clear() for i in buckets]

        for i in range(n):
            UpdateDisplay(i)
            if QUIT_SIGNAL:
                return
        sleep(delay)


    print(unsorted)

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
    pygame.draw.rect(screen, color,(i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
