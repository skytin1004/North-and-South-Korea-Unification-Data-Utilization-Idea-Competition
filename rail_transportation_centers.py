import pandas as pd
import geopandas as gpd

# 데이터 불러오기
railway_stations_df = pd.read_csv('C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/stations_within_railway_buffer.csv', encoding='EUC-KR')
north_korea_railway = gpd.read_file('C:/Users/sms79/Desktop/공모전/통일 빅데이터 공모전/map_bridge_station_railroad/북한지도_철도망_EPSG4326_EUC_KR_GeoJSON_NM.geojson', encoding='EUC-KR')

railway_stations_df.head(), north_korea_railway.head()

# 철도 라인을 약간의 버퍼로 확장하여 철도역이 해당 라인 위에 있는지 확인
buffered_railway = north_korea_railway.buffer(0.01)  # 약 1km 버퍼 적용 (실제 값은 좌표 체계와 지역에 따라 달라질 수 있음)

# stations DataFrame을 GeoDataFrame으로 변환
stations_gdf = gpd.GeoDataFrame(railway_stations_df, geometry=gpd.points_from_xy(railway_stations_df['Y좌표'], railway_stations_df['X좌표']))

# 철도역이 버퍼 내에 위치하는지 확인
within_buffer = stations_gdf.geometry.apply(lambda point: buffered_railway.contains(point).any())

# 버퍼 내에 위치하는 철도역만 선택
stations_within_buffer = stations_gdf[within_buffer]

stations_within_buffer.head()

# 각 철도역이 어떤 철도 라인에 속하는지 확인
def get_railway_name(point):
    return north_korea_railway[buffered_railway.contains(point)]['NM'].values[0]

stations_within_buffer['철도라인'] = stations_within_buffer['geometry'].apply(get_railway_name)
stations_within_buffer.head()

import networkx as nx

# 철도역 간의 연결 관계를 나타내는 그래프 생성
G = nx.Graph()

# 철도역을 그래프의 노드로 추가
for index, row in stations_within_buffer.iterrows():
    G.add_node(row['지명'], position=(row['Y좌표'], row['X좌표']))

# 철도 라인별로 철도역 간의 연결 관계를 그래프의 엣지로 추가
for line_name in stations_within_buffer['철도라인'].unique():
    stations_on_line = stations_within_buffer[stations_within_buffer['철도라인'] == line_name]
    sorted_stations = stations_on_line.sort_values(by='Y좌표')  # 경도 기준으로 정렬
    for i in range(len(sorted_stations) - 1):
        G.add_edge(sorted_stations.iloc[i]['지명'], sorted_stations.iloc[i + 1]['지명'])

# 각 철도역의 연결 중심성 계산
centrality = nx.degree_centrality(G)
sorted_centrality = dict(sorted(centrality.items(), key=lambda x: x[1], reverse=True))

# 연결 중심성 목록
sorted_centrality

# 상위 5개의 철도역의 연결 중심성 추출
top_5_centrality = dict(list(sorted_centrality.items())[:5])
print(top_5_centrality)

