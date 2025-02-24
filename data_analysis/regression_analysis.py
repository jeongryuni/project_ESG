# 회귀분석
# ESG 등급에 따른 주가 변동성 분석
# 독립변수 : 2020~2024년까지의 ESG 평균 등급
# 종속변수 : 2020~2024년까지의 종목별 주가 변동성

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 주가 변동성 데이터 불러오기
finance_df = pd.read_csv('종목별_변동성.csv')

# ESG 등급 데이터 불러오기
esg_df = pd.read_csv('../data_cleaning/cleaned_data/esg_data/ESG_year_data.csv')

# 주가 변동성 데이터 이상치 제거
Q1 = finance_df['변동성'].quantile(0.25)
Q3 = finance_df['변동성'].quantile(0.75)
IQR = Q3-Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = (finance_df['변동성'] < lower_bound) | (finance_df['변동성'] > upper_bound)
finance_df = finance_df[~outliers]

# ESG 등급을 숫자로 변환하기 위한 매핑
grade_mapping = {
    'A+': 5,
    'A': 4,
    'B+': 3,
    'B': 2,
    'C': 1,
    'D': 0
}

# ESG 등급 데이터에 숫자 매핑 적용
esg_df['종합등급_수치'] = esg_df['종합등급'].map(grade_mapping)

# 각 종목별로 2020~2023년까지의 평균 ESG 종합등급 계산
esg_avg_df = esg_df.groupby('회사명').agg({
    '종합등급_수치': 'mean'
}).reset_index()

# 주가 변동성 데이터와 ESG 평균 등급 데이터 병합
merged_df = pd.merge(finance_df, esg_avg_df, left_on='종목명', right_on='회사명')

merged_df.to_csv('esg_average.csv', index=False)

# 필요 없는 열 제거
merged_df = merged_df[['종목명', '변동성', '종합등급_수치']]

# 독립 변수(X)와 종속 변수(y) 설정
X = merged_df[['종합등급_수치']]
y = merged_df['변동성']

# 상수항 추가
X = sm.add_constant(X)

# 회귀 분석 모델 생성 및 적합
model = sm.OLS(y, X)
results = model.fit()

# 회귀 분석 결과 출력
print(results.summary())

# 회귀 직선 그리기
plt.figure(figsize=(10, 6))

# 산점도 그리기
plt.scatter(merged_df['종합등급_수치'], merged_df['변동성'], color='blue', label='Data points')

# 회귀 직선 계산
predictions = results.predict(X)
plt.plot(merged_df['종합등급_수치'], predictions, color='red', label='Regression line')

# 그래프 제목 및 레이블 설정
plt.title('ESG 등급에 따른 주가 변동성 분석')
plt.xlabel('ESG 평균 등급 (2020~2024)')
plt.ylabel('주가 변동성 (2020~2024)')
plt.legend()
plt.grid()

# 그래프 출력
plt.show()
