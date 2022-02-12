import os
# 將原始 PM2.5 數據轉為等級
def cnn():
    file = ""
    print(f"python ./code/covertToLevel.py {file}")
    os.system(f"python ./code/covertToLevel.py {file}")

def main():
    cnn()
if __name__ == '__main__':
    main()