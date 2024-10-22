# 2. 주가 데이터 정제
# 모든 년도와 분기를 표기해 한 데이터프레임으로 저장

import pandas as pd
import glob
import os

# 모든 CSV 파일을 가져오기
file_list = glob.glob('cleaned_data/finance_data/*.csv')

# 데이터프레임 리스트
df_list = []

# 분기 변환 매핑 (03 -> Q1, 06 -> Q2, 09 -> Q3, 12 -> Q4)
quarter_mapping = {
    '03': 'Q1',
    '06': 'Q2',
    '09': 'Q3',
    '12': 'Q4'
}

for file in file_list:
    # 파일명에서 연도와 분기 추출 (예: '2020_03_finance_cleaned_data.csv')
    file_name = os.path.basename(file)  # 파일 이름만 가져오기
    year, quarter = file_name.split('_')[0], file_name.split('_')[1]

    # CSV 파일 읽기
    df = pd.read_csv(file)

    # 연도와 분기 컬럼 추가
    df['연도'] = year
    df['분기'] = quarter_mapping.get(quarter, quarter)  # 분기를 매핑하여 변환

    # 리스트에 데이터프레임 추가
    df_list.append(df)

# 모든 데이터프레임을 하나로 병합
merged_df = pd.concat(df_list, ignore_index=True)

# 데이터 정렬
merged_df = merged_df.sort_values(by=['종목명','연도','분기'])

# 결과 확인
print(merged_df.head())

# 병합된 데이터 저장
merged_df.to_csv('cleaned_data/finance_data/finance_year_quarter_data.csv', index=False)