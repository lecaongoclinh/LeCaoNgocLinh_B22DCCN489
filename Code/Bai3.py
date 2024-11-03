import warnings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import os

warnings.filterwarnings('ignore')

# Đọc vào file result.csv
df = pd.read_csv('result.csv', header=[0, 1, 2])
df.columns = [tuple('' if 'Unnamed:' in x else x for x in col) for col in df.columns]

# Kiểm tra thông tin cơ bản của DataFrame
print("DataFrame Info:")
df.info()

print("\nMissing Values per Column:")
print(df.isna().sum())

print("\nTeam Value Counts:")
print(df[('', '', 'Team')].value_counts())
# Đường dẫn đến thư mục
output_dir = 'hinh_ve'

# Tạo thư mục nếu nó không tồn tại
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#Tắt chế độ tương tác
plt.ioff()
# K-means Clustering
sse = []
silhouette_scores = []
# Lọc dữ liệu dạng số để phân cụm
X = df.select_dtypes(include=[float, int]).dropna(axis=1, how='any')  # Xóa các cột có giá trị null
# Tính SSE và điểm silhouette cho mỗi giá trị k
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    sse.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X, kmeans.labels_))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(range(2, 10), sse, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.title("Elbow Method")

plt.subplot(1, 2, 2)
plt.plot(range(2, 10), silhouette_scores, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Score")
plt.savefig(os.path.join(output_dir, f'Kmeans.png'))
plt.close() 
print("Hinh anh da duoc luu vào thu muc hinh_ve")

# PCA và vẽ phân cụm K-means với PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
kmeans = KMeans(n_clusters=4, random_state=42)  # Sử dụng n_clusters=4 theo quan sát từ Elbow/Silhouette
clusters = kmeans.fit_predict(X_pca)

plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=clusters, palette="viridis", legend='full')
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("K-means Clustering with PCA")
plt.savefig(os.path.join(output_dir, f'Kmeans_PCA.png'))
plt.close() 
print("Hinh anh da duoc luu vào thu muc hinh_ve")

# Biểu đồ Radar so sánh cầu thủ

# Chọn hai cầu thủ có cùng vị trí để so sánh
p1 = "Elijah Adebayo"  # Tên cầu thủ
p2 = "Simon Adingra"  # Tên cầu thủ

# Danh sách các chỉ số muốn so sánh
attributes = [('','','Age'),('', '', 'Matches Played'),('', 'Performance', 'non-Penalty Goals'),('', 'Expected', 'xG'),('Shooting', 'Standard', 'SoT')]

# Kiểm tra xem cầu thủ và các thuộc tính có trong dữ liệu hay không
if p1 not in df[('', '', 'Name')].values or p2 not in df[('', '', 'Name')].values:
    print(f"One or both players not found in the dataset.")
else:
    # Lấy dữ liệu của hai cầu thủ
    data1 = df[df[('', '', 'Name')] == p1][attributes].values.flatten()
    data2 = df[df[('', '', 'Name')] == p2][attributes].values.flatten()
    print(data1)
    print(data2)
    limits = [40, 50, 10, 1, 40]
    # Kiểm tra nếu có thiếu dữ liệu
    if data1.size == 0 or data2.size == 0:
        print(f"One or both players have missing data for the selected attributes.")
    else:

        scaler = StandardScaler()
        data_combined = np.vstack([data1, data2])  # Kết hợp dữ liệu hai cầu thủ
        data_scaled = scaler.fit_transform(data_combined)
    
        # Chuẩn bị dữ liệu sau khi chuẩn hóa cho từng cầu thủ
        data1_scaled = np.array([val / lim for val, lim in zip(data1, limits)])
        data2_scaled = np.array([val / lim for val, lim in zip(data2, limits)])
        data1_scaled = np.append(data1_scaled, data1_scaled[0])
        data2_scaled = np.append(data2_scaled, data2_scaled[0])
        # Thiết lập các nhãn và góc cho biểu đồ radar
        labels = [f'{attr[2]}' for attr in attributes]  # Lấy tên chỉ số từ attributes
        num_vars = len(attributes)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        # Vẽ biểu đồ radar
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        #  # Giới hạn trục y tối đa
        # ax.set_ylim(0, 1.2)  # Thiết lập phạm vi từ 0 đến 1.2 để kiểm soát độ lệch

        ax.fill(angles, data1_scaled, color='blue', alpha=0.25, label=p1)
        ax.fill(angles, data2_scaled, color='red', alpha=0.25, label=p2)
        ax.plot(angles, data1_scaled, color='blue', linewidth=2)
        ax.plot(angles, data2_scaled, color='red', linewidth=2)

        # Thiết lập các nhãn
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        # Thêm tiêu đề và chú thích
        plt.title(f"So sánh cầu thủ {p1} và {p2}")
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        plt.savefig(os.path.join(output_dir, f'Radar_chart.png'))
        plt.close() 
        print("Hinh anh da duoc luu vào thu muc hinh_ve")