## make_GEI
### step
切 cut(1、2、3) -> 疊GEI(4) -> 正規化(5) -> 畫圖(6) and GEI 正規化後的結果 K-means 分群(1、2)
### cut
1. CountLevelNum.py
    > 輸入PM2.5原始資料，判斷每小時10*10的空汙圖每一格的等級，輸出每張圖各等級數量
    > output 存放在 countLevelNum
    > 切 cut 前置作業
    >   - input: 2018micro.csv
    >   - output: 2018micro_CountNum.csv
    > 正規化後的 GEI 分群
    >   - input: GEI_origin_regular.csv、GEI_Level_regular.csv
    >   - output:GEI_origin_regular_countNum.csv、GEI_Level_regular_countNum.csv

2. cluster.py
    > 用 k-means 分群
    > output 存放在 clstering
    > cut 前置作業
    >   - input: 2018micro_countNum.csv
    >   - output:2018micro_cluster.csv
    > 正規化後的 GEI 分群
    >   - input: GEI_origin_regular_countNum.csv、GEI_Level_regular_countNum.csv
    >   - output:GEI_origin_regular_cluster.csv、GEI_Level_regular_cluster.csv

3. cut.py
    > 現在檢查的這一張和前張的所屬群不同，此張視為cut
    > cut 和 cut 之間 (shot)，圖片數量至少為 3 張
    > - input: 2018micro_cluster.csv
    > - output: 2018micro_cut.csv
### 準備的數據
-  2018micro.csv
-  level.csv
1. covertToLevel.py
    > 將原始數據轉為空汙 PM2.5 等級劃分
    > - input: 2018micro.csv 
    > - ouput: level.csv
### GEI
4. GEI.py
    > 將cut和cut之間的shot疊成GEI
    > output 存放在 GEI_data
    > - input: 2018micro.csv、2018level.csv、cut~3.csv
    > - outpput:GEI_origin.csv、GEI_level.csv
    > 數據結果: 發現某幾筆數據特別大 (NO.1301 -> 1145、1146)，其餘大部分落在 0~45

5. regular.py
    > 將資料正規化
    > output 存放在 GEI_regular
    > - input: GEI_origin.csv、GEI_level.csv
    > - output: GEI_origin_regular.csv、GEI_level_regular.csv

6. userDataPic.py
    > 將數據畫圖
    > 越黑代表越乾淨，越白代表空汙越嚴重
    > - input: GEI_origin_regular.csv、GEI_level_regular.csv
    > - output: GEI 圖片
## contrast切
1. regular.py
    > 將資料正規化 --- 單張 GEI 正規化(凸顯特徵用，所以顏色不表示空汙的絕對等級)
    > - input: GEI_origin.csv、GEI_level.csv
    > - output: GEI_origin_singleRegular.csv、GEI_level_singleRegular.csv
2. userDataPic.py
    > 畫圖
    > - input: GEI_origin_singleRegular.csv、GEI_level_singleRegular.csv
    > - output: GEI 圖片
