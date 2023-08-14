import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
fe = fm.FontEntry(
    fname=r'C:/Windows/Fonts/나눔고딕/NanumGothic.ttf', # ttf 파일이 저장되어 있는 경로
    name='NanumGothic')                        # 이 폰트의 원하는 이름 설정
fm.fontManager.ttflist.insert(0, fe)              # Matplotlib에 폰트 추가
plt.rcParams.update({'font.size': 18, 'font.family': 'NanumGothic'}) # 폰트 설정


# 데이터 불러오기
railway_stations_df = pd.read_csv('C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/stations_within_railway_buffer.csv', encoding='EUC-KR')
local_products = pd.read_csv('C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/북한 특산물 위치.csv', encoding='EUC-KR')

from math import radians, sin, cos, sqrt, atan2

#지구상의 두 점의 최단거리 구하는 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구반지름

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    # haversine 공식 적용
    a = (sin(dlat / 2) ** 2 +
         cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

# 각 특산물 위치에서 20km 이내에 특산물 공급 거점역이 있는지 확인
local_products['특산물 위치 20km 이내의 철도역'] = False
for idx, product in local_products.iterrows():
    for i, station in railway_stations_df.iterrows():
        distance = haversine(product['Y좌표'], product['X좌표'], station['Y좌표'], station['X좌표'])
        if distance <= 20:
            local_products.at[idx, '특산물 위치 20km 이내의 철도역'] = True
            break

# 특산물 공급 거점역이 20km이내에 있는 특산물의 비율 계산
percentage_with_selected_station = (local_products['특산물 위치 20km 이내의 철도역'].sum() / len(local_products)) * 100

percentage_with_selected_station

# 데이터 구성
labels_selected = ['20km이내에 철도역이 있음', '20km이내에 철도역이 없음']
sizes_selected = [local_products['특산물 위치 20km 이내의 철도역'].sum(),
                  len(local_products) - local_products['특산물 위치 20km 이내의 철도역'].sum()]
colors_selected = ['#87AAFF', '#FFA8C1']
explode_selected = (0.1, 0)  # explode 1st slice

# 원형차트로 표시
plt.figure(figsize=(10, 6))
plt.pie(sizes_selected, explode=explode_selected, labels=labels_selected, colors=colors_selected,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.title('북한 특산물 주변 철도역 분석(20km)')
plt.show()