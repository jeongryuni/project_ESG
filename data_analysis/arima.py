# 시간에 따른 ESG 등급 상위 그룹과 하위 그룹의 주가 변동성 비교

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 주가 변동성 데이터 불러오기
finance_df = pd.read_csv('종목별_변동성.csv')

# ESG 등급 데이터 불러오기
esg_df = pd.read_csv('../data_cleaning/cleaned_data/esg_data/ESG_year_data.csv')

# 주가 변동성 데이터 이상치 제거
Q1 = finance_df['변동성'].quantile(0.25)
Q3 = finance_df['변동성'].quantile(0.75)
IQR = Q3 - Q1
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

# 필요 없는 열 제거
merged_df = merged_df[['종목명', '변동성', '종합등급_수치']]

# 등급 정렬
esg_avg_sort = merged_df.sort_values(by='종합등급_수치', ascending=False)

# 상위 30%, 하위 30% 나누기
top30 = esg_avg_sort[:int(len(esg_avg_sort) * 0.3)]  # 상위 30%
bottom30 = esg_avg_sort[int(len(esg_avg_sort) * 0.7):]  # 하위 30%

# 상위 30%와 하위 30%의 종목 리스트
top30_list = top30['종목명']
bottom30_list = bottom30['종목명']

# 주가 데이터 불러오기
df = pd.read_csv("분기별_주가_데이터.csv")

# 상위 30% 그룹의 주가 데이터
top30_data = df[df['종목명'].isin(top30_list)]

# 하위 30% 그룹의 주가 데이터
bottom30_data = df[df['종목명'].isin(bottom30_list)]

# 상위 30% 그룹과 하위 30% 그룹의 변동성 계산
top30_volatility = top30_data.groupby("연도-분기")["수익률"].std().reset_index()
bottom30_volatility = bottom30_data.groupby("연도-분기")["수익률"].std().reset_index()

# 컬럼명 변경
top30_volatility.columns = ["연도-분기", "변동성"]
bottom30_volatility.columns = ["연도-분기", "변동성"]

# 시계열 그래프 그리기
plt.figure(figsize=(12, 6))

# 상위 30% 변동성 그래프
plt.plot(top30_volatility['연도-분기'], top30_volatility['변동성'], label='상위 30% ESG 등급', color='blue')

# 하위 30% 변동성 그래프
plt.plot(bottom30_volatility['연도-분기'], bottom30_volatility['변동성'], label='하위 30% ESG 등급', color='red')

# 그래프 작성
plt.title('상위 30% vs 하위 30% ESG 등급의 주가 변동성 비교', fontsize=16)
plt.xlabel('연도-분기', fontsize=12)
plt.ylabel('변동성 (수익률 표준편차)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 그래프 출력
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df = pd.read_csv("분기별_주가_데이터.csv")

# 상위 30%와 하위 30% 변동성 계산 (기존 코드 참조)
top30_volatility = top30_data.groupby("연도-분기")["수익률"].std().reset_index()
bottom30_volatility = bottom30_data.groupby("연도-분기")["수익률"].std().reset_index()

# 컬럼명 변경
top30_volatility.columns = ["연도-분기", "변동성"]
bottom30_volatility.columns = ["연도-분기", "변동성"]


# ARIMA 모델을 이용한 예측 함수
def predict_volatility(data, periods=12):  # 3년 = 12분기
    data['연도-분기'] = pd.to_datetime(data['연도-분기'], format='%Y-%m')
    model = ARIMA(data['변동성'], order=(1, 0, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=periods)
    return forecast



# 상위 30% 변동성 예측
top30_forecast = predict_volatility(top30_volatility, periods=12)

# 하위 30% 변동성 예측
bottom30_forecast = predict_volatility(bottom30_volatility, periods=12)



# 예측 결과 시각화
plt.figure(figsize=(14, 7))

# 상위 30% 변동성 그래프
plt.plot(top30_volatility['연도-분기'], top30_volatility['변동성'], label='상위 30% ESG 등급', color='blue')

# 하위 30% 변동성 그래프
plt.plot(bottom30_volatility['연도-분기'], bottom30_volatility['변동성'], label='하위 30% ESG 등급', color='red')

# 예측된 값 추가 (상위 30%)
forecast_index = pd.date_range(top30_volatility['연도-분기'].max(), periods=12, freq='QE')
plt.plot(forecast_index, top30_forecast, label='상위 30% 변동성 예측', linestyle='--', color='blue')

# 예측된 값 추가 (하위 30%)
forecast_index_bottom = pd.date_range(bottom30_volatility['연도-분기'].max(), periods=12, freq='QE')
plt.plot(forecast_index_bottom, bottom30_forecast, label='하위 30% 변동성 예측', linestyle='--', color='red')

# 그래프 작성
plt.title('상위 30% vs 하위 30% ESG 등급의 주가 변동성 예측', fontsize=16)
plt.xlabel('연도-분기', fontsize=12)
plt.ylabel('변동성 (수익률 표준편차)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 그래프 출력
plt.tight_layout()
plt.show()

# NaN 값 확인 및 제거
top30_volatility['변동성'] = pd.to_numeric(top30_volatility['변동성'], errors='coerce')
bottom30_volatility['변동성'] = pd.to_numeric(bottom30_volatility['변동성'], errors='coerce')

top30_volatility = top30_volatility.dropna()
bottom30_volatility = bottom30_volatility.dropna()

# 데이터 개수 확인
print("Top 30 개수:", len(top30_volatility))
print("Bottom 30 개수:", len(bottom30_volatility))

# 분산 확인
print("Top 30 변동성 분산:", top30_volatility['변동성'].var())
print("Bottom 30 변동성 분산:", bottom30_volatility['변동성'].var())

# t-test 실행 (데이터가 충분할 때만)
if len(top30_volatility) > 1 and len(bottom30_volatility) > 1:
    from scipy.stats import ttest_ind
    st, pv = ttest_ind(top30_volatility['변동성'], bottom30_volatility['변동성'])
    print("t-statistic:", st, "p-value:", pv)
else:
    print("데이터가 부족하여 t-test를 수행할 수 없습니다.")