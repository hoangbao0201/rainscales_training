import pandas as pd

# data = {
#     'Name': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Hùng', 'Lan', 'Mai', 'Nam', 'Trang'],
#     'Age': [20, 21, 19, 22, 20, 23, 21, 20, 22, 19],
#     'Gender': ['Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nữ'],
#     'Score': [8.5, 7.0, 9.0, 4.5, 6.0, 3.5, 5.5, 8.0, 6.5, 4.0]
# }

data = {
    'Name': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Hùng', 'Lan', 'Mai', 'Nam', 'Trang', 'Quân', 'Vy', 'Tuấn', 'Linh', 'Phong', 'Ngọc', 'Minh', 'Yến', 'Sơn', 'Thảo'],
    'Age': [20, 21, 19, 22, 20, 23, 21, 20, 22, 19, 24, 20, 23, 19, 22, 21, 20, 18, 22, 19],
    'Gender': ['Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ'],
    'Score': [8.5, 7.0, 9.0, 4.5, 6.0, 3.5, 5.5, 8.0, 6.5, 4.0, 7.5, 9.5, 5.0, 6.8, 4.2, 8.1, 7.9, 3.0, 6.3, 2.5]
}

df_students = pd.DataFrame(data)

print("=== Toàn bộ dữ liệu ===")
print(df_students)

print("\n\n=== 3 dòng đầu tiên ===")
print(df_students.head(3))

print("\n\n=== Tên sinh viên tại index=2 ===")
print(df_students.loc[2, 'Name'])

print("\n\n=== Tuổi sinh viên tại index=10 ===")
if 10 in df_students.index:
    print(df_students.loc[10, 'Age'])
else:
    print("Index 10 không tồn tại trong DataFrame.")

print("\n\n=== Các cột Name và Score ===")
print(df_students[['Name', 'Score']])

df_students['Pass'] = df_students['Score'] >= 5
print("\n\n=== Thêm cột Pass ===")
print(df_students)

df_sorted = df_students.sort_values(by='Score', ascending=False)
print("\n\n=== Sắp xếp theo Score giảm dần ===")
print(df_sorted)
