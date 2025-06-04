import pandas as pd
import numpy as np

df_nv = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105, 106, 107, 108],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh', 'Giang', np.nan],
    'Age': [25, np.nan, 30, 22, 28, 35, np.nan, 31],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan, 'Marketing', 'IT'],
    'Salary': [700, 800, 750, np.nan, 710, 770, 690, np.nan]
})

df_pb = pd.DataFrame({
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
})

print("\n ================ Bài 1 ================")
print(df_nv.isnull())

print("\n ================ Bài 2 ================")
df_nv = df_nv[df_nv.isnull().sum(axis=1) <= 2]
print(df_nv)

print("\n ================ Bài 3 ================")
df_nv['Name'] = df_nv['Name'].fillna("Chưa rõ")
df_nv['Age'] = df_nv['Age'].fillna(df_nv['Age'].mean())
df_nv['Salary'] = df_nv['Salary'].ffill()
df_nv['Department'] = df_nv['Department'].fillna("Unknown")
print(df_nv)

print("\n ================ Bài 4 ================")
df_nv['Age'] = df_nv['Age'].astype(int)
df_nv['Salary'] = df_nv['Salary'].astype(int)
print(df_nv.dtypes)

print("\n ================ Bài 5 ================")
df_nv['Salary_after_tax'] = df_nv['Salary'] * 0.9
print(df_nv[['Name', 'Salary', 'Salary_after_tax']])

print("\n ================ Bài 6 ================")
df_it = df_nv[(df_nv['Department'] == 'IT') & (df_nv['Age'] > 25)]
print(df_it)

print("\n ================ Bài 7 ================")
df_sorted = df_nv.sort_values(by='Salary_after_tax', ascending=False)
print(df_sorted[['Name', 'Salary_after_tax']])

print("\n ================ Bài 8 ================")
df_avg_salary = df_nv.groupby('Department')['Salary'].mean().reset_index()
print(df_avg_salary)

print("\n ================ Bài 9 ================")
df_merged = pd.merge(df_nv, df_pb, on='Department', how='left')
print(df_merged[['Name', 'Department', 'Manager']])

print("\n ================ Bài 10 ================")
df_new = pd.DataFrame({
    'ID': [109, 110],
    'Name': ['Lâm', 'Ngọc'],
    'Age': [27, 29],
    'Department': ['Marketing', 'IT'],
    'Salary': [730, 810]
})
df_new['Salary_after_tax'] = df_new['Salary'] * 0.9
df_new['Age'] = df_new['Age'].astype(int)
df_new['Salary'] = df_new['Salary'].astype(int)

df_final = pd.concat([df_nv, df_new], ignore_index=True)
print(df_final)
