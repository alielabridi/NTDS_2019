start=`date +%s`

BASEDIR=$(dirname "$0")
cd $BASEDIR

# remove time information (reduce size)
awk '{print $3 "\t" $4 "\t" $5}' relations.csv > relations_red.csv

# create second file, swapping column 3&4, adding 10 to col 5 (identifier for duplicate data)

awk -F $'\t' 'BEGIN{OFS=FS;}{t=$i;$i=$j;$j=t;$3+=10;}1' i=1 j=2  relations_red.csv > buffer.csv

# sort new file in column order 1,3,2
sort -n -k 1,1 -k 3,3 -k 2,2 -o buffer.csv buffer.csv


# merge sort both files
sort -n -k 1,1 -k 3,3 -k 2,2 -m relations_red.csv buffer.csv > relations_red_ext.csv

rm relations_red.csv
rm buffer.csv

echo "Duration: $((($(date +%s)-$start)/60)) minutes"