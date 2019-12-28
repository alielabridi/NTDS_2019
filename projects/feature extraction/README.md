# Feature extraction process

In order to extract features from the given dataset it is being preprocessed using a shell script so that the actuall feature extraction in python then can be done easier.

## Preprocessing
The given data, which is already sorted along the column "src" is being fully copied and sorted along the column "dst". The columns "src" and "dst" in the copied dataset are then swapped and the numerical value 10 is added to the last column (5) in order to being able to identify the _doubled_ data. Both files are then being sort merged into a new file which then consist of all edges (in and outgoing) for each node gathered together. Since each edge is therefore listed twice the file size is double, however performing local feature extraction reduces to simple algebraic computations that can be done fast. Furthermore this way of processing the data allows to extract the features from the whole dataset rather than sampling first which would alter the feature space.

## Feature extraction
The preprocessed file is being loaded in individual chunks and in each chunk the features are calculated.

The following features are extracted:

* deg_tot: degree of a node
* deg_out: degree for outgoing edges (deg_in = deg_tot - deg_out)
* uni_neigh: number of unique neighbors of a node
* nr_of_bidirect: number of bidirectional (in & out) relations

To be implemented
* deg_weight: degree weigthed with the scarcity of the relations
* deg_strong: number of strong relations (several different interactions)
* rel_div: diversity of relations
