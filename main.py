from PIL import Image
import keyboard
from time import sleep

PALETTE = {}
X_OFFSET = 64
Z_OFFSET = 64
Y_OFFSET = 70  # make sure this is higher than the highest existing block in the region


def set_palette():
    block_types = ["terracotta", "concrete"]
    colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "blue", "purple", "green", "brown", "red", "black"]
    p = Image.open("palette.png")
    p.convert("RGB")
    for i, block_type in enumerate(block_types):
        for j, color in enumerate(colors):
            r, g, b = p.getpixel((i*6, j*6))
            PALETTE[(block_type, color)] = (r, g, b)


def get_nearest(r, g, b):
    curr_min = 1000000000
    curr_key = None
    for key in PALETTE:
        value = PALETTE[key]
        this_min = (r-value[0])**2 + (g-value[1])**2 + (b-value[2])**2
        if this_min < curr_min:
            curr_min = this_min
            curr_key = key
    return curr_key


def set_block(block_name, x, y):
    keyboard.press_and_release('t')
    sleep(.07)
    keyboard.write(f'/setblock {x} {Y_OFFSET} {y} minecraft:{block_name}\n')
    sleep(.07)


def main():
    im = Image.open("image.png")
    im.convert("RGB")
    converted_image = {}
    for i in range(im.width):
        for j in range(im.height):
            r, g, b = im.getpixel((i, j))
            converted_image[(i, j)] = get_nearest(r, g, b)
    sleep(5)
    for xy in converted_image:
        print(xy)
        print(converted_image[xy])
        block_string = converted_image[xy][1] + "_" + converted_image[xy][0]
        set_block(block_string, xy[0]+X_OFFSET, xy[1]+Z_OFFSET)


if __name__ == "__main__":
    set_palette()
    main()