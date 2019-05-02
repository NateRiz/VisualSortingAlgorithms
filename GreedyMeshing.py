import pygame
import sys
from noise import pnoise2

pygame.init()
(width, height) = (800, 600)

greedy_on = True
debug_lines = True

def print_z(tiles, w):
    for i, t in enumerate(tiles):
        if t:
            print(t.z, end="\t")
        else:
            print("N", end="\t")
        if not (i + 1) % w:
            print()

    print("\n\n\n")


class Mesher:
    def __init__(self, tiles, row_width, row_height):
        self.tiles = tiles
        self.width = row_width * 6
        self.height = row_height * 6
        self.quads = []

    def greedy_mesh(self):
        self.quads.clear()
        seen = set()
        # for i, t in enumerate(self.tiles):
        # print(t, end="\n" if not (i + 1) % self.width else " ")

        index = 0
        while index < len(self.tiles) and index not in seen:
            self.quads.append(self.tiles[index])  # Top Left

            w = index + 1
            end = (w + self.width - 1) // self.width * self.width
            while w < end and w not in seen and self.tiles[index].z == self.tiles[w].z:
                w += 1
            self.quads.append(self.tiles[w - 6 + 4])  # Top Right

            size = -1
            done = False
            for x in range(index // self.height, self.height//6):
                start = index
                end = w
                for y in range(start, end):
                    index2 = self.get_index(x, y % self.width)
                    if index2 not in seen and self.tiles[index].z != self.tiles[index2].z:
                        done = True
                        break

                if done:
                    break

                for y in range(start, end):
                    index2 = self.get_index(x, y % self.width)
                    seen.add(index2)

                size += 1

            self.quads.append(self.tiles[index + size * self.width + 1])  # bottom left
            self.quads.append(self.tiles[w - 6 + size * self.width + 2])  # bottom right

            index += 1
            while index < len(self.tiles) and index in seen:
                index += 1

    def get_index(self, a, b):
        return a * self.width + b

    def quads_as_tris(self):
        tris = []
        for q in range(len(self.quads[::4])):
            tris.append(self.quads[4 * q + 0])
            tris.append(self.quads[4 * q + 1])
            tris.append(self.quads[4 * q + 2])
            tris.append(self.quads[4 * q + 1])
            tris.append(self.quads[4 * q + 2])
            tris.append(self.quads[4 * q + 3])
        return tris


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
    FPS = 30
    clock = pygame.time.Clock()

    tiles_per_row = 40

    tiles = fill_data(tiles_per_row)
    if greedy_on:
        mesher = Mesher(list(tiles), tiles_per_row, tiles_per_row)
        mesher.greedy_mesh()
        tiles = mesher.quads_as_tris()
        print(F"Greedy Vertices: {len(tiles)}")
    draw_tiles(screen, tiles, tiles_per_row)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        pygame.display.update()


def draw_tiles(screen, tiles, tiles_per_row):
    w = width / tiles_per_row
    h = height / tiles_per_row
    for i, j, k in zip(tiles[0::3], tiles[1::3], tiles[2::3]):
        pygame.draw.polygon(
            screen,
            3 * [(75 + i.z / 100 * 255 + j.z / 100 * 255 + k.z / 100 * 255) % 255],
            [[i.x * w, i.y * h], [j.x * w, j.y * h], [k.x * w, k.y * h]],
            0
        )

        if debug_lines:
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
        vec1 = Vec3(i % tiles_per_row, i // tiles_per_row, 0.0)  # top left
        vec2 = Vec3(i % tiles_per_row, i // tiles_per_row + 1.0, 0.0)  # bottom left
        vec3 = Vec3(i % tiles_per_row + 1.0, i // tiles_per_row + 1.0, 0.0)  # bottom right

        vec4 = Vec3(i % tiles_per_row, i // tiles_per_row, 0.0)  # top left
        vec5 = Vec3(i % tiles_per_row + 1.0, i // tiles_per_row, 0.0)  # top right
        vec6 = Vec3(i % tiles_per_row + 1.0, i // tiles_per_row + 1.0, 0.0)  # bottom right

        tiles.append(vec1)
        tiles.append(vec2)
        tiles.append(vec3)
        tiles.append(vec4)
        tiles.append(vec5)
        tiles.append(vec6)

    print(F"Naive Vertices: {len(tiles)}")

    octaves = 1
    persistence = .5
    for i in range(len(tiles) // 6):
        for j in range(6):
            tiles[6 * i + j].z = int(
                100 * pnoise2(tiles[6 * i].x / tiles_per_row, tiles[6 * i].y / tiles_per_row, octaves, persistence))
    # from collections import Counter
    # [print((k, j)) for k, j in dict(Counter([i.z for i in tiles])).items()]

    return tiles


if __name__ == '__main__':
    main()
