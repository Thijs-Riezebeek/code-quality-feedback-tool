import sys

if __name__ == "__main__":
    max_weight = 100

    # So when the weight provided through the first argument is larger than the max_weight, we print that it is not good. If it is below the max weight we print that it is good
    print "{} is good".format(sys.argv[1]) if int(sys.argv[1]) <= max_weight else "{} is not good".format(sys.argv[1])

    if sys.argv[1] > max_weight:  # Only if the weight argument is larger (not equal) to the max_weight do we print that it is good
        print "{} is good".format(sys.argv[1])
