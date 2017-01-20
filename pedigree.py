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
		"""Parse pedigree tree and retreive list of ancestors for one animal."""
		ancestor_list = []
		try:
			for x in self[individus].parents:
				ancestor_list.append((x,count))
				ancestor_list.extend(self.ancestors_list(x,count+1))
		except KeyError:
			pass
		return ancestor_list


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
		list_of_fathers = [i[0] for i in list_of_mates]
		list_of_mothers = [i[1] for i in list_of_mates]

		total_nb_ind = len(set(list_of_progenies) | set(list_of_fathers) | set(list_of_mothers))

		#calculation of relatedness for founders
		relatedness_dict = {}
		female_founders = [i for i in list_of_mothers if i not in list_of_progenies]
		male_founders = [j for j in list_of_fathers if j not in list_of_progenies]

		for j in male_founders:
			for i in male_founders:
				if j == i:
					relatedness_dict[(j,i)] = 1/2
				else:
					relatedness_dict[(j,i)] = 0

		for j in female_founders:
			for i in female_founders:
				if j == i:
					relatedness_dict[(j,i)] = 1/2
				else:
					relatedness_dict[(j,i)] = 0

		for j in male_founders:
			for i in female_founders:
				relatedness_dict[(j,i)] = 0
				relatedness_dict[(i,j)] = 0
		
		#Prepare list of total parents that will be solved first 
		solving_mates = []
		solved_individuals = set(female_founders)|set(male_founders)
		
		#loop for all nodes of the pedigree
		while 1:

			if solving_mates == []:
				solving_mates = [x for x in list(relatedness_dict) if x in list_of_mates]#Define mates that will be solved for highest node of pedigree
				test_mates = solving_mates[:]
			else:
				solving_mates = [x for x in list(relatedness_dict) if x in list_of_mates and x not in test]#Define mates that will be solved for below nodes of pedigree
				test_mates.extend(solving_mates)

			#First loop to calculate relatedness between progeny and parents + within progeny inbreeding
			for tuple_mate in solving_mates: #mates to be analyzed (ind1,ind2)
				# enumerate indexes the list. Index of progeny(ies) for a single cross from list of Mates
				for progeny in [index for index,y in enumerate(list_of_mates) if y == tuple_mate]:#for each progeny(ies)
					progeny_for_relatedness = list_of_progenies[progeny]#get progeny name from index
					relatedness_dict[(progeny_for_relatedness,progeny_for_relatedness)] = 1/2*(1+relatedness_dict[tuple_mate])#inbreeding from parent of progeny_for_relatedness (in y)
					relatedness_dict[(progeny_for_relatedness,tuple_mate[0])] = relatedness_dict[(tuple_mate[0],progeny_for_relatedness)]=1/2*relatedness_dict[(tuple_mate[0],tuple_mate[0])]
					relatedness_dict[(progeny_for_relatedness,tuple_mate[1])] = relatedness_dict[(tuple_mate[1],progeny_for_relatedness)]=1/2*relatedness_dict[(tuple_mate[1],tuple_mate[1])]
					
					solved_individuals.add(progeny_for_relatedness)
			
			#Seconf loop to calculate relatedness between progeny and and other individuals
			for tuple_mate in solving_mates:
				# enumerate indexes the list. Index of progeny(ies) for a single cross from list of Mates
				for progeny in [index for index,y in enumerate(list_of_mates) if y == tuple_mate]:#for each progeny(ies)
					progeny_for_relatedness = list_of_progenies[progeny]#get progeny name from index

					for z in [z for z in solved_individuals if z != progeny_for_relatedness]:
						
						if ((progeny_for_relatedness,z) not in relatedness_dict and
						   (z,progeny_for_relatedness) not in relatedness_dict):
							ancestors = [val for sublist in self.ancestors_list(progeny_for_relatedness) for val in sublist]

							if z in ancestors:
								chain_ancestry = ancestors[ancestors.index(z)+1]
								relatedness_dict[(progeny_for_relatedness,z)] = relatedness_dict[(z,progeny_for_relatedness)]=(1/2)**(chain_ancestry+1)

							elif z not in self.keys():
								relatedness_dict[(progeny_for_relatedness,z)] = relatedness_dict[(z,progeny_for_relatedness)] = 0

							else:
								p = self[progeny_for_relatedness].parents[0]
								pprim = self[z].parents[0]
								m = self[progeny_for_relatedness].parents[1]
								mprim = self[z].parents[1]
								relatedness_dict[(progeny_for_relatedness,z)] = relatedness_dict[(z,progeny_for_relatedness)]=(
								1/4*relatedness_dict[(p,pprim)] +
								1/4*relatedness_dict[(p,mprim)] +
								1/4*relatedness_dict[(m,pprim)] +
								1/4*relatedness_dict[(m,mprim)])
			
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
	file_name = "Lievre_Odile_16.csv"
	test = rdpedfile.read_ped_file(file_name)
	test = Pedigree(test)
	matrix1 = test.related_table()
	matrix2 = test.cross_table()
	print(matrix1,"\n")
	print(matrix2,"\n")
