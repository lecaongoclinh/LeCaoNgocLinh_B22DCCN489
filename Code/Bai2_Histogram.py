import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import re
# Đọc dữ liệu từ CSV với header đa cấp
df = pd.read_csv('result.csv', header=[0, 1, 2])

# Làm sạch tên cột
df.columns = [tuple('' if 'Unnamed:' in x else x for x in col) for col in df.columns]

# Lọc các cột có kiểu dữ liệu số (float và int)
numeric_cols = df.select_dtypes(include=['float', 'int']).columns
# Đường dẫn đến thư mục
output_dir = 'hinh_ve'

# Tạo thư mục nếu nó không tồn tại
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#Tắt chế độ tương tác
plt.ioff()
# Hàm để làm sạch tên tệp
def clean_filename(name):
    # Thay thế các ký tự không hợp lệ bằng dấu gạch dưới
    return re.sub(r'[<>:"/\\|?*]', '_', name)
# Vẽ biểu đồ histogram cho từng thuộc tính số theo từng đội
for cnt, att in enumerate(numeric_cols, start=1):
    # Ghép tên cột để tạo tiêu đề cho biểu đồ
    his_name = "_".join(filter(None, att))  # Kết hợp các phần trong tuple không rỗng
    his_name_cleaned = clean_filename(his_name)  # Làm sạch tên tệp
  # Kết hợp các phần trong tuple không rỗng

    # Biểu đồ toàn bộ dữ liệu
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=att, kde=True, bins=20)
    plt.title(f"Histogram {his_name} of All Players in the League")
    his_name_cleaned = clean_filename(his_name)  # Làm sạch tên tệp
    plt.xlabel(his_name)
    plt.ylabel("Tần suất")
   
    # Lưu biểu đồ vào thư mục hinh ve
    plt.savefig(os.path.join(output_dir, f'histogram_{his_name_cleaned}.png'))
    print("Hinh anh da duoc luu vào thu muc hinh_ve")
    plt.close()   # Đóng hình để tránh hiển thị

    # Biểu đồ theo từng đội
    g = sns.FacetGrid(df, col=('','','Team'), col_wrap=4, height=3, sharex=True, sharey=True)
    g.map_dataframe(sns.histplot, x=att, bins=20, kde=True)
    g.set_axis_labels(his_name, "Tần suất")  # Đặt tên trục x
    g.set_titles(f"{his_name} of {{col_name}}")  # Tiêu đề

    # Căn chỉnh và hiển thị biểu đồ
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'facet_{his_name_cleaned}.png'))
    print("Hinh anh da duoc luu vào thu muc hinh_ve")
    plt.close()  # Đóng hình để tránh hiển thị
