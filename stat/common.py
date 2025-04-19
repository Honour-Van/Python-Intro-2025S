import csv
import re
import pandas as pd

def extract_10_digit_number(input_string):
    # 使用正则表达式匹配10位数字
    match = re.search(r'(?<!\d)\d{10}(?!\d)', input_string)
    if match:
        return match.group(0)  # 返回匹配的10位数字
    return None  # 如果没有匹配到，返回None

MAPPING_FILE = './data/username_mapping.csv'
def get_uname2id_mapping(file):
    with open(file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        uname2id = {}
        next(csv_reader)  # 跳过表头
        for row in csv_reader:
            uname = row[1]
            id = extract_10_digit_number(uname)
            uname2id[uname] = id
        with open(MAPPING_FILE, 'w', encoding='utf-8', newline='') as mapping_file:
            csv_writer = csv.writer(mapping_file)
            csv_writer.writerow(['uname', 'id'])
            for uname, id in uname2id.items():
                csv_writer.writerow([uname, id])
    return uname2id

def read_uname2id_mapping_from_csv():
    uname2id = {}
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # 跳过表头
        for row in csv_reader:
            uname = row[0]
            id = row[1]
            uname2id[uname] = id
    return uname2id
    
def get_registration_list():
    df = pd.read_csv('./data/registration_list.csv')
    return df

if __name__ == '__main__':
    # get_uname2id_mapping('./output/2.csv')
    print(get_registration_list())
