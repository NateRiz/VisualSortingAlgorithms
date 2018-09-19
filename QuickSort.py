import pygame
import sys
from random import shuffle, randint
from math import sqrt, ceil
from time import sleep
from threading import Thread

pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
unsorted = [i for i in range(1, 1000)]
shuffle(unsorted)
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 5 / 1000  # Milli


def main():
    global unsorted

    for i in range(n):
        pygame.draw.rect(screen, WHITE,(i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()

    while not QUIT_SIGNAL:
        if sorted(unsorted) != unsorted:
            unsorted = QuickSort(unsorted)
        else:
            [UpdateDisplay(i, j, (0, 255, 0)) for i, j in enumerate(unsorted)]


def QuickSort(S, offset=0):
    sleep(delay)
    n = len(S)
    if n < 2:
        return S

    p = S[0]
    if n >= 3:
        p = sorted([S[0], S[n // 2], S[-1]])[1]

    L = []
    E = []
    G = []

    i = 0
    while i < len(S):
        if QUIT_SIGNAL:
            return
        if S[i] < p:
            L.append(S[i])
        elif S[i] > p:
            G.append(S[i])
        else:
            E.append(S[i])
        i += 1

    c1 = GetRandomColor()
    c2 = GetRandomColor()
    c3 = GetRandomColor()
    [UpdateDisplay(i + offset, j, c1) for i, j in enumerate(L)]
    [UpdateDisplay(i + offset + len(L), j, c2) for i, j in enumerate(E)]
    [UpdateDisplay(i + offset + len(L) + len(E), j, c3) for i, j in enumerate(G)]

    L = QuickSort(L, offset)
    if QUIT_SIGNAL:
        return []
    G = QuickSort(G, offset + len(L) + len(E))
    if QUIT_SIGNAL:
        return []

    return L + E + G


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


def GetRandomColor():
    return (randint(200, 255), randint(200, 255), randint(200, 255))


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
