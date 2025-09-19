import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fit_coefficients(file_path):
    # 读取数据
    data = pd.read_csv(file_path, sep="\t", engine="python")
    data.columns = data.columns.str.strip()

    focal = data["焦距"].values
    gx = data["GGX"].values
    gy = data["GGY"].values

    # 权重：0-100mm内权重大
    weights = np.where(focal <= 100, 5.0, 1.0)   # 你可以调节 5.0 -> 10.0 来加强权重

    # 加权三次拟合
    coef_gx = np.polyfit(focal, gx, 3, w=weights)
    coef_gy = np.polyfit(focal, gy, 3, w=weights)

    # 转换为 0次 1次 2次 3次 排列
    coef_gx = coef_gx[::-1]
    coef_gy = coef_gy[::-1]

    gx_gy_combined = list(coef_gx) + list(coef_gy)

    print("GX拟合系数:", coef_gx)
    print("GY拟合系数:", coef_gy)

    # 可视化对比
    p_gx = np.poly1d(coef_gx[::-1])  
    p_gy = np.poly1d(coef_gy[::-1])

    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.scatter(focal, gx, label="Raw GX")
    plt.plot(focal, p_gx(focal), 'r-', label="Fitted GX")
    plt.legend()
    plt.title("GX Fitting")

    plt.subplot(1,2,2)
    plt.scatter(focal, gy, label="Raw GY")
    plt.plot(focal, p_gy(focal), 'r-', label="Fitted GY")
    plt.legend()
    plt.title("GY Fitting")

    plt.show()

    return gx_gy_combined
