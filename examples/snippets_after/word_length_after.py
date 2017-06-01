from sys import argv


def average_word_length(file_name):
    with open(file_name, 'r') as file:
        contents = file.read()

    words = contents.split(' ')
    summed_word_length = sum([len(word) for word in words])

    return float(summed_word_length) / len(words)

if __name__ == '__main__':
    filename = argv[1]

    avg_word_length = average_word_length(filename)
    print "Average word length '{}' is {}".format(filename, avg_word_length)
