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
unsorted = [i for i in range(1, 2000)]
shuffle(unsorted)
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 4 / 1000  # Milli


def main():
    global unsorted
    for i in range(n):
        pygame.draw.rect(screen, WHITE,(i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()

    while not QUIT_SIGNAL:
        if sorted(unsorted) != unsorted:
            unsorted = MergeSort(unsorted)


def MergeSort(S, offset=0):

    n = len(S)
    if n > 1:
        A, B = S[:n // 2], S[n // 2:]
        A = MergeSort(A, offset)
        if QUIT_SIGNAL:
            return S
        B = MergeSort(B, offset + n//2)
        if QUIT_SIGNAL:
            return S
        S = Merge(A, B, offset)
        sleep(delay)
    return S


def Merge(A, B, offset):
    S=[]
    i, j = 0, 0
    color = GetRandomColor()
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            S.append(A[i])
            UpdateDisplay(offset + i + j, A[i], color)
            i += 1
        else:
            S.append(B[j])
            UpdateDisplay(offset + i + j, B[j], color)
            j += 1
    while i < len(A):
        S.append(A[i])
        UpdateDisplay(offset + i + j, A[i], color)
        i += 1
    while j < len(B):
        S.append(B[j])
        UpdateDisplay(offset + i + j, B[j], color)
        j += 1
    return S


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
    pygame.draw.rect(screen, color, (i * (width / n), height - (j * (height / n)), (width / n) - offset, height))
    pygame.display.update()

def GetRandomColor():
    return (randint(200,255), randint(200,255), randint(200,255))


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
