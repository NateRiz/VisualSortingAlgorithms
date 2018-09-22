import pygame
import sys
from random import shuffle
from math import sqrt, ceil
from time import sleep
from threading import Thread


class MinHeap:
    def __init__(self, data=None):
        self.heap = []
        if data:
            self.heapify(data)

    def __len__(self):
        return len(self.heap)

    def push(self, val):
        self.heap.append(val)
        self._percolate_up(len(self.heap) - 1)

    def pop(self):
        if not len(self.heap):
            raise IndexError("Attempted to pop an empty heap.\n")
        self._swap(0, len(self.heap) - 1)

        popped = self.heap.pop()
        self._percolate_down(0)
        return popped

    def heapify(self, data):
        self.heap = data
        [self._percolate_down(i) for i in reversed(range(len(data)))]

    def _parent(self, pos):
        return (pos - 1) // 2

    def _left(self, pos):
        return 2 * pos + 1

    def _right(self, pos):
        return 2 * pos + 2

    def _swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

        UpdateDisplay(n-len(self.heap)+a, self.heap[a])
        UpdateDisplay(n-len(self.heap)+b, self.heap[b])

    def _has_left(self, pos):
        return self._left(pos) < len(self.heap)

    def _has_right(self, pos):
        return self._right(pos) < len(self.heap)

    def _percolate_up(self, pos):
        if pos != 0:
            if self.heap[pos] < self.heap[self._parent(pos)]:
                self._swap(pos, self._parent(pos))
                self._percolate_up(self._parent(pos))

    def _percolate_down(self, pos):
        if self._has_left(pos):
            left = self._left(pos)
            small = left
            if self._has_right(pos):
                right = self._right(pos)
                if self.heap[right] < self.heap[left]:
                    small = right
            if self.heap[pos] > self.heap[small]:
                self._swap(pos, small)
                self._percolate_down(small)


pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
mh = [i for i in range(0, 2000)]
shuffle(mh)
n = len(mh)
QUIT_SIGNAL = False
offset = 0
if n <= 100:
    offset = ceil(sqrt(100 - n))
delay = 0 / 1000  # Milli



def main():
    for i in range(n): pygame.draw.rect(screen, WHITE, (i * (width / n), height - (mh[i] * (height / n)), (width / n) - offset, height))
    pygame.display.update()
    unsorted = MinHeap(mh)
    HeapSort(unsorted)
    while not QUIT_SIGNAL:
        sleep(delay)


def HeapSort(min_heap):
    new_list = []
    for i in range(len(min_heap)):
        new_list.append(min_heap.pop())
        UpdateDisplay(i, new_list[i], (0, 255, 0))

        sleep(delay)
        if QUIT_SIGNAL:
            return

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
