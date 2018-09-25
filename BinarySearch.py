import pygame
import sys
from random import shuffle, choice, randint
from math import sqrt, ceil
from time import sleep
from threading import Thread

pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
unsorted = [i for i in range(1, 7000)]
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 100 / 1000  # Milli


def main():
    for i in range(n):
        pygame.draw.rect(screen, WHITE,
                         (i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()

    BinarySearch(unsorted, 0, len(unsorted)-1, choice(unsorted))
    while not QUIT_SIGNAL:
        sleep(delay)


def BinarySearch(arr, l, r, x):
    if QUIT_SIGNAL:
        return
    sleep(delay)
    color = GetRandomColor()
    [UpdateDisplay(i, arr[i], color) for i in range(l, r)]
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return BinarySearch(arr, l, mid - 1, x)
        else:
            return BinarySearch(arr, mid + 1, r, x)
    else:
        return -1


def CheckInput():
    global QUIT_SIGNAL
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT_SIGNAL = True
                return
        sleep(1)


def UpdateDisplay(i, j,  color=(255, 255, 255)):
    pygame.draw.rect(screen, BLACK, (i * (width / n), 0, (width / n) - offset, height))
    pygame.draw.rect(screen, color,
                     (i * (width / n), height - (j * (height / n)), (width / n) - offset, height))
    pygame.display.update()

def GetRandomColor():
    return (randint(200,255), randint(200,255), randint(200,255))


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
