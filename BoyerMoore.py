import pygame
import sys
from time import sleep
from threading import Thread

QUIT_SIGNAL = False
pygame.init()
pygame.font.init()
width, height = (800, 600)
screen = pygame.display.set_mode((width, height))
FPS = 30
clock = pygame.time.Clock()
font = None


class BoyerMoore:
    def __init__(self, orig, comp):
        self.original = orig
        self.compare = comp
        self.index = 0  # Wheres the left most index?
        self.sub_index = 0  # What character (from the right) are we at?
        self.char_width = font.render("X", 1, (0, 0, 0)).get_size()[0]
        self.comp_height = font.render(self.original, 1, (255, 255, 255)).get_size()[1] + 16
        self.reset_state = False
        self.count_state = False
        self.done_state = False
        self.move_count = 0
        self.answer = -1
        self.reset_screen()

    def update(self):
        orig_index = len(self.compare) + self.index - self.sub_index - 1
        comp_index = (-self.sub_index - 1) % len(self.compare)
        if self.done_state or orig_index > len(self.original):
            return
        if self.reset_state:
            self.reset_state = False
            self.reset_screen()
            return

        if self.count_state:
            self.count()
            return



        orig_char = self.original[orig_index]
        comp_char = self.compare[comp_index]
        correct = orig_char == comp_char
        color = (255, 0, 0)
        if correct:
            color = (0, 255, 0)
            if self.sub_index == len(self.compare)-1:
                self.answer = self.index
                self.done_state = True
                print("Answer: ", self.answer)
        char = font.render(orig_char, True, color)
        screen.blit(char, (self.char_width * orig_index, 0))
        char = font.render(comp_char, True, color)
        screen.blit(char, ((self.index + comp_index) * self.char_width, self.comp_height))


        self.sub_index += 1
        if not correct:
            self.count_state = True

        pygame.display.update()

    def count(self):
        if self.sub_index >= len(self.compare):
            self.index += 1
            self.sub_index = 0
            self.count_state = False
            self.reset_state = True
            return

        orig_index = len(self.compare) + self.index - self.sub_index + self.move_count
        comp_index = (-self.sub_index - 1) % len(self.compare)
        color = (255, 255, 0)
        orig_char = self.original[orig_index]
        comp_char = self.compare[comp_index]
        correct = orig_char == comp_char
        char = font.render(comp_char, True, color)
        screen.blit(char, ((self.index + comp_index) * self.char_width, self.comp_height))

        self.sub_index += 1
        self.move_count += 1
        if correct or self.sub_index >= len(self.compare):
            self.sub_index = 0
            self.index += self.move_count
            self.move_count = 0
            self.count_state = False
            self.reset_state = True

        pygame.display.update()

    def reset_screen(self):
        screen.fill((0, 0, 0))
        buffer = 16
        orig = font.render(self.original, True, (255, 255, 255))
        comp = font.render(self.compare, True, (255, 255, 255))
        screen.blit(orig, (0, 0))
        screen.blit(comp, (self.index * self.char_width, orig.get_size()[1] + buffer))


def main():
    global font

    original = "Testing1TestingTesting12Testing123Testing132"
    compare = "ting123T"
    font = get_font(max(len(original), len(compare)))
    delay = 300 / 1000  # n/1000 = n milliseconds
    substr = BoyerMoore(original, compare)

    while not QUIT_SIGNAL:
        substr.update()
        sleep(delay)


def CheckInput():
    global QUIT_SIGNAL
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT_SIGNAL = True
                return
        sleep(1)


def get_font(str_size):
    font = pygame.font.SysFont("Ubuntu.ttf", 8)
    prev_font = font

    i = 8
    while font.render("X", True, (0, 0, 0)).get_size()[0] * str_size <= 4 * width // 5:
        prev_font = font
        font = pygame.font.Font("Ubuntu.ttf", i)
        i += 2
    return prev_font


if __name__ == '__main__':
    Thread(target=CheckInput, ).start()
    main()
    pygame.quit()
    sys.exit(0)
