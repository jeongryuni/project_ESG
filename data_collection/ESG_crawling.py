from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# 옵션 객체 생성
options = Options()
options.add_experimental_option("detach", True)

# 크롬 드라이버 생성
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# 사이트 접속하기
driver.get('https://esg.krx.co.kr/contents/02/02020000/ESG02020000.jsp')

# 연도 선택 창 접근 (select 태그 접근)
select_element = driver.find_element(By.ID, 'sch_yyc4ca4238a0b923820dcc509a6f75849b')

# Select 객체 생성 후 옵션 선택
select = Select(select_element)
select.select_by_value('2024')

# 선택된 연도 확인
selected_year = select.first_selected_option.text
print(f"선택된 연도: {selected_year}")  # 로그 출력

# 조회 클릭
wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.ID, 'btnidc4ca4238a0b923820dcc509a6f75849b')))
button.click()

# 데이터 수집을 위한 리스트 초기화
all_data_list = []

# 페이지 수집 루프
while True:
    # 테이블 로드 대기
    wait.until(EC.presence_of_element_located((By.ID, "gridtableeccbc87e4b5ce2fe28308fd9f2a7baf3")))

    # 테이블 접근
    table = driver.find_element(By.ID, "gridtableeccbc87e4b5ce2fe28308fd9f2a7baf3")

    # 테이블의 HTML 소스를 가져오기
    table_html = table.get_attribute('outerHTML')

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(table_html, 'html.parser')

    # <tbody>에서 등급 데이터 추출
    rows = soup.find('tbody').find_all('tr')

    # 각 행을 반복하며 데이터 추출
    for row in rows:
        cells = row.find_all('td')
        data = []

        # 회사명을 <a> 태그에서 텍스트만 가져오기
        company_name_tag = cells[0].find('a')  # <a> 태그 찾기
        if company_name_tag:
            company_name = company_name_tag.text.strip()  # <a> 태그의 텍스트만 가져옴
        else:
            company_name = cells[0].text.strip()  # <a> 태그가 없으면 일반 텍스트를 가져옴
        data.append(company_name)  # 회사명 추가

        # 나머지 셀들에서 <span> 태그의 텍스트를 가져오기
        for cell in cells[1:]:  # 첫 번째 셀은 이미 추가했으므로 나머지 셀에서 반복
            span = cell.find('span')
            if span:
                data.append(span.text.strip())  # <span>의 텍스트를 가져오고 공백 제거
            else:
                data.append(cell.text.strip())  # <span>이 없는 경우 일반 텍스트를 가져옴

        if data:  # 데이터가 있는 경우에만 추가
            all_data_list.append(data)

    # 다음 페이지 버튼 클릭
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next")
        if "disabled" in next_button.get_attribute("class"):
            break  # 더 이상 다음 페이지가 없으면 종료
        else:
            next_button.click()  # 다음 페이지로 이동
            time.sleep(2)  # 다음 페이지 로드 대기
    except Exception as e:
        print("Error navigating to next page:", e)
        break

# DataFrame으로 변환
# 컬럼 이름을 자동으로 설정
if all_data_list:
    # 각 행의 길이를 확인하여 동적으로 컬럼 이름을 설정
    num_columns = len(all_data_list[0])  # 첫 번째 행의 길이로 열 수 설정
    columns = [f'컬럼_{i+1}' for i in range(num_columns)]  # 동적으로 컬럼 이름 생성
    df = pd.DataFrame(all_data_list, columns=columns)
else:
    df = pd.DataFrame(columns=['회사명', '등급', '연도'])  # 비어있는 경우 기본 열 이름 설정

# DataFrame 출력
print(df)

# 드라이버 종료
driver.quit()

# CSV로 저장
df.to_csv('2024-ESG.csv', index=False)
