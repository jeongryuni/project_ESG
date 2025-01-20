import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 데이터 불러오기
df = pd.read_csv('분기별_주가_데이터.csv')

# 시계열 그래프 시각화
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='연도-분기', y='수익률', hue='종목명', marker='o')


# 그래프 설정
plt.xticks(rotation=45)  # X축 레이블 회전
plt.title("연도별 & 분기별 주가 수익률 변화")
plt.xlabel("연도-분기")
plt.ylabel("수익률 (%)")
plt.legend(title="회사명")  # 범례 추가
plt.grid(True)

# 그래프 출력
plt.show()