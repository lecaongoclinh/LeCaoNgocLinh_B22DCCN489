import pandas as pd

# Đọc file CSV với header đa cấp
df = pd.read_csv('result.csv', header=[0, 1, 2])

# Thay thế 'Unnamed:' bằng khoảng trắng
df.columns = [tuple('' if 'Unnamed:' in x else x for x in col) for col in df.columns]
print("Cột sau khi thay đổi:", df.columns)

# Danh sách để lưu kết quả
results_top_bottom = []

def collect_top_bottom(df, column, n=3):
    # Kiểm tra nếu 'Name' không tồn tại
    name_col = ('', '', 'Name')
    team_col = ('', '', 'Team')
    if name_col not in df.columns:
        print("Lỗi: Cột 'Name' không tồn tại trong DataFrame!")
        return

    top = df.nlargest(n, column)[[name_col, team_col, column]]
    bottom = df.nsmallest(n, column)[[name_col, team_col, column]]
    
    att = '_'.join(filter(None, column))  # Tạo tên chỉ số từ tuple
    results_top_bottom.append({'Metric': att, 'Type': 'Top', 'Name': '', 'Team': '', 'Score': ''})

    for _, row in top.iterrows():
        results_top_bottom.append({'Metric': '', 'Type': 'Top', 'Name': row[name_col], 'Team': row[team_col], 'Score': row[column]})

    results_top_bottom.append({'Metric': '', 'Type': '', 'Name': '', 'Team': '', 'Score': ''})  # Dòng trống
    results_top_bottom.append({'Metric': att, 'Type': 'Bottom', 'Name': '', 'Team': '', 'Score': ''})

    for _, row in bottom.iterrows():
        results_top_bottom.append({'Metric': '', 'Type': 'Bottom', 'Name': row[name_col], 'Team': row[team_col], 'Score': row[column]})

    results_top_bottom.append({'Metric': '', 'Type': '', 'Name': '', 'Team': '', 'Score': ''})  # Dòng trống

# Duyệt qua các chỉ số dạng số và tìm top/bottom 
numeric_cols = df.columns[5:]  # Lấy cột từ thứ 6 trở đi
for col in numeric_cols:
    if pd.api.types.is_numeric_dtype(df[col]):
        collect_top_bottom(df, col)

# Chuyển danh sách kết quả thành DataFrame
results_df = pd.DataFrame(results_top_bottom)

# Ghi vào file txt
with open('top_bottom.txt', 'w', encoding='utf-8') as file:
    file.write(results_df.to_string(index=False))  # Không ghi chỉ số

# Ghi kết quả ra file CSV
results_df.to_csv('top_bottom.csv', index=False)
print("Danh sách đã được lưu vào file top_bottom.csv")
