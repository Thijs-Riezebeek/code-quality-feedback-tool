# This program takes a length, width and height as command line arguments and calculates the volume that corresponds to these values
from sys import argv

if __name__ == '__main__':
    if len(argv) != 4 or not argv[1].isdigit() or not argv[2].isdigit() or not argv[3].isdigit():
        print "Invalid input, example execution: ", argv[0], " <length> <width> <height>"
        exit()

    box_length = int(argv[1]) # Cast the length, width and height from command line to int, because command line args are strings
    box_width = int(argv[2])
    box_height = int(argv[3])

    print "Box volume is ", box_length * box_width * box_height, "for height: ", box_height, ", width ", box_width, " and length ", box_length
