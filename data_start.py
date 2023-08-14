# 이 파일은 공공데이터 포털의 철도역 및 지하철역 위치 정보에서 철도역에 해당하는 정보만 추출하여 CSV 파일로 저장하는 코드입니다.

import geopandas as gpd

# GeoJSON 파일을 GeoDataFrame에 로드
north_korea_railway = gpd.read_file("C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/북한지도_철도망_EPSG4326_EUC_KR_GeoJSON_NM.geojson")

import matplotlib.pyplot as plt

# plot 설정
fig, ax = plt.subplots(figsize=(12, 12))

# 철도망 작성
north_korea_railway.plot(ax=ax, color='blue', linewidth=1.5)

# 철도 및 지하철역 위치 정보 파일 읽기
import pandas as pd

# EUC-KR 인코딩으로 CSV 파일 읽기
railway_stations_path = "C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/북한지도_철도_지하철역_EPSG4326_EUC_KR.csv"
railway_stations_df = pd.read_csv(railway_stations_path, encoding='EUC-KR')

# 자도에 철도역 표시하기
ax.scatter(railway_stations_df["Y좌표"], railway_stations_df["X좌표"], color='red', s=15, label="railroad station")
ax.legend()
ax.set_title("Railroad network and station locations in North Korea")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(True)

plt.show()

# stations DataFrame을 GeoDataFrame으로 변환
stations_gdf = gpd.GeoDataFrame(railway_stations_df, geometry=gpd.points_from_xy(railway_stations_df['Y좌표'], railway_stations_df['X좌표']))

# 철도망 데이터에서 버퍼 생성
buffered_railways = north_korea_railway.buffer(0.01)

# 철도망에서 1km 이내에 있는 철도역 추출
stations_within_buffer = stations_gdf[stations_gdf.within(buffered_railways.unary_union)]

# 불필요한 열 삭제
stations_within_buffer = stations_within_buffer.drop(columns=["geometry"])

# 데이터프레임 출력
print(stations_within_buffer)

# CSV파일로 저장
file_path = "C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/stations_within_railway_buffer.csv"
stations_within_buffer.to_csv(file_path, index=False, encoding='EUC-KR')

file_path
