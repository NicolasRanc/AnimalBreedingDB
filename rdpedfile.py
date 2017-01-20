# -*- coding: utf-8 -*-

import pedigree

class MyError(Exception):
    """Base class for exceptions in this module."""
    pass

class InputFormatError(MyError):
    """Exception raised for errors in the format of input file.
    Attributes:
    message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

class MultipleEntriesError(MyError):
    """Exception raised for errors if duplicated entries are found in input file.
    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        

def read_ped_file(file_name):
    """Function that read pedigree input file in the current directory and convert
    into rows into Animal object from pedigree module.
    """
    dict_of_related = {}
    row_index=0
    
    with open(file_name, "r") as file_source:

        for rows in file_source:#For all rows, in file
            rows = rows.strip()#split per row
            row_index=row_index+1
            if rows == "":#stop if reading empty row
                break
            if "Nom" not in rows:
                individual_row = rows.split(',')
                if len(individual_row)==5:
                    name = individual_row[0]#define name of Lievre
                    if name not in dict_of_related.keys():
                        dict_of_related[name] = pedigree.Animal(individual_row[0],
                                                                (individual_row[1],individual_row[2]),
                                                                 individual_row[3],
                                                                 individual_row[4])#append new Lievre to dictionnary
                    else:
                        raise MultipleEntriesError("Le fichier présente des entrées dupliquées à la ligne {0}".format(row_index))
                else:
                    raise InputFormatError("Le fichier présente un problème de format à la ligne {0}".format(row_index))
                
    return dict_of_related
 
if __name__ == "__main__":
    import pedigree
    from os import chdir
    chdir("/home/nicolas/Animal_Breeding_DB/")
    file_name = "Lievre_Odile_16.csv"
    test = read_ped_file(file_name)
    print(test)
    print(len(test))
