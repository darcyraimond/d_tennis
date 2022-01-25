# A series of functions useful for handling .csv files in this project


# Import any required packages
from termcolor import colored


# ==================================================
# Content below this point
# ==================================================


def csv_to_lines(path):
    """
    Imports a .csv file at the given path, and returns an array with
    each line in the file as an element.

    Inputs:
        - path: file path to the .csv file

    Outputs:
        - out: array containing lines from the .csv file
    """
    out = []
    try:
        for line in open(path):
            out.append(line.strip())
        return out

    except FileNotFoundError:
        # Try to add .csv to the end of the file's name
        try:
            for line in open(path + ".csv"):
                out.append(line.strip())
            return out

        except FileNotFoundError:
            print(colored("Fatal Error:", "red"),
                    f"could not find file with path {path} or {path}.csv")
            exit(1)


def csv_to_cells(path, same_length=True):
    """
    Imports a .csv file at the given path, and returns a 2d array. The
    first dimension represents the rows of the file, while the second
    represents the columns.

    Inputs:
        - path: file path to the .csv file
        - same_length (optional, default True): asserts that the number
            of cells in each row must be the same

    Outputs:
        - out: 2d array containing cells from the .csv file 
    """
    lines = csv_to_lines(path)
    out = []
    row_length = None
    for line in lines:

        # Add row
        row = line.split(",")
        out.append(row)

        # Row length check
        if row_length is None:
            row_length = len(row)
        elif same_length:
            if row_length == len(row):
                pass
            else:
                print(colored("Fixable Error:", "yellow"),
                        "unmatched row lengths - need to fix this")
        
    return out


def cells_to_dicts(cells, header_row=0):
    """
    Takes a 2d array and converts to a 1d array of dictionaries, using
    the specified header row as the dictionary keys

    Inputs:
        - cells: 2d array of data
        - header_row (optional, default 0): row to be used as dictionary
            keys

    Outputs:
        - out: 1d array of dictionaries
    """
    headers = cells[header_row]
    out = []
    for i, row in enumerate(cells):
        if i == header_row: continue
        d = {}
        for j, cell in enumerate(row):
            d[headers[j]] = cell
        out.append(d)

    return out


def csv_to_dicts(path, header_row=0, same_length=True):
    """
    Imports a .csv file at the given path and returns a 1d array of
    dictionaries with one dictionary for each row of the file, using the
    specified header row as dictionary keys. This is running
    csv_to_cells followed by cells_to_dicts.

    Inputs:
        - path: file path to the .csv file
        - header_row (optional, default 0): row to be used as dictionary
            keys

    Outputs:
        - out: 1d array of dictionaries
    """
    cells = csv_to_cells(path, same_length)
    out = cells_to_dicts(cells, header_row)
    return out