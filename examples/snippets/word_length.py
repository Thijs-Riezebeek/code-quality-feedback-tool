from sys import argv


def average_word_length(file_name):
    with open(file_name, 'r') as file:
        contents = file.read()

    return sum([len(word) for word in contents.split(' ')]) / float(len(contents.split(' ')))

if __name__ == '__main__':
    filename = argv[1]

    avg_word_length = average_word_length(filename)
    print "Average word length '{}' is {}".format(filename, avg_word_length)
