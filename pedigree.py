# -*- coding: utf-8 -*-

class Animal:
	"""Class of animals with name, parents, sex and cross selection attributes"""
	def __init__(self,nom,parents,cross,sex):
		self.nom = nom
		self.parents = parents
		self.cross = int(cross)
		self.sex = sex
		#add status (dead/alive)
		#add year
		
	def __repr__(self):
		return "Animal: name({}),male({}),female({}),sex({})".format(	self.nom,
																		self.parents[0],
																		self.parents[1],
																		self.sex)

class Pedigree(dict):
	"""Class of Dictionnary for animal pedigree objects with methods for ancestry analysis
	and cross selection based on ancestry
	methods are:
	grand_parents_list:     retrieve grand parents of animal.
	test_common_parents:    test (True/False) if two animals share common parent.
	ancestors_list:         retrieve list of ancestors for one animal.
	test_common_par_grdpar  test (True/False) if two animals share parent as grand parent and vice versa.
	test_common_grdpar:     test (True/False) if two animals share common grand parent.
	cross_decision:         test if two animal can be crossed together (no common parents or
	                        grand parents.
	cross_table:            create a dictionnary (key = (ind1, ind2)) with results for cross decision if animal are
	                        selected for being crossed (1 as Animal.cross attribute)      
	relatedness:            create a dictionnary (key = (ind1, ind2)) with results of relatedness between all animals.
	                        (see http://www.agroparistech.fr/svs/genere/uvf/GP/Phi/appli2.htm for
	                        calculations)
	related_table:          create a dictionnary (key = (ind1, ind2)) with results for relatedness if animals are
	                        selected for being crossed (1 as Animal.cross attribute)                  
	"""
	
	def __init__(self,dict=None):
		"""Method to copy dictionnary of pedigree into Pedigree object"""
		self.data = {}
		if dict is not None: self.update(dict)

	def grand_parents_list(self,indiv):
		"""Method to extract list of grand parents from name (key in Pedigree)"""
		list_grand_parents = []
		pedigree = self[indiv].parents
		try:#allow to check for individual in pedigree that are not declared
			for ancestor in pedigree:
				for i in self[ancestor].parents:
					if i not in list_grand_parents: #add the grandparent to the list if grand parent not in list of grandparent
						list_grand_parents.append(i)
		except KeyError:
			list_grand_parents = []
			
		return list_grand_parents


	def test_common_parents(self,male,female):
		"""Method that test if two individuals shared a knwon common parents"""
		commonPar = False
		if self[male].parents[0] == self[female].parents[0] or self[male].parents[1] == self[female].parents[1]:
			commonPar = True
		return commonPar


	def ancestors_list(self,individus,count = 1):
		"""Parse pedigree tree and retreive dict of ancestors for one animal (iterative analysis)."""
		ancestor_dict = {}
		try:
			for x in self[individus].parents:
				ancestor_dict[x]=count
				self.ancestors_list(x,count+1)
		except KeyError:
			pass
		return ancestor_dict


	def test_common_par_grdpar(self,male,female):
		"""test (True/False) if two animals share parent as grand parent and vice versa"""
		male_grand_parents = self.grand_parents_list(male)
		female_grand_parents = self.grand_parents_list(female)
		commonParGrPar = False
		for individual in male_grand_parents:
			if individual in self[female].parents:
				commonParGrPar = True
		for individual in female_grand_parents:
			if individual in self[male].parents:
				commonParGrPar = True
		return commonParGrPar
		

	def test_common_grdpar(self,male,female):
		"""Method that test if two individuals shared a known common grand parents"""
		male_grand_parents = self.grand_parents_list(male)
		female_grand_parents = self.grand_parents_list(female)
		commongrPar = False
		for individual in male_grand_parents:
			if individual in female_grand_parents:
				commongrPar = True
		return commongrPar
		
	def cross_decision (self,indiv1,indiv2):
		"""Method that give True or False value if crossing is accepted"""
		parentCommun = self.test_common_parents(indiv1,indiv2)
		grandParentCommun = self.test_common_grdpar(indiv1,indiv2)
		parGrParCommun = self.test_common_par_grdpar(indiv1,indiv2)

		crossing = parentCommun or grandParentCommun or parGrParCommun
		
		if crossing == True:
			crossing = False
		else:
			crossing = True
		
		return crossing
		
	def cross_table (self):
		"""create a dictionnary (key = (ind1, ind2)) with results for cross decision if animal
		are selected for being crossed (1 as Animal.cross attribute)"""
		list_of_progenies = []
		for relatives in [x for x in self if self[x].cross == 1]:
			list_of_progenies.append(relatives)
		cross_tab = {}
		for x in list_of_progenies:
			for y in list_of_progenies:
				if self.cross_decision(x,y):
					cross_tab[(x,y)] = 1
				else:
					cross_tab[(x,y)] = 0
		return cross_tab
	   
	def relatedness(self):
		"""create a dictionnary (key = (ind1, ind2)) with results of relatedness between all animals.
	    (see http://www.agroparistech.fr/svs/genere/uvf/GP/Phi/appli2.htm for calculations)"""

		#get list of progenies, dams, sires and mates
		list_of_progenies = list(self.keys())
		list_of_mates = [self[relatives].parents for relatives in self]
		list_of_parents = set([self[relatives].parents[0] for relatives in self]) | set([self[relatives].parents[1] for relatives in self])
		
		total_nb_ind = len(set(list_of_progenies) | list_of_parents)
		
		#calculation of relatedness for founders
		relatedness_dict = {}
		founders = [i for i in list_of_parents if i not in list_of_progenies]
		
		for j in founders:
			for i in founders:
				if j == i:
					relatedness_dict[(j,i)] = 1.0/2
				else:
					relatedness_dict[(j,i)] = 0.0
		
		#Prepare list of total parents that will be solved first 
		solving_mates = []
		solved_individuals = founders[:]
		
		#loop for all nodes of the pedigree
		while 1:
			if solving_mates == []:
				#Define mates that will be used to solved for highest node of pedigree
				solving_mates = [x for x in relatedness_dict.keys() if x in list_of_mates]#Extract mates that are already in relatedness_dict 
				test_mates = solving_mates[:]
			else:
				#Define mates that will be used to solved for below nodes of pedigree
				solving_mates = [x for x in list(relatedness_dict) if x in list_of_mates and x not in test_mates]
				test_mates.extend(solving_mates)
			#First loop to calculate relatedness between progeny and parents + within progeny inbreeding
			for mate_tuple in solving_mates: #mates to be analyzed
				for progeny,animal in self.items():
					if animal.parents == mate_tuple: #for each progeny(ies) calculate relatedness with each parents + inbreeding coef
						relatedness_dict[(progeny,progeny)] = 1.0/2*(1 + relatedness_dict[mate_tuple])#inbreeding
						relatedness_dict[(progeny,mate_tuple[0])] = relatedness_dict[(mate_tuple[0],progeny)]=1.0/2*relatedness_dict[(mate_tuple[0],mate_tuple[0])] + 1.0/2*relatedness_dict[(mate_tuple[0],mate_tuple[1])]
						relatedness_dict[(progeny,mate_tuple[1])] = relatedness_dict[(mate_tuple[1],progeny)]=1.0/2*relatedness_dict[(mate_tuple[1],mate_tuple[1])] + 1.0/2*relatedness_dict[(mate_tuple[0],mate_tuple[1])]
						solved_individuals.append(progeny)
			#Seconf loop to calculate relatedness between progenies and and other individuals in top of tree
			for progeny,animal in self.items():
				if animal.parents in solving_mates:
					for z in solved_individuals:
						if z != progeny and (progeny,z) not in relatedness_dict:
							if z not in self.keys():
								relatedness_dict[(progeny,z)] = relatedness_dict[(z,progeny)] = 0		
							else:
								p = self[progeny].parents[0]
								pprim = self[z].parents[0]
								m = self[progeny].parents[1]
								mprim = self[z].parents[1]
								relatedness_dict[(progeny,z)] = relatedness_dict[(z,progeny)]=(
								1.0/4*relatedness_dict[(p,pprim)] +
								1.0/4*relatedness_dict[(p,mprim)] +
								1.0/4*relatedness_dict[(m,pprim)] +
								1.0/4*relatedness_dict[(m,mprim)])
			if len(relatedness_dict) >= total_nb_ind**2:
				break

				
		return relatedness_dict
	
	def related_table (self):
		"""create a dictionnary (key = (ind1, ind2)) with results for relatedness if
		animals are selected for being crossed (1 as Animal.cross attribute)"""
		list_of_progenies = [x for x in self if self[x].cross == 1]
		relatedness_dict = self.relatedness()
		related_tab = {}
		for x in list_of_progenies:
			for y in list_of_progenies:
				related_tab[(x,y)] = relatedness_dict[(x,y)]
		return related_tab

if __name__=="__main__":
	from os import chdir
	chdir("/home/nicolas/Animal_Breeding_DB/")
	import rdpedfile
	file_name = "Test.csv"
	test = rdpedfile.read_ped_file(file_name)
	test = Pedigree(test)
	print(test)
	matrix1 = test.related_table()
	matrix2 = test.cross_table()
	print(matrix1,"\n")
	print(matrix2,"\n")
