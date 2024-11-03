import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv("result2.csv")

# Tìm đội có điểm cao nhất ở mỗi chỉ số dựa trên giá trị trung bình (mean)
top_teams_by_mean = []

# Lặp qua từng cột để tìm đội bóng có điểm trung bình cao nhất
for column in df.columns:
    if column.startswith('Mean of'):
        max_mean_team = df.loc[df[column].idxmax(), 'Team']  # Tên đội bóng
        max_mean_value = df[column].max()  # Giá trị điểm trung bình cao nhất
        top_teams_by_mean.append([column.replace('Mean of ', ''), max_mean_team, max_mean_value])

# Tạo DataFrame từ danh sách kết quả
top_teams_df = pd.DataFrame(top_teams_by_mean, columns=['Attribute', 'Top Team', 'Mean Value'])
print(top_teams_df)

# Ghi kết quả vào file CSV
top_teams_df.to_csv('top_teams_by_mean.csv', index=False)
print("Du lieu da duoc luu vao file op_teams_by_mean.csv")

# Tìm đội có phong độ tốt nhất
mean_columns = [col for col in df.columns if col.startswith('Mean of')]
df['Total Mean Score'] = df[mean_columns].sum(axis=1)  # Tính tổng điểm trung bình

# Tìm đội bóng có phong độ tốt nhất
top_team = df.loc[df['Total Mean Score'].idxmax(), 'Team']
top_score = df['Total Mean Score'].max()
print(f"Đội bóng có phong độ tốt nhất: {top_team} với tổng điểm trung bình: {top_score}")
