from os import chdir
chdir("/home/nicolas/Animal_Breeding_DB/")
import rdpedfile
import pedigree
#file_name = "Test.csv"
#file_name = "Lievre_Odile_16.csv"
file_name = "comet.csv"
test = rdpedfile.read_ped_file(file_name)
test = pedigree.Pedigree(test)

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
	#Seconf loop to calculate relatedness between progeny and and other individuals in top of tree
	for progeny,animal in self.items():
		if animal.parents in solving_mates:#for progeny, test if parents correpsond to mate
			for z in solved_individuals:#estimate relatedness of progeny with solved individuals only
				if z != progeny and (progeny,z) not in relatedness_dict:#work only if realtedness not calculated
					if z not in self.keys():#Test if z is founders level1
						#print("if 54",progeny,z)
						#ancestry = test.ancestors_list(progeny)	
						#if z in [indiv for indiv in ancestry.keys()]:
						#	print("if 65",progeny,z)#never ran
						#	chain_ancestry = ancestry[z]
						#	relatedness_dict[(progeny,z)] = relatedness_dict[(z,progeny)]=(
						#	(1.0/2)**(chain_ancestry+1))*(1+relatedness_dict[(z,z)])
						#else:
						#	relatedness_dict[(progeny,z)] = relatedness_dict[(z,progeny)] = 0
						relatedness_dict[(progeny,z)] = relatedness_dict[(z,progeny)] = 0		
					else:# z is solved and declared as pedigree entry
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
