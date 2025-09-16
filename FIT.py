import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
def fit_coefficients(file_path):
    # 读取数据
    # file_path = "C:\\Users\\A0001975\\Desktop\\CHENAN2.txt"
    data = pd.read_csv(file_path, sep="\t", engine="python")

    # 去掉可能多余的空格
    data.columns = data.columns.str.strip()

    # 提取列
    focal = data["焦距"].values
    gx = data["GGX"].values
    gy = data["GGY"].values

    # 三次拟合
    coef_gx = np.polyfit(focal, gx, 3)
    coef_gy = np.polyfit(focal, gy, 3)

    # 调整为 0次 1次 2次 3次 排列（polyfit是从高次到低次输出的）
    coef_gx = coef_gx[::-1]
    coef_gy = coef_gy[::-1]
    # 合并GX和GY为一个列表
    gx_gy_combined = list(coef_gx) + list(coef_gy)
    print("GX拟合系数:", coef_gx)
    print("GY拟合系数:", coef_gy)
    return  gx_gy_combined
# print(fit_coefficients())