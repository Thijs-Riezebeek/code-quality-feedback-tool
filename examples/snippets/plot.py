import matplotlib as plt

def plotje(x_list, y_list, title, x_title, y_title):
    """
    @return: a plot for 2 lists and titles for the graph and axes
    """
    plt.figure()
    plt.plot(x_list, y_list, 'r-')
    # input-lists for x and y; plotted with a red line
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.axis([find_minimum(x_list), find_maximum(x_list), find_minimum(y_list), find_maximum(y_list)])
    # assigns values to the axes
    plt.show()
