import pandas as pd

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

station_product_counts_150km = []
for i, station_row in railway_stations_df.iterrows():
    count = 0
    for j, product_row in local_products.iterrows():
        distance = haversine(station_row['X좌표'], station_row['Y좌표'], 
                             product_row['X좌표'], product_row['Y좌표'])
        if distance <= 150:
            count += 1
    station_product_counts_150km.append(count)

railway_stations_df['특산물 개수'] = station_product_counts_150km
sorted_stations = railway_stations_df.sort_values(by='특산물 개수', ascending=False).reset_index()

selected_stations = []
for i, row in sorted_stations.iterrows():
    # 75km 이내에 다른 철도역이 없는 경우에만 추가
    if not any(haversine(row['X좌표'], row['Y좌표'], stat['X좌표'], stat['Y좌표']) < 75 for stat in selected_stations):
        selected_stations.append(row)
        if len(selected_stations) == 15:
            break

selected_stations_df = pd.DataFrame(selected_stations)
print(selected_stations_df[['지명', '특산물 개수']])

# CSV파일로 저장
file_path = "C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/selected_stations.csv"
selected_stations_df.to_csv(file_path, index=False, encoding='EUC-KR')

file_path