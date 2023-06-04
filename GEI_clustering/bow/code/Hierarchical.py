import numpy as np
import csv
import sys
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

# Create linkage matrix and then plot the dendrogram
def plot_dendrogram(model):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)
    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix,color_threshold=max(model.distances_)*0.2)

# def main(folder,inputData,size):
def main(folder,inputData,size,cutType,year):
    # 要分多少群
    readData = []
    name = []
    inputFile = f"./bow/data/{year}/{cutType}/{folder}/{inputData}_{size}.csv"
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
                name.append(row[0])
            except:
                pass
    # setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(compute_distances=True)
    model = model.fit(readData)
    # plot the top three levels of the dendrogram
    plot_dendrogram(model)
    plt.title(f"{inputData}_{size}.csv")
    plt.show()
if __name__ == "__main__":
    # inputFile = "../data/accumulate/GEI_level_2.csv"
    # main(inputFile)
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])