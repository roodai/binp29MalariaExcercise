# Malaria Case Study
A phylogenetic analysis of malaria parasites
## Software used
GeneMark-ES Suite 4.62\
BLAST 2.11.0+\
Proteinortho 6.0.33\
BUSCO 5.3.0
## Outline
- Annotate genomes with GeneMark
- Filter genes based on GC-content and minimun sequence length
- Perform BLAST search on filtered sequences
- Filter host sequences from parastes based on BLAST results and taxonomy databases
- Identify orthologs with Proteinortho and BUSCO
- Produce genes corresponding to common BUSCOs in all species

## Procedure
Genes were predicted in the Plasmodium vivax genome using GeneMark and with default parameters:


```shell
gmes_petap.pl --sequence Plasmodium_vivax.genome
```

The “--sequence” flag denotes the input sequence.

A provided script was modified to filter fasta files with GC length and minimum sequence length. The script is ran as such:

```shell
python GCminlenfilter.py input.genome output.genome
```

GC content was derived from literature to be 26%, minimum sequence lengths was given and set to 3000.

Genes were predicted for the new filtered haemoproteus genome:

```shell
gmes_petap.pl --sequence filteredHaemoproteustartakovskyi.genome --ES --min_contig 5000
```
The --ES flag denotes internal training and the --min_contig sets the minimum allowable contig size. internal training was used due to the absence of reference material, minimum contig size was chosen somewhat arbitralily but should produce good results as long as the contig size is not set too low.

Fasta sequences from the now annotated haemoproteus genome are produced:

```shell
gffParse.pl -i filteredHaemoproteustartakovskyi.genome -g filteredHemoproteus.gtf -c -p
```
The -i flag denotes the input fasta file, -g flag the input .gff file. The -c flag checks for stop codons within reading frames, shifts the reading frame to the two other options if one is found the outputs produced will be adjusted to have a reading frame without the internal stop codon. The -p flag also outputs a translation of the DNA as a amino acid fasta file.

Before the fasta files were generated the .gff file had to be modified, by removing the GC-content and lenght section from the headers, which we're all in the first field. The following sed command was used. Afterwards only the scaffold name was left in the first field, which seemingly fixes compatibility issues between Genemark .gff files and gffParse.pl. With this line of reasoning the issue is with gffParse.pl since it only extracts scaffold names if it's the only thing in the first field of the ehader.

```shell
sed "s/ GC=.*\tGeneMark.hmm/\tGeneMark.hmm/"
```

To discern the remaining avian derived scaffold the annotated sequences in the .gff file are used as queries in a blastp search against the SwissProt database.


```shell
blastp -query gffParse.faa -db SwissProt -evalue 1e-10 -out blastedHaemo.blastp
```

The -query flag denotes the input query which in this case is an amino acid sequence, -db denotes the database used. An e-value filter was set with the -evalue flag to a default value of 1^(-10) to ensure false positives are filtered from the search.

The blastp results were first parsed to produce the top target per hit with a python script ran as such:

```shell
python oneTargetBlastParser.py input.blastp output.blastp
```

The targets of avian origin are to be removed. For this the blastp table with one target per hit is cross referenced to a SwissProt fasta file (Swissprot.fasta) containing the fasta seqeunces of the data hosted in the SwissProt database, the newest version of which available at: ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz
which was used to determine the species origin of the targets.
To determine if the species are avian a taxonomy file (taxonomy.dat) from NCBI is used which is available at:
ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat

The targets determined to be avian are produced into the output.

The aforementioned operations are carried out by the listAvesTargets.py script, the section determining the avian species from the taxonomy file was copied from supplied code.

```shell
python listAvesTargets.py input.blastp reference.fasta taxonomy.dat output.txt
```

The produced list of gene IDs from targets of avian origins is cross referenced to the annotation file produced from the GC-content filtered file to determine what scaffolds match the gene IDs that need to be removed. The removeFromFasta.py script produces correct scaffold names from gene IDs and prints only scaffolds that are not in the gene IDs to the output and is run as such:

```shell
python removeFromFasta.py geneids.txt input.gtf input.fasta output.fasta
```


Genemark annotation was ran on the new fasta file without any avian sequence data.

```shell
gmes_petap.pl --sequence noAvesHemo.fasta --ES -min_contig 5000
```

Nucleotide and amino acid seuquences were made from the fasta and annotation files for all plasmodia, toxoplasma gondii and the avian origin filtered haemoproteus, with gffParse.pl. Just like before sed editing was performed.

Proteinortho was used to determine otrhologs for all species.

```shell
nohup proteinortho6.pl {Ht,Pb,Pc,Pf,Pk,Pv,Py,Tg}.faa &
```
Busco was used to generate orhtologs for all species thusly:

```shell
busco -i species.faa -o species -m prot -l apicomplexa
```
The flag -i denotes input, -o the output, -m the mode for busco which for this case is proteins. The lineage for busco is chosen with the flag -l, for our species the lineage apicomplexa was used, which contains the plasmodia, the haemoproteus and the toxoplasma species used.

The script buscoParsing.py takes busco result tables and corresponding fasta files as input. It produces the ratio of complete or duplicate busco entries to all busco entries per table. It will then compare busco entries for all species included as input and produce the amount of common ones. The main function of the script is to produce corresponding gene IDs to the common busco entries in an ordered fashion. The script should then produce an output file per common busco entry that has the gene ID and sequence per species included, this feature is currently no included but the script is coded with this function in mind. The script can be ran as such:

```shell
python buscoParsing.py species1.tsv species2.tsv species3.tsv species1.faa species2.faa species3.faa
```
The script can be run for any number of species as long as the tables are included first and tha fasta files second.
