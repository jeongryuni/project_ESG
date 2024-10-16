# 1. ESG 데이터 정제
# ESG 데이터에서 필요한 컬럼만 추출

import pandas as pd

# CSV 파일 읽어오기
result = pd.read_csv('../data_collection/data/esg_data/2024-ESG.csv')

# 컬럼명 변경
result = result.rename(columns={
    '컬럼_1': '회사명',
    '컬럼_2': '종합등급',
    '컬럼_3': '환경',
    '컬럼_4': '사회',
    '컬럼_5': '지배구조',
})

# 필요한 컬럼만 남기기
result = result[['회사명', '종합등급', '환경', '사회', '지배구조']]

print(result)

# 변경된 DataFrame을 CSV 파일로 저장
result.to_csv('cleaned_data/esg_data/2024-ESG-cleaned.csv', index=False)