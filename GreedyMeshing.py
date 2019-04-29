import pygame
import sys
from noise import pnoise2

pygame.init()
(width, height) = (800, 600)


class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = z

    def __add__(self, other):
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)

    def __sub__(self, other):
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z)

    def __mul__(self, other):
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __repr__(self):
        return F"Vec3({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return self.__repr__()

    # Swizzling
    @property
    def xy(self):
        return self.x, self.y

    @property
    def xz(self):
        return self.x, self.z

    @property
    def yz(self):
        return self.y, self.z

    @property
    def xyz(self):
        return self.x, self.y, self.z


def main():
    screen = pygame.display.set_mode((width, height))
    FPS = 60
    clock = pygame.time.Clock()

    tiles_per_row = 30

    tiles = fill_data(tiles_per_row)

    greedy_mesh(tiles, tiles_per_row, tiles_per_row)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        draw_tiles(screen, tiles, tiles_per_row, width, height)

        pygame.display.update()


def draw_tiles(screen, tiles, tiles_per_row, width, height):
    w = width / tiles_per_row
    h = height / tiles_per_row
    for i, j, k in zip(tiles[0::3], tiles[1::3], tiles[2::3]):
        pygame.draw.polygon(
            screen,
            3 * [(i.z / 100 * 255 + j.z / 100 * 255 + k.z / 100 * 255) % 255],
            [[i.x * w, i.y * h], [j.x * w, j.y * h], [k.x * w, k.y * h]],
            0
        )
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            [[i.x * w, i.y * h], [j.x * w, j.y * h], [k.x * w, k.y * h]],
            1
        )


def fill_data(tiles_per_row):
    tiles = []
    n = tiles_per_row ** 2
    for i in range(n):
        vec1 = Vec3(i % tiles_per_row, i // tiles_per_row, 0.0)
        vec2 = Vec3(i % tiles_per_row, i // tiles_per_row + 1.0, 0.0)
        vec3 = Vec3(i % tiles_per_row + 1.0, i // tiles_per_row + 1.0, 0.0)
        tiles.append(vec1)
        tiles.append(vec2)
        tiles.append(vec3)

    for i in range(n):
        vec1 = Vec3(i % tiles_per_row, i // tiles_per_row, 0.0)
        vec2 = Vec3(i % tiles_per_row + 1.0, i // tiles_per_row, 0.0)
        vec3 = Vec3(i % tiles_per_row + 1.0, i // tiles_per_row + 1.0, 0.0)
        tiles.append(vec1)
        tiles.append(vec2)
        tiles.append(vec3)

    octaves = 1
    persistence = .5
    for i in tiles:
        i.z = int(100 * pnoise2(i.x / tiles_per_row, i.y / tiles_per_row, octaves, persistence))

    from collections import Counter

    [print((k, j)) for k, j in dict(Counter([i.z for i in tiles])).items()]
    print()

    return tiles


def greedy_mesh(tiles, width, height):
    mask = [None] * (width * height)



if __name__ == '__main__':
    main()
