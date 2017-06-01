# This program takes a length, width and height as command line arguments
# and calculates the volume that corresponds to these values
from sys import argv


def args_are_valid():
    if len(argv) != 4:
        return False

    for arg in argv[1:]:
        if not arg.isdigit():
            return False

    return True

if __name__ == '__main__':
    if not args_are_valid():
        print "Invalid input, example execution: ",\
            argv[0], " <length> <width> <height>"

        exit()

    # CLI arguments cast to int because they are always strings
    box_length = int(argv[1])
    box_width = int(argv[2])
    box_height = int(argv[3])

    volume = box_length * box_width * box_height

    print "Box volume is ", volume, "for height: ",\
        box_height, ", width ", box_width, " and length ", box_length


