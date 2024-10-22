# 1. 주가 데이터 정제
# ESG 데이터와 주가 데이터의 동일한 회사만 교집합으로 남아있게 병합

import pandas as pd

# ESG 데이터 불러오기
esg_file = 'cleaned_data/esg_data/ESG_year_data.csv'
esg_df = pd.read_csv(esg_file, encoding='utf-8')

# 금융 데이터 불러오기
finance_file = '../data_collection/data/finance_data/2023_12_finance_data.csv'
finance_df = pd.read_csv(finance_file, encoding='EUC-KR')

# 두 데이터 프레임의 공통 열인 '회사명'과 '종목명'을 기준으로 교집합 병합
merged_df = pd.merge(finance_df, esg_df, left_on='종목명', right_on='회사명', how='inner')

# 불필요한 열 제거
merged_df = merged_df.drop(['회사명', '종합등급', '환경', '사회', '지배구조', '종목코드', '연도'], axis=1)

# 중복 제거
merged_df = merged_df.drop_duplicates()

# 결과 확인
print(merged_df.head())

# 병합된 데이터를 CSV 파일로 저장
merged_df.to_csv('cleaned_data/finance_data/2023_12_finance_cleaned_data.csv', index=False, encoding='utf-8')
