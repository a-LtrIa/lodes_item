import pandas as pd

# 读取 Excel 文件
file_path = '干员名单.xlsx'  # 文件路径
df = pd.read_excel(file_path, engine='openpyxl')  # 使用 openpyxl 引擎读取

# 获取第二列的所有人名
names = df.iloc[:, 1].tolist()  # iloc[:, 1] 表示第二列，tolist() 转换为列表

# 打印结果
print(names)