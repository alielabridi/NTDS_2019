start=`date +%s`

BASEDIR=$(dirname "$0")
cd $BASEDIR

# create second file, swapping column 3&4, adding 10 to col 5 (identifier for duplicate data)

awk -F $'\t' 'BEGIN{OFS=FS;}{t=$i;$i=$j;$j=t;$5+=10;}1' i=3 j=4  relations.csv > buffer.csv

# sort new file in column order 3,5,4
sort -n -k 3,3 -k 5,5 -k 4,4 -o buffer.csv buffer.csv


# merge sort both files
sort -n -k 3,3 -k 5,5 -k 4,4 -m relations.csv buffer.csv > relations_extended.csv

# rm buffer.csv

echo "Duration: $((($(date +%s)-$start)/60)) minutes"