import csv
from common import read_uname2id_mapping_from_csv, get_registration_list
import pandas as pd

# 教学网原始格式是tsv，转换成csv，方便excel或python查看
def convert_tsv_to_csv(input_file, output_file):
    # 读取 TSV 文件并写入 CSV 文件
    with open(input_file, 'r', encoding='utf-8') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        with open(output_file, 'w', encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in tsv_reader:
                csv_writer.writerow(row)

def process_csv_file(input_file, output_file, uname2id):
    if uname2id is None:
        uname2id = read_uname2id_mapping_from_csv()
    # 读取注册表
    registration_df = get_registration_list()
    
    # 读取 CSV 文件
    df = pd.read_csv(input_file)
    df['学号'] = df['名字'].map(uname2id)

    # 要根据题目数量来看除以多少，不一定是5道题
    question_columns = [col for col in df.columns if col.isdigit()]
    total_questions = len(question_columns)
    df['成绩'] = df['通过数'] / total_questions * 10
    df['成绩'] = df['成绩'].round(2)  # 保留两位小数
    # 把学号和成绩放到前面

    df = df[['学号', '名字', '通过数', '成绩'] + question_columns]

    # 确保 '学号' 列的类型一致
    registration_df['学号'] = registration_df['学号'].astype(str)
    df['学号'] = df['学号'].astype(str)
    # 将注册表中的学号和成绩合并到原始数据中
    df = pd.merge(registration_df[['学号', '姓名']], df, on='学号', how='left')
    
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

if __name__ == '__main__':

    # # 将 TSV 文件转换为 CSV 文件
    # for i in range(1, 6):
    #     convert_tsv_to_csv(f'./raw/{i}.csv', f'./data/{i}.csv')

    # 读取 CSV ，插入一列mapping得到的id，然后根据通过数量计算成绩
    uname2id = read_uname2id_mapping_from_csv()
    for i in range(1, 6):
        process_csv_file(f'./data/{i}.csv', f'./output/{i}.csv', uname2id)

