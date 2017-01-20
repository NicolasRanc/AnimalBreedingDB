# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import rdpedfile
import wtcrossxlfl
import pedigree
from os.path import split

class filedialog(QWidget):
	"""filedialog class is QApplication that shows graphical interface for LievreDB
	with methods:
	getfiles that allows importing input file
	runanalysis that allows user to select type of analysis to run and launch it"""
	
	def __init__(self, parent=None):
		"""This is method for graphical interface"""
		super(filedialog, self).__init__(parent)

		#Declare global variables
		self.fullname = str		
		self.filename = str
		self.folder = str
		self.pedigree_dict= {}
		
		#Define the highest level Layout (level1)
		layout = QVBoxLayout()
		self.btn1=QPushButton("Choisir fichier")
		pedigree_dict = self.btn1.clicked.connect(self.getfiles)#import file when clicking on btn1
		layout.addWidget(self.btn1)
		
		#Define Grid layout (level2)
		grid=QGridLayout()
		
		self.chk1=QCheckBox("CrossTable")
		grid.addWidget(self.chk1,1,1)
		
		self.chk2=QCheckBox("Relatedness")
		grid.addWidget(self.chk2,2,1)
		
		self.treshlab=QLabel("seuil apparentement :")
		grid.addWidget(self.treshlab,2,2)
		
		self.tresh=QDoubleSpinBox()
		self.tresh.setRange(0.000,1.000)
		self.tresh.setSingleStep(0.005)
		self.tresh.setDecimals(3)
		self.tresh.setValue(0.100)
		grid.addWidget(self.tresh,2,3)
		
		self.btnRun=QPushButton("Lancer Analyse(s)")
		self.btnRun.clicked.connect(self.runanalysis)#launch select analysis from QCheckBox is checked and click on BtnRun
		grid.addWidget(self.btnRun,2,4)
		
		#Add grid to first level Layout
		layout.addLayout(grid)

		#Add QTextEdit to first level Layout
		self.contents=QTextEdit()
		layout.addWidget(self.contents)
		
		#Parameter to Add Layout to self (Qapplication)
		self.setLayout(layout)
		self.setGeometry(300,200,600,400)
		self.setWindowIcon(QIcon('iconwin.png'))
		self.setWindowTitle("Animal Breeding DB")
		
	def getfiles(self):
		"""getfiles method that open system window to select file
		(restricted to csv) and import it. The function return
		importing message about success or errors"""
		dlg=QFileDialog()#open system window to select file
		dlg.setFileMode(QFileDialog.ExistingFile)#only existing file
		dlg.setFilter("csv files (*.csv)")#restricted to csv format
		if dlg.exec_():
			self.fullname = dlg.selectedFiles()[0]
			folder_file_names = split(self.fullname)
			self.filename = folder_file_names[1]
			self.folder = folder_file_names[0]
		try:
			input_dict = rdpedfile.read_ped_file(self.fullname)#if import is successful
			self.contents.append("<span style=\"color:#008B00;\" >" +#green
			                     str(self.filename) +
			                     "	chargé avec succès" +
			                     "</span>")
			self.pedigree_dict = pedigree.Pedigree(input_dict)
			
		except MultipleEntriesError as pedfile_error:#if problem of multiple entries declared
			self.contents.append("<span style=\"color:#ff0000;\" >" +#red
			                     str(self.filename) +
			                     " - " +
			                     str(pedfile_error) +
			                     "</span>")

		except InputFormatError as pedfile_error:#if problem of unexpected format
			self.contents.append("<span style=\"color:#ff0000;\" >" +#red
			                     str(self.filename) +
			                     " - " +
			                     str(pedfile_error) +
			                     "</span>")
			
	def runanalysis(self):
		"""runanalysis method is a function that is launched when clicking on btnRun.
		It look at checkbox options for analysis, run the selected analysis and print message
		when analysis are done. Print an error if nothing is selected."""
		if self.chk1.isChecked() or self.chk2.isChecked():
			if self.chk1.isChecked():
				wtcrossxlfl.wrtcrossxls(self.pedigree_dict.cross_table(), "Cross", 1,self.folder)
				self.contents.append("<span style=\"color:#008B00;\" >" +#green
				                     "Analyse Cross réalisée avec succès" +
				                     "</span>")
			if self.chk2.isChecked():
				wtcrossxlfl.wrtcrossxls(self.pedigree_dict.related_table(), "Relatedness", self.tresh.value(),self.folder)
				self.contents.append("<span style=\"color:#008B00;\" >" +#green
				                     "Analyse Relatedness réalisée avec succès" +
				                     "</span>")
		else:
			self.contents.append("<span style=\"color:#ff0000;\" >" +#red
			                     "Erreur: au moins une option sélectionnée avant de lancer l'analyse" +
			                     "</span>")

def main():
	app = QApplication(sys.argv)
	ex = filedialog()
	ex.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
