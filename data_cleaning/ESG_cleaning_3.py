# 3. ESG 데이터 정제
# ESG 종합등급 결측치 제거

import pandas as pd
df = pd.read_csv('C:\project_ESG\workspace\data_cleaning\cleaned_data\esg_data\ESG_year_data.csv')

# 종합등급 컬럼 결측치 제거
df['종합등급'] = df['종합등급'].replace('-', 'NAN')
# print(df['종합등급'].unique())

# 환경 컬럼 결측치 제거
# print(df['환경'].unique())
df['환경'] = df['환경'].replace('-', 'NAN')

# 환경 컬럼 결측치 제거
df['환경'] = df['환경'].replace('-', 'NAN')
print(df['환경'].unique())

# 사회 컬럼 결측치 제거
df['사회'] = df['사회'].replace('-', 'NAN')
print(df['사회'].unique())

# 지배구조 컬럼 결측치 제거
df['지배구조'] = df['지배구조'].replace('-', 'NAN')
print(df['지배구조'].unique())

# 연도 컬럼 결측치 제거
df['연도'] = df['연도'].replace('-', 'NAN')
print(df['연도'].unique())

df.to_csv('cleaned_data/esg_data/ESG_missing_value_drop.csv')