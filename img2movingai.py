# Convert an image into a MovingAI .map file.
# @author Davide Aversa <thek3nger@gmail.com>
# @version 1.0.0

import sys

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

def img2movingai(filename, output=None):
    """
    The main algorithm.
    """
    if output is None:
        output = filename + ".map"

    img = load_image(filename)
    img_matrix = img.load()

    width, height = img.size

    with open(output, 'w') as f:
        f.write("type octile\n")
        f.write("height " + str(height) + "\n")
        f.write("width " + str(width) + "\n")
        f.write("map\n")

        for y in range(height):
            line = ""
            for x in range(width):
                line += color_to_char(img_matrix[x,y])
            line += "\n"
            f.write(line)

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
    if not is_reversed:
        img2movingai(filename)
    else:
        movingai2img(filename)
