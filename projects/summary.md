# Project Summary: Spammers on Social Networks

## Motivation:
The goal of the project is to implement a model/algorithm capable of classifying users of a social media network as "spammers" or "not spammers" based on their interactions with other users and a limited set of features.

## Dataset:
We opted for the "Social Spammers" dataset from UC Stanta Cruz. The dataset is a graph of interaction between the users of the social network Tagged.com.
- It contains 5.6M users and 858M links between them. Each user has 4 features and is labeled as "spammer" or "not spammer".
- Each link represents an action between two users. The network contains 7 anonymized types of links.

## Graph:
Unsurprisingly:
- Vertices: Users
- Edges: Interactions


## Challenges:
- Size of the dataset: due to its large volume (>2 Gb), the dataset can't be processed easily as is. Sampling methods will be necessary.
- Features: Apart from the types of interactions, there are only 4 features tied to the users, meaning "classic" classifying approaches might not be good enough

## Engineering:
// We should put here what techniques and tools we think we'll have to use and a lot of buzzwords
- Downsampling: This essentially means that we have to find a representative subset of the vertices. However, since the network is connected this will mean to break/neglect edges which in turn introduces an error.
- Extract graph features: Due to the structure of the dataset more features can be extracted from the different interaction graphs. To begin with the deegres, the clustering coefficients and the number of triangles can be added as features to explore their correlation with the "spammer" label.
- Classification: To classify the constructed feature graph we then have to deploy a classification algorithm that works best with the given data structure. As to start with we might compare the linear vs. nonlinear methods learned in class with each other (PCA, MDS vs. Isomap, Laplacian Eigenmaps, LLE).

## Conclusion:

