# 統計 shot 長度的分布圖
# -----------------
import matplotlib.pyplot as plt
# 畫圖
def draw(result):
    plt.bar(result.keys(), result.values(), width=2, bottom=None, align='center', data=None)
    # plt.xticks(rotation='統計圖')
    # plt.axhline(y=100, c="r", ls="--", lw=2)
    print("total of GEI is",sum(result.values()))
    plt.title("shot of statistical diagram")
    plt.xlabel("shot")
    plt.ylabel("number")
    plt.show()
def main():
    result = dict()
    shot = 0
    time = 0
    with open("./cut~3.csv") as file:
        for line in file:
            time += 1
            line = line.strip().split(",")
            # cut
            if line[1] == "1" and shot != 0:
                if shot in result.keys():
                    result[shot] += 1
                else:
                    result[shot] = 1
                shot = 0
                continue
            elif line[1] == "0":
                shot += 1
        print("x 軸, y 軸")
        for key in sorted(result.keys()) :
            print(key,"    " , result[key])
        # print("x軸",list(result.keys()))
        # print(list(result.values()))
        draw(result)

main()