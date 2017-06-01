from numpy import random, sqrt

if __name__ == '__main__':
    x1, x2 = random.random(), random.random()
    y1, y2 = random.random(), random.random()
    z1, z2 = random.random(), random.random()

    distance = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2) + pow((z1 - z2), 2))

    print "Distance: ", distance

