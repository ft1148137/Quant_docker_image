import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
x = np.arange(9)
y = np.sin(x)
z = np.cos(x)
# marker数据点样式，linewidth线宽，linestyle线型样式，color颜色
plt.plot(x, y, marker="*", linewidth=3, linestyle="--", color="orange")
plt.plot(x, z)
plt.title("matplotlib")
plt.xlabel("height")
plt.ylabel("width")
# 设置图例
plt.legend(["Y","Z"], loc="upper right")
plt.grid(True)
plt.show()
