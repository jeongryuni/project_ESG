# 주가 데이터 정제
# 종목명 행의 개수가 20개가 아니면 제거(모든 분기의 데이터의 수 = 20)
import pandas as pd

# 데이터 불러오기
finance_df = pd.read_csv('cleaned_data/finance_data/finance_year_quarter_data.csv')

# 종목명 별로 빈도 수 확인
counts = finance_df['종목명'].value_counts()

# 빈도가 16인 종목명만 필터링
filtered_df = finance_df[finance_df['종목명'].isin(counts[counts == 20].index)]

# 필터링 결과 확인
# print(filtered_df['종목명'].value_counts())
filtered_df.to_csv('cleaned_data/finance_data/finance_year_quarter_filtered_data.csv', index=False)