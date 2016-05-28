# Convert an image into a MovingAI .map file.
# @author Davide Aversa <thek3nger@gmail.com>
# @version 1.0.0

import sys
import re
import random

from PIL import Image

from movingaiparser import parse_map

color_map = {
    'WALL': (0, 0, 0),
    'FREE': (255, 255, 255),
    'TREE': (0, 255, 0),
}

def load_image(filename):
    """
    Load an image file.

    @param filename The image filename
    @return an Image object.
    """
    return Image.open(filename)

def color_to_char(color):
    """
    Map each pixel color to a particular map tile.
    """
    # Trim to RGB
    color = (color[0], color[1], color[2])
    if color == color_map['WALL']:
        return "@"
    if color == color_map['FREE']:
        return "."
    if color == color_map['TREE']:
        return "T"
    # Any other color is a wall.
    return "@"

def char_to_color(char):
    """
    Map each char to a pixel color.
    """
    if char == '@':
        return color_map['WALL']
    if char == '.':
        return color_map['FREE']
    if char == 'T':
        return color_map['TREE']
    # Any other char is a wall.
    return color_map['WALL']

def color_to_key_or_door(color):
    """
    A key is any other  color (r,g,42) that open any door (42,g,b).
    """
    pass

def find_doors(image, size):
    width, height = size
    return [ (x,y) for x in range(width)
             for y in range(height)
             if image[x,y][0] == 42]

def img2movingai(filename, output=None):
    """
    The main algorithm.
    """
    if output is None:
        output = filename + ".map"

    img = load_image(filename)
    img_matrix = img.load()

    width, height = img.size

    doors = find_doors(img_matrix, (width, height))
    print(doors)
    key_door_template = ''
    if len(doors) > 0:
        for d in doors:
            key_door_template += "key $key$ {} {}\n".format(d[0], d[1])

    with open(output, 'w') as f:
        f.write("type octile\n")
        f.write("height " + str(height) + "\n")
        f.write("width " + str(width) + "\n")
        f.write(key_door_template)
        f.write("map\n")

        for y in range(height):
            line = ""
            for x in range(width):
                if (x,y) in doors:
                    line += '.'
                else:
                    line += color_to_char(img_matrix[x,y])
            line += "\n"
            f.write(line)

def instantiate_template(template_file):
    """
    Takes a template map and replace `$key$` with random keys.
    @param template_file: the path to the template file.
    """
    all_map = ''
    keys_num = 0

    parsed_map = parse_map(template_file)

    with open(template_file, 'r') as f:
        all_map = f.read()
        keys_num = all_map.count('$key')
        all_map = re.sub(r"\$key\$",r"{}",all_map)

    def random_free():
        rnd = parsed_map.random_free()
        return rnd[0]

    # Generate random keys.
    keys = [ "{} {}".format(*random_free()) for _ in range(keys_num)]

    with open(template_file + ".inst.map", 'w') as f:
        f.write(all_map.format(*keys))

def movingai2img(filename, output=None):
    """
    Convert a MovingAI map file into a PNG image.
    @param filename: Path to the MovingAI map.
    @param output: The name of the output PNG file.
    """
    if output is None:
        output = filename + ".png"

    parsed_map = parse_map(filename)
    output_image = Image.new('RGB', (parsed_map.width, parsed_map.height), color_map['WALL'])
    for x in range(parsed_map.width):
        for y in range(parsed_map.height):
            output_image.putpixel((x,y), char_to_color(parsed_map.matrix[y][x]))
    output_image.save(output)


if __name__ == '__main__':
    filename = sys.argv[1]
    is_reversed = len(sys.argv) > 2 and sys.argv[2] == '-R'
    templating = len(sys.argv) > 2 and sys.argv[2] == '-T'
    if is_reversed:
        movingai2img(filename)
    elif templating:
        instantiate_template(filename)
    else:
        img2movingai(filename)
