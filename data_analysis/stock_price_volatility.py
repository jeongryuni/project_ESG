import pandas as pd

# 1. 데이터 불러오기
df = pd.read_csv('../data_cleaning/cleaned_data/finance_data/finance_year_quarter_data.csv')

# 2. 변동률 계산 함수 작성
def calculate_change_rates(df):
    change_rates = []

    # 종목명과 연도, 분기로 그룹화
    grouped = df.groupby(['종목명', '연도'])

    for (stock, year), group in grouped:
        # 각 분기 데이터 가져오기
        q1_close = group[group['분기'] == 'Q1']['종가']
        q2_close = group[group['분기'] == 'Q2']['종가']
        q3_close = group[group['분기'] == 'Q3']['종가']
        q4_close = group[group['분기'] == 'Q4']['종가']

        # 변동률 계산
        if not q1_close.empty and not q2_close.empty:
            q1_to_q2 = ((q2_close.values[0] - q1_close.values[0]) / q1_close.values[0]) * 100
            change_rates.append({'종목명': stock, '연도': year, '분기': 'Q2', '변동률 (%)': q1_to_q2})

        if not q2_close.empty and not q3_close.empty:
            q2_to_q3 = ((q3_close.values[0] - q2_close.values[0]) / q2_close.values[0]) * 100
            change_rates.append({'종목명': stock, '연도': year, '분기': 'Q3', '변동률 (%)': q2_to_q3})

        if not q3_close.empty and not q4_close.empty:
            q3_to_q4 = ((q4_close.values[0] - q3_close.values[0]) / q3_close.values[0]) * 100
            change_rates.append({'종목명': stock, '연도': year, '분기': 'Q4', '변동률 (%)': q3_to_q4})

    # 새로운 연도로 넘어갈 때 Q1 변동률 계산
    for (stock, year), group in grouped:
        if year > df['연도'].min():  # 이전 연도가 존재할 때
            previous_year = year - 1
            previous_group = df[(df['종목명'] == stock) & (df['연도'] == previous_year) & (df['분기'] == 'Q4')]

            if not previous_group.empty and not group[group['분기'] == 'Q1'].empty:
                previous_q4_close = previous_group['종가'].values[0]
                current_q1_close = group[group['분기'] == 'Q1']['종가'].values[0]

                # Q1 변동률 계산
                q4_to_q1 = ((current_q1_close - previous_q4_close) / previous_q4_close) * 100
                change_rates.append({'종목명': stock, '연도': year, '분기': 'Q1', '변동률 (%)': q4_to_q1})

    return pd.DataFrame(change_rates)

# 3. 새로운 데이터프레임 생성
change_rate_df = calculate_change_rates(df)

# 원본 데이터프레임에 변동률 컬럼 추가
df = df.merge(change_rate_df, on=['종목명', '연도', '분기'], how='left')

# 결과 확인
print(df.head())

# 변동률 데이터 저장
df.to_csv('finance_with_change_rates.csv', index=False)
