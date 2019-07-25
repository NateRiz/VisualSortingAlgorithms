"""
Idea from https://leetcode.com/problems/pancake-sorting/
Given an array A, we can perform a pancake flip:
We choose some positive integer k <= A.length,
then reverse the order of the first k elements of A.
We want to perform zero or more pancake flips
(doing them one after another in succession) to sort the array A.
"""

import pygame
import sys
from random import shuffle, randint, seed
from math import sqrt, ceil
from time import sleep
from threading import Thread

pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
unsorted_temp = [i for i in range(1, 20)]
seed(0)
shuffle(unsorted_temp)
unsorted = []
for i in range((len(unsorted_temp)+1)//5):
    print(i*10, i*10+10, i)
    unsorted += sorted(unsorted_temp[i*5: i*5 + 5], reverse=randint(0, 1))
n = len(unsorted)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 800 / 1000  # Milli


def main():
    for i in range(n):
        pygame.draw.rect(screen, WHITE,
                         (i * (width / n), height - (unsorted[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()

    while not QUIT_SIGNAL:
        if sorted(unsorted) != unsorted:
            PancakeSort(unsorted)


def PancakeSort(unsorted):
    for i in range(n-1, -1, -1):
        big = i
        for j in range(i-1, -1, -1):
            if unsorted[big] < unsorted[j]:
                big = j
        if big != i:
            swap(unsorted, big, i)
        sleep(delay)
        UpdateDisplay(i, (0, 255, 0))
        if QUIT_SIGNAL:
            return

    [UpdateDisplay(i, (0, 255, 0)) for i in range(n)]


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

def get_color():
    return (100+randint(0,155), 100+randint(0,155), 100+randint(0,155))

def swap(arr, i, j):
    color = get_color()
    for n in range((i + 1) // 2):
        arr[n], arr[i - n] = arr[i - n], arr[n]

    for n in range(i):
        UpdateDisplay(n, color)
        sleep(delay/10)

    color = get_color()
    sleep(delay)

    for n in range((j + 1) // 2):
        arr[n], arr[j - n] = arr[j - n], arr[n]

    for n in range(j):
        UpdateDisplay(n, color)
        sleep(delay/10)

if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
