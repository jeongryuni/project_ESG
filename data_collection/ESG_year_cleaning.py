import pandas as pd

ESG_2020 = pd.read_csv('data/esg_data/2020-ESG-cleaned.csv')
ESG_2021 = pd.read_csv('data/esg_data/2021-ESG-cleaned.csv')
ESG_2022 = pd.read_csv('data/esg_data/2022-ESG-cleaned.csv')
ESG_2023 = pd.read_csv('data/esg_data/2023-ESG-cleaned.csv')
ESG_2024 = pd.read_csv('data/esg_data/2024-ESG-cleaned.csv')

# 각 데이터에 연도 열 추가
ESG_2020['연도'] = 2020
ESG_2021['연도'] = 2021
ESG_2022['연도'] = 2022
ESG_2023['연도'] = 2023
ESG_2024['연도'] = 2024

# 데이터 합치기
df = pd.concat([ESG_2020, ESG_2021, ESG_2022, ESG_2023, ESG_2024], ignore_index=True)
df = df.sort_values(by=['회사명','연도'])


result = df.to_csv('data/esg_data/ESG_year_data.csv', index=False)
print(pd.read_csv('data/esg_data/ESG_year_data.csv'))