# 철도 및 지하철역 위치 정보 파일 읽기
import pandas as pd

# 데이터 불러오기
selected_stations_path = "C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/selected_stations.csv"
selected_stations_df = pd.read_csv(selected_stations_path, encoding='EUC-KR')

# 데이터의 처음 5행 출력
selected_stations_df.head()

import matplotlib.pyplot as plt

# 철도역 위치 표시
plt.scatter( selected_stations_df['Y좌표'],selected_stations_df['X좌표'], color='red', s=10)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Selected Stations in North Korea')
plt.show()

# 데이터 불러오기
special_production_locations_path = "C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/북한 특산물 위치.csv"
special_production_locations_df = pd.read_csv(special_production_locations_path, encoding='EUC-KR')

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

# 특산물의 위치에서 가장 가까운 역 조사
def find_nearest_station(product_lat, product_lon, stations_df):
    min_distance = float('inf')
    nearest_station = None

    for idx, row in stations_df.iterrows():
        distance = haversine(product_lat, product_lon, row['X좌표'], row['Y좌표'])
        if distance < min_distance:
            min_distance = distance
            nearest_station = row['지명']

    return nearest_station


# 각 특산물 위치에서 가장 가까운 역 찾기
special_production_locations_df['가장 가까운 역'] = special_production_locations_df.apply(lambda row: find_nearest_station(row['X좌표'], row['Y좌표'], selected_stations_df), axis=1)
special_production_locations_df.head()

#  각각의 철도역이 참조된 횟수를 계산.
station_reference_counts = special_production_locations_df['가장 가까운 역'].value_counts()
station_reference_df = station_reference_counts.reset_index()
station_reference_df.columns = ['철도역', '참조 횟수']
station_reference_df = station_reference_df.sort_values(by="참조 횟수", ascending=False)
station_reference_df

# 각 철도역의 참조 횟수 데이터를 원래의 철도역 데이터프레임에 병합
stations_with_references = pd.merge(selected_stations_df, station_reference_df, left_on='지명', right_on='철도역', how='left').fillna(0)
stations_with_references = stations_with_references.drop(columns=['철도역'])
print(stations_with_references)
"""
import folium
# 북한 위치로 지도 생성
map_project = folium.Map(location=[40.0, 127.0], zoom_start=7)

# 지도에 철도역 참조 횟수를 반영해 원형으로 표시
for idx, row in stations_with_references.iterrows():
    radius = row['참조 횟수'] * 2
    folium.CircleMarker(
        location=(row['X좌표'], row['Y좌표']),
        radius=radius,
        color="#87AFFF",
        fill=True,
        fill_color="#87AFFF",
        fill_opacity=0.60,
        weight=0.5,
    ).add_to(map_project)

    # 글자 크기 설정
    font_size = min(int(radius * 1.5), 16)

    # 원 안에 들어가는 텍스트를 표시
    folium.Marker(
        location=(row['X좌표'], row['Y좌표']),
        icon=folium.DivIcon(
            html=f'<div style="color: white; font-size: {font_size}px; font-weight: bold; text-align: center; line-height: {font_size}px;">{int(row["참조 횟수"])}</div>'),
    ).add_to(map_project)

# HTML파일로 저장
map_project_path = "C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/map_project.html"
map_project.save(map_project_path)

map_project_path
"""