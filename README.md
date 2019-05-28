A small project for a bioinformatics course.

#### Data source

The [eggNOG database](http://eggnogdb.embl.de) (last accessed 2019-09-30) is used as main data source. EggNOG is a database that stores information on which genes in a particular species correspond (by an evolutionary relationship) to those of other species.

To run the program, the following files are needed (last accessed 2019-09-30):

http://eggnogdb.embl.de/download/eggnog_4.5/eggnog4.functional_categories.txt

http://eggnogdb.embl.de/download/eggnog_4.5/eggnog4.species_list.txt

http://eggnogdb.embl.de/download/eggnog_4.5/data/meNOG/meNOG.annotations.tsv.gz

http://eggnogdb.embl.de/download/eggnog_4.5/data/meNOG/meNOG.members.tsv.gz

(The latter two need to be unpacked first.)

All four files need to be placed in `/data/` in order for the script to work.

#### Description

`runscript.py` does the following things:

1. It takes two species names as input and calculates how many genes (proteins) in the first species have at least one corresponding (linked via an ortholog group) homolog in the other species. Only species listed in the specified eggNOG database are considered.

2. It looks through the data to look for genes with a restricted taxonomic distribution and examines the following, using human genes as a reference point:
  * How many of the human (Homo sapiens) genes that do not have a homolog in mice (Mus musculus), have at least one homolog in chimps (Pan troglodytes)?
  * What are these genes protein ID's?
  * Is there any corresponding (metazoan level) functional description from eggNOG available for those genes? If so, which functional categories do the orthologous groups (NOG's) that they appear in have, and how many proteins are in each category?

Output data is stored in `\results\functional_category.txt` and `\results\protein_ids.txt`.