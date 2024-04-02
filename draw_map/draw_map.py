import sys 
import math 
import numpy             as np
import matplotlib.pyplot as mpl
from   matplotlib import colors
 
# === Drawing function  ==============================================

def draw(map_values) -> None:
    ''' Converts the map (views, obstacle) into percentage in [0, 1] 
        or 2 in not viewed, then draws it with colors (see belox).
    '''
    # --- convert the map into 2D values -----------------------------
    # get the map sizes (l,c): l lines, c columns, 2 integers for each
    map_sizes = ( len(map_values), len(map_values[0]) )
    # create an equivalent: l lines, c columns, 1 percentage
    values = [ [ 0 for j in range(map_sizes[1]) ]
               for i in range(map_sizes[0]) ]
    for i in range(map_sizes[0]):      # for each line
        for j in range(map_sizes[1]):  # for each column
            # if the cell has not been viewed (unknown)
            if (map_values[i][j][0] == 0):
                values[i][j] = 2       # set percent. out of [0,1]
            else:  # otherwise, set it to ratio obstacle/views
                values[i][j] = (map_values[i][j][1] 
                                / map_values[i][j][0])
            # debug: OK
            # print(f'm({i},{j})={values[i][j]}')
    # debug: print the values computed
    #print(values) 
    
    # colormap : 3 colors + grey
    cmap = colors.ListedColormap(['white', 'orange', 'red', 'grey'])
    # the values' limit: white fo 0-25%, orange for 25-75%,
    #                    red for 75-100%, grey for unknown
    bounds = [0, .25, .75, 1.25, 2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # clear the figure
    mpl.clf()
    # use it to draw the data with the colormap
    mpl.imshow(values, cmap=cmap, norm=norm)
    # add the grid's lines
    mpl.grid(which='major', axis='both',
             linestyle='-', color='k', linewidth=1)
    # get them at the right place, with no label
    mpl.xticks(np.arange(-.5, map_sizes[1], 1), []);
    mpl.yticks(np.arange(-.5, map_sizes[0], 1), []);

    # display the figure
    mpl.show()

 
# === Main function and module call ==================================

# Using a main function is cleaner than having global variables
# and function calls.

def main() -> int:
    # reads a file given as first parameter, or default to map.txt
    fl_nm    = sys.argv[1] if (len(sys.argv) > 1) else 'map.txt'

    # --- read the real values from the given file ---------------
    # each line is a sequence of o,v separed by a space
    # (o = number of times an obstacle was seen in the cell,
    #  v = number of views of the cell)
    with open(fl_nm, 'r') as map_file:
        map_lines  = map_file.readlines()     # get the lines
        map_height = len(map_lines)           # their number
        map_width  = map_lines[0].count(',')  # number of couples
        map_sizes  = (map_height, map_width) 

        # we fill the square with default values
        map_values = [ [ [0, 0] for j in range(map_width)]
                       for i in range(map_height)]
        # debug: OK
        #print(f'Map is {map_height}x{map_width}')

        for i in range(map_height):  # for each line
            map_list = map_lines[i].split('  ')  # separate cells
            for j in range(map_width):           # for each cell
                # get both string values
                str_array = map_list[j].split(',')
                # convert the string to integer
                for k in [0,1]:
                    map_values[i][j][k] = int(str_array[k])
                # debug: OK
                # print( 'm({0},{1})=({2},{3})'.format(i, j,
                #                                      map_values[i][j][0],
                #                                      map_values[i][j][1]) )

        # once map is read, show it
        draw(map_values)

    return 0

# When this module is called, it starts the main function.
if __name__ == "__main__":
    sys.exit( main() )
