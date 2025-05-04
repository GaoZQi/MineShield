import os
import pandas as pd

def merge_csv_files(output_file):
    input_folder = os.getcwd()  # 获取当前工作目录，也就是脚本所在的目录
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv') and f != 'merged_data.csv']

    # 用于存储所有数据的列表
    dataframes = []

    # 循环读取每个 CSV 文件
    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

    # 将所有 DataFrame 合并成一个
    merged_df = pd.concat(dataframes, ignore_index=True)

    # 保存合并后的数据到指定的输出文件
    merged_df.to_csv(output_file, index=False)
    print(f'合并后的 CSV 文件已保存为: {output_file}')


# 使用示例
output_file = 'Random_forest_data.csv'  # 输出合并后的 CSV 文件路径
merge_csv_files(output_file)
