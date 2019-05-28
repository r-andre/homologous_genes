#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Applied Programming for Bioinformatics
Final project
runscript.py
'''

import re
#from re import search # returns an 'defined but unused' error, despite them
#from re import match  # being used later

# opening the data files
# storing their contents line for line in a variable for further use
# closing the data files

DATA0 = open("./data/eggnog4.species_list.txt")
SPEC_LIST = DATA0.readlines()
DATA0.close()

DATA1 = open("./data/meNOG.members.tsv")
MENOG_MEMBERS = DATA1.readlines()
DATA1.close()

DATA2 = open("./data/meNOG.annotations.tsv")
MENOG_ANNOTATIONS = DATA2.readlines()
DATA2.close()

DATA3 = open("./data/eggnog4.functional_categories.txt")
FUNCT_CAT = DATA3.readlines()
DATA3.close()

'''
1. Write a program that takes two species names as input and calculates how
many genes (proteins) in the first species have at least one corresponding
(linked via an ortholog group) homolog in the other species. Note that several
proteins (paralogs) in one species can belong to the same ortholog group.
The species should be chosen at runtime via command line arguments, not
hardcoded. Only species listed in eggNOG should be considered.
'''

# defining input species names (via manual input) and variables that later
# store their name, tax id, and other information

SPECIES0 = input("Please enter a species name (eg. Trichoplax adhaerens) and "
                 + "press 'enter':\n")
SPECIES1 = input("Please enter a species name (eg. Ictidomys "
                 + "tridecemlineatus) and press 'enter':\n")
#SPECIES0 = "Trichoplax adhaerens"
#SPECIES1 = "Ictidomys tridecemlineatus"
#TAXID0 = ""
#TAXID1 = ""
#GROUP0 = []
#GROUP1 = []
FOUND_SPEC_LIST = ""
#found_group = []

# defining a function to check line for line if the input species names are
# listed in the data file. if they are found, their information is stored in
# a designated file

def check_if_listed(species_name):
    global FOUND_SPEC_LIST
    for line in SPEC_LIST:
        if re.match((species_name + "\t"), line):
            FOUND_SPEC_LIST = FOUND_SPEC_LIST + line
            return True
        else: pass

# checking the data file for both input species names, if they are found their
# corresponding variable storing a boolean value is set to 'True', if they are
# not found it is set to 'False'

FOUND_SPECIES0 = check_if_listed(SPECIES0)
FOUND_SPECIES1 = check_if_listed(SPECIES1)

#print(FOUND_SPEC_LIST)

# only if both input species names are listed in the data file, another
# variable storing a boolean value is set to true (allowing the program to run
# further) confirming it by showing a short (optional) 'success' message.
# otherwise the program will end with an 'error' message (because the code that
# follows after depends on the boolean returning 'True')

if FOUND_SPECIES0 == True and FOUND_SPECIES1 == True:
    LOOK_FOR_GENES = True
    print("Success! Found both input species names in the meNOG database.")
#    input("Please press 'enter' to continue.")
else: print("Error! You did not provide two valid species names as input. "
            + "Maybe the species you provided are not listed in meNOG? "
            + "Please try again.")

# the rest of the program is dependent on this 'if' condition, because if not
# both of the input species names can be found in the data files, the the
# program is redundant. a short (optional) message confirms the start of it

if LOOK_FOR_GENES == True:
    print("\nAlright, let's do this...\n")

#    print(FOUND_SPEC_LIST)

# defing a function to find the tax id of a species name by searching for it in
# the variable that stores the species information. it cuts out all the other
# information and returns only the tax id

    def acquire_taxid(species_name):
        species_taxid = re.search(species_name + "\t\d+\t", FOUND_SPEC_LIST)
        species_taxid = species_taxid.group(0)
        species_taxid = species_taxid.replace(species_name + "\t", "")
        species_taxid = species_taxid.replace("\t", "")
        return species_taxid

# acquiring the tax id of both species names and storing them in corresponding
# variables

    TAXID0 = acquire_taxid(SPECIES0)
    TAXID1 = acquire_taxid(SPECIES1)

# defining a function to find the ortholog group of species by searching for it
# in the variable that stores information of meNOG members. it cuts out all the
# other information and returns only the group name(s) the gene of a species
# belongs to by adding them to a list

    def find_group(species_taxid):
        species_group = []
        for line in MENOG_MEMBERS:
            if re.search(species_taxid + ".", line):
                found_group = line
                found_group = found_group.replace("meNOG\t", "")
                found_group = found_group.split("\t", 1)[0]
#                print(found_group)
                species_group.append(found_group)
            else: pass
        return species_group

# finding the group names of the ortholog group of species and storing them as
# lists in corresponding variables

    GROUP0 = find_group(TAXID0)
    GROUP1 = find_group(TAXID1)

# finding common ortholog groups among species genes and printing them to the
# screen with a short message

    COMMON_GROUPS = set(GROUP0) & set(GROUP1)
    print(str(len(COMMON_GROUPS)) + " genes of " + SPECIES0 + " have at "
          + "least one corresponding (linked via an ortholog group) homolog "
          + "in " + SPECIES1 + ".\n")
#    input("Please press 'enter' to continue.")

    print("Proceeding to part 2...\n")

    '''
    2. Let’s use this code and data to look for genes with a restricted
    taxonomic distribution. Using human genes as a reference point, examine the
    following

    a) How many of the human (Homo sapiens) genes that do not have a homolog in
    mouse (Mus musculus), but have at least one homolog in chimp (Pan
    troglodytes)?
    For sanity checking: the answer should be around 1500 to 2000
    '''

# setting up variables that store the requested species information, using the
# functions defined before

    SPECIES2 = "Homo sapiens"
    check_if_listed(SPECIES2)
    TAXID2 = acquire_taxid(SPECIES2)
    GROUP2 = find_group(TAXID2)

    SPECIES3 = "Mus musculus"
    check_if_listed(SPECIES3)
    TAXID3 = acquire_taxid(SPECIES3)
    GROUP3 = find_group(TAXID3)

    SPECIES4 = "Pan troglodytes"
    check_if_listed(SPECIES4)
    TAXID4 = acquire_taxid(SPECIES4)
    GROUP4 = find_group(TAXID4)

# defining a function that looks for an element that is not in one list, but in
# another, and adds that element to a new list

    def find_common_uncommon(species0, species1, species2):
        com_uncom = []
        for elem in species0:
            if elem not in species1:
                if elem in species2:
                    com_uncom.append(elem)
                else: pass
            else: pass
        com_uncom = set(com_uncom)
        return com_uncom

# finding all genes of one species that do not have homologs in another
# species, but that do have homologs in a third species, and reporting the
# total number of those genes

    UN_COMMON = find_common_uncommon(GROUP2, GROUP3, GROUP4)

    print("(a) " + str(len(UN_COMMON)) + " human genes that do not have "
          + "a homolog in mouse, have at least one homolog in chimp.\n")
#    input("Please press 'enter' to continue.")

    '''
    b) What are their protein ids? Store this in a results file.
    '''

# defining a function that looks for the protein ids of a list of ortholog
# groups in a data file and stores them in a dedicated text file omitting
# duplicate entries

    def find_proteinid(species_id):
        unique_id = []
        output_file = open("./results/protein_ids.txt", "w+")
        for elem in UN_COMMON:
            for line in MENOG_MEMBERS:
                if re.search("meNOG\t" + elem + "\t", line):
                    protein_id = re.search(species_id + ".\D+\d+", line)
                    if protein_id:
                        unique_id.append(protein_id.group(0))
                    else: pass
                else: pass
        unique_id = set(unique_id)
        for elem in unique_id:
            output_file.write(elem + "\n")
        output_file.close()

# finding the protein ids of a set of ortholog groups, storing them in a
# 'result' file, and confirming this action with a message

    find_proteinid(TAXID2)

    print("(b) The requested file containing the protein ID's can now be "
          + "found in './results/protein_ids.txt'.\n")

    '''
    c) Is there any corresponding (metazoan level) functional description
    available from eggNOG for those genes? If so, which functional categories
    do the orthologous groups (NOGs) that they appear in have, and how many
    proteins in each category? (store this in a formatted results file)
    '''

# defining a function that searches for protein counts and functional
# categories of elements of a set of ortholog groups that in a data file, and then
# stores the results including the group name in a dedicated text file. it
# omits groups that do not have a functional description in the data file

    def find_functional_things(ortholog_groups):
        output_file = open("./results/functional_category.txt", "w+")
#        output_file.write("group name\tprotein count\tfunctional "
#                           + "category\n")
        for elem in ortholog_groups:
            for line in MENOG_ANNOTATIONS:
                if re.search(elem, line) and not re.search("\tNA", line):
                    protein_count = re.search(elem + "\t\d+", line).group(0)
                    funct_cat = re.search("\t\D+\t", line).group(0)
                    output_file.write(protein_count + "\t" + funct_cat + "\n")
                else: pass
        output_file.close()

# finding protein count and functional categories of a set of ortholog groups,
# storing them in a 'result' file, and confirming this action with a message

    find_functional_things(UN_COMMON)

    print("(c) The requested file containing the functional categories of the "
          + "orthologous groups can now be found in "
          + "'./results/functional_categories.txt'.\n")

    '''
    3. Are there any rodent specific genes, i.e. genes in orthologous groups
    that only contain mouse (Mus musculus) and rat (Rattus norvegicus)
    proteins, but no other species? If so, what are the corresponding
    orthologous groups, protein ids, and what are their (metazoan ortholog
    group level description) functions?
    For sanity checking: the answer should be Very Very Few.
    '''

# META NOTE: i was not able to solve this part...

    input("Part 3 is missing...\nPress 'enter' to quit.")
