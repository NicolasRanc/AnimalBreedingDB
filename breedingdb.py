import sqlite3
import pedigree
import rdpedfile
from os import chdir

chdir("/home/nicolas/Animal_Breeding_DB/")
file_name = "Lievre_Odile_16.csv"
test = rdpedfile.read_ped_file(file_name)

#create table for progenies
conn = sqlite3.connect('./db/lievredb.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS progenies(
   	id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
   	name TEXT NOT NULL,
   	male_parent TEXT DEFAUT NULL,
   	female_parent TEXT DEFAUT NULL,
   	sex TEXT DEFAUT NULL,
   	birth_year TEXT DEFAUT NULL,
   	FOREIGN KEY(male_parent) REFERENCES temp_progenies(id),
   	FOREIGN KEY(female_parent) REFERENCES temp_progenies(id)
   	)
""")
conn.commit()

def get_animal_from_db():
	actual_animal_db={}
	cursor.execute("""SELECT id, name FROM progenies""")
	rows = cursor.fetchall()
	for row in rows:
		actual_animal_db[row[1]]=row[0]
	return actual_animal_db

def set_animal_to_db(list_to_db):
	cursor.executemany("""
	INSERT INTO progenies(name, male_parent,female_parent,sex,birth_year) VALUES(?, ?, ?, ?, ?)""", list_to_db
	)
	conn.commit()

progenies_to_db=list()

for individuals,pedigree_ind in test.items():
	if pedigree_ind.cross==0:
		progenies_to_db.append([
		individuals,
		pedigree_ind.parents[0],
		pedigree_ind.parents[1],
		pedigree_ind.sex,
		"NULL"])

actual_progenies_db=get_animal_from_db()

list_of_animal = [i[0] for i in progenies_to_db]
list_of_male = set([i[1] for i in progenies_to_db])
list_of_female = set([i[2] for i in progenies_to_db])

female_founders = [n for n in list_of_female if n not in actual_progenies_db.keys()]
male_founders = [n for n in list_of_male if n not in actual_progenies_db.keys()]

founders_to_db = []
for i in [n for n in female_founders if n not in founders_to_db]:
	founders_to_db.append([i,"NULL","NULL","femelle","NULL"])

for i in [n for n in male_founders if n not in founders_to_db]:
	founders_to_db.append([i,"NULL","NULL","male","NULL"])

set_animal_to_db(founders_to_db)


while 1:
	actual_progenies_db=get_animal_from_db()
	prepare_to_db = [n for n in progenies_to_db if n[1] in actual_progenies_db.keys() and n[2] in actual_progenies_db.keys()]
	#prepare_to_db devient vide après le premier loop???
	if prepare_to_db == []:
		break
	else:
		for i in prepare_to_db:
			i[1] = actual_progenies_db[i[1]]
			i[2] = actual_progenies_db[i[2]]
			cursor.execute("""
			INSERT INTO progenies(name, male_parent,female_parent,sex,birth_year) VALUES(?,?,?,?,?)""", i)
	conn.commit()

conn.close()


#Create function to load single animal in db


#cursor = conn.cursor()
#cursor.execute("""
#DROP TABLE progenies
#""")
#conn.commit()


#create table for precalculated relatedness
#cursor = conn.cursor()
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS progenies(
#     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#     parent_male_id INTEGER NOT NULL,
#     parent_female_id INTEGER NOT NULL,
#     relationship, REAL, DEFAUT NULL)
#""")
#
#con.commit()


##create table for crosses
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS progenies(
#     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name TEXT,
#     male_parent,
#     female_parent,
#     sex,
#     birth_year,)
#""")


#create table for weaning (sevrage=
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS progenies(
#     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name TEXT,
#     male_parent,
#     female_parent,
#     sex,
#     birth_year,)
#""")
