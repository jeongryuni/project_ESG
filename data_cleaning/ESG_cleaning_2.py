# ESG 데이터 정제
# 1) 데이터 병합 후 연도 컬럼 추가
# 2) 결측치 제거
# 3) 2020년부터 2024년까지 모든 등급을 갖고 있는 회사만 필터링

import pandas as pd
import numpy as np

# 데이터 로드 (2020년부터 2024년까지)
ESG_2020 = pd.read_csv('cleaned_data/esg_data/2020-ESG-cleaned.csv')
ESG_2021 = pd.read_csv('cleaned_data/esg_data/2021-ESG-cleaned.csv')
ESG_2022 = pd.read_csv('cleaned_data/esg_data/2022-ESG-cleaned.csv')
ESG_2023 = pd.read_csv('cleaned_data/esg_data/2023-ESG-cleaned.csv')
ESG_2024 = pd.read_csv('cleaned_data/esg_data/2024-ESG-cleaned.csv')

# 각 데이터에 연도 열 추가
ESG_2020['연도'] = 2020
ESG_2021['연도'] = 2021
ESG_2022['연도'] = 2022
ESG_2023['연도'] = 2023
ESG_2024['연도'] = 2024

# 데이터 병합 (2020년부터 2024년까지 사용)
df = pd.concat([ESG_2020, ESG_2021, ESG_2022, ESG_2023, ESG_2024], ignore_index=True)

# '-' 값을 NaN으로 변환
df.replace('-', np.nan, inplace=True)

# '종합등급' 값이 NaN인 행 삭제
df = df.dropna(subset=['종합등급'])

# 중복된 행 제거
df = df.drop_duplicates()

# 회사명/연도 정렬
df = df.sort_values(by=['회사명','연도'])

# 각 회사별로 연도 수 세기
company_year_counts = df.groupby('회사명')['연도'].nunique()

# 2020년부터 2024년까지 모든 등급을 갖고 있는 회사만 필터링
valid_companies = company_year_counts[company_year_counts == 5].index

# 해당 회사들의 데이터만 필터링
df_filtered = df[df['회사명'].isin(valid_companies)]

# 저장
df_filtered.to_csv('cleaned_data/esg_data/ESG_year_data.csv', index=False)


