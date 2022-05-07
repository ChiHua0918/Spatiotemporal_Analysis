# 計算每一種方法的分群結果好壞，進行比較
# ANOVA 變異數分析、輪廓係數 兩種評斷方式
# ---------------------------------
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
from sklearn.cluster import KMeans
import csv
import pandas as pd

# Calinski-Harabaz Index
def CHIndex(k,data):
    kmeans_model = KMeans(n_clusters=k).fit(data)
    labels = kmeans_model.labels_
    return calinski_harabasz_score(data, labels)  
# 輪廓係數  Silhouette Coefficient
def SC(k,data):
    kmeans = KMeans(n_clusters=k).fit(data)
    return silhouette_score(data, kmeans.predict(data))
def main():
    data = ['GEI_Level_bow_2_cluster.csv',
            'GEI_Level_bow_3_cluster.csv',
            'GEI_origin_bow_2_cluster.csv',
            'GEI_origin_bow_3_cluster.csv']
    # data = ["GEI_Level_bow_2_col.csv",
    #         "GEI_Level_bow_2_leftDown.csv",
    #         "GEI_Level_bow_2_rightDown.csv",
    #         "GEI_Level_bow_2_row.csv",
    #         "GEI_origin_bow_2_col.csv",
    #         "GEI_origin_bow_2_leftDown.csv",
    #         "GEI_origin_bow_2_rightDown.csv",
    #         "GEI_origin_bow_2_row.csv",
    #         "GEI_Level_bow_3_col.csv",
    #         "GEI_Level_bow_3_leftDown.csv",
    #         "GEI_Level_bow_3_rightDown.csv",
    #         "GEI_Level_bow_3_row.csv",
    #         "GEI_origin_bow_3_col.csv",
    #         "GEI_origin_bow_3_leftDown.csv",
    #         "GEI_origin_bow_3_rightDown.csv",
    #         "GEI_origin_bow_3_row.csv"]
    scores = [] # 輪廓係數分數
    ss_value = [] # calinski_harabaz_score 分數
    file_cluster = []# 每一個 file 總共分了多少群
    print("quadrant、quadrantDecideNum")
    print("請問要選取哪一個資料夾:",end = " ")
    folder = input()
    for file in data:
        with open(f"./data/clustering/{folder}/{file}", newline= '') as csvfile :
            rows = csv.reader(csvfile, delimiter = ',')
            readData = [] # 數據
            cluster = []  # GEI 所屬群
            for row in rows :
                try:
                    readData.append(list(map(float,row[2:])))
                    cluster.append(int(row[1]))
                except:
                    pass
            # 計算輪廓係數分數 ，群數 0~?
            k = max(cluster)+1
            scores.append(SC(k,readData))
            ss_value.append(CHIndex(k,readData))
            file_cluster.append(k)
    result = {'k':file_cluster,'Silhouette Coefficient':scores,'Calinski-Harabaz Index':ss_value}
    show = pd.DataFrame(result,index=data)
    print(show)
if __name__ == "__main__":
    main()