# -*- coding: utf-8 -*-

import xlsxwriter
import time
import os

def wrtcrossxls(input_dict, type_dict, threshold, folder):
	"""function to write dictionnary {(ind1,ind2):value} into excel file with conditionnal
	formatting according to threshold into user defined folder
	attributes are:
	--input_dict = input dictionnary
	--type_dict = type of dictionnary (used to define name of xls file and the way threshold is used)
	--threshold = threshold for conditionnal formatting
	--folder = destination folder"""
	
	os.chdir(folder)
	
	list_of_keys = list(input_dict.keys())
	
	list_of_key1 = []
	list_of_key2 = []
	for index in list_of_keys:
		list_of_key1.append(index[0])
		list_of_key2.append(index[1])

	listOfAnimal = list(set(list_of_key1) | set(list_of_key2))
	listOfAnimal.sort()
	list_len = len(listOfAnimal)
	
	time_string = time.strftime("%d%b%Y-%H%M%S")
	
	wb = xlsxwriter.Workbook('{0}{1}.xls'.format(type_dict,time_string))#add date in name of file
	
	ws = wb.add_worksheet()
	
	#Create specific cell format
	format_false = wb.add_format({'bg_color': '#FFC7CE','font_color':'#9C0006'})#Light red background with dark red text
	format_true = wb.add_format({'bg_color': '#C6EFCE','font_color':'#006100'})#Light green background with dark green text
	
	#Create first row specific format with text rotation and border
	format_first_row = wb.add_format({'rotation': -90,'border':1})
	
	#Create overall cell format with border
	format_overall=wb.add_format({'border':1})
	
	if type_dict == "Relatedness":#reverse conditional formating when Relatedness type of output
		format_true,format_false = format_false,format_true
	
	ws.conditional_format(1,1,list_len,list_len,{'type':     'cell',
                                                 'criteria': '<',
                                                 'value':    threshold,
                                                 'format':   format_false})
	
	ws.conditional_format(1,1,list_len,list_len,{'type':     'cell',
                                                 'criteria': '>=',
                                                 'value':    threshold,
                                                 'format':   format_true})
	
	
	col=0
	row=0
	
	#write first row with all entries
	for col in range(list_len):
		ws.write(0, col+1, listOfAnimal[col],format_first_row)
	#fill the file row per row starting with name and following with subsequent values
	for row in range(list_len):
		ws.write(row+1, 0, listOfAnimal[row], format_overall)
		for col in range(list_len):
			cross = input_dict[(listOfAnimal[col], listOfAnimal[row])]
			ws.write(row+1, col+1, cross, format_overall)
	
	#Define overall sheet and printable format
	ws.set_row(0,70.0)
	ws.set_column(1,list_len,3.0)
	ws.print_area(0,0,list_len,list_len)
	ws.set_landscape()
	
	wb.close()

if __name__ == "__main__":
    from os import chdir,getcwd
    chdir("/home/nicolas/Animal_Breeding_DB/")
    import pedigree
    import rdpedfile
    file_name = "Lievre_Odile_16.csv"
    test = pedigree.Pedigree(rdpedfile.read_ped_file(file_name))
    matrix1 = test.related_table()
    matrix2 = test.cross_table()
    wrtcrossxls(matrix1,"RelatednessResults",0.1,getcwd())
    wrtcrossxls(matrix2,"CrossResults",1,getcwd())
