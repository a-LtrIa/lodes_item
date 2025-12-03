import chardet


peoples = []    
with open("干员分类.csv", "r",encoding="utf-8-sig") as f:
    for line in f:
        print(line)
        peoples.append(line.strip())

print(peoples)