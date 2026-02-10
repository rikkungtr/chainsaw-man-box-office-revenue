from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.backends.backend_agg
import numpy as np
from scipy.optimize import curve_fit


# Create a canvas with Agg backend then save it as a file.
#     canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
#     canvas.print_figure(file_name, dpi=300)
#     print(file_name + ' has been saved.')
# You can show the plot on the display, too.
#     show.plt

FILE_NAME = "./chainsaw-man-box-office-revenue-forecast.png"

# 日本語フォント
plt.rcParams["font.family"] = "Noto Sans CJK JP"

GRAPF_TITLE = "劇場版 チェンソーマン レゼ篇 興行収入推移と予測（ゴールデンウィーク開けまでの指数減衰モデル）"

# 2026年2月26日（木）（公開33週、231日）までプロット
MAX_DAY = 230

# ターゲットライン
TARGET = 107
TARGET_LABLE_1 = f"{TARGET + 3}億円ライン"
TARGET_LABEL_2 = f"{TARGET}億円ライン"
TARGET_LABEL_3 = f"{TARGET - 3}億円ライン"

X_LEGEND = "興行収入"
FIT_LEGEND = "指数減衰フィット曲線"

X_LABLE = "公開日 2025年9月19日（金）から 2026年5月7日（木）までの32週（231日間）"
Y_LABLE = "興行収入（億円）"


# データ
days = np.array(
    [
        1, 3, 4, 6,
        10, 17, 24, 31,
        38, 42, 46, 52,
        59, 73, 80, 88,
        95, 102, 108, 116,
        122, 129, 136, 143
    ]
)
revenue = np.array(
    [
        4.2, 12.51, 15.2, 20,
        29, 43, 54, 65,
        71.7, 73.8, 79, 83.1,
        87.7, 92.8, 94.9, 96.2,
        98, 99.5, 101.5, 102.8,
        103.7, 104.3, 105.1, 105.6
    ]
)

# 公開日
release_date = datetime(2025, 9, 19)
dates = np.array([release_date + timedelta(days=int(d)) for d in days])


# 指数減衰モデル（オーバーフロー防御あり）
def exp_decay(x, A, B, k):
    z = -k * x
    # exp のオーバーフローを防ぐクリップ（安全側）
    z = np.clip(z, -700, 700)
    return A - B * np.exp(z)


# フィット: 初期値 p0 をデータから自動算出し、k>=0 を制約する
A0 = max(revenue[-1], revenue.max()) * 1.02
B0 = max(A0 - revenue[0], 1e-6)
i1, i2 = 0, min(4, len(days) - 1)
y1, y2 = revenue[i1], revenue[i2]
x1, x2 = days[i1], days[i2]
if (A0 - y1) > 0 and (A0 - y2) > 0 and x2 != x1:
    K0 = -np.log((A0 - y2) / (A0 - y1)) / (x2 - x1)
    if not np.isfinite(K0) or K0 <= 0:
        K0 = 0.02
else:
    K0 = 0.02
p0 = [A0, B0, K0]
bounds = ([0, 0, 0], [np.inf, np.inf, np.inf])  # k>=0 を強制
popt, pcov, *_ = curve_fit(exp_decay, days, revenue, p0=p0, bounds=bounds, maxfev=100000)
A, B, k = popt

x_fit = np.linspace(0, MAX_DAY, 3000)
y_fit = exp_decay(x_fit, A, B, k)
dates_fit = np.array([release_date + timedelta(days=float(d)) for d in x_fit])

# プロット
fig, ax = plt.subplots(figsize=(8, 8))

# 凡例位置（調整可能）
LEGEND_LOC = "upper right"
LEGEND_BBOX = (0.9875, 0.897)
LEGEND_NCOL = 1

# 枠線（spines）と目盛線を太くする
for spine in ax.spines.values():
    spine.set_linewidth(2.5)
# 目盛り線を太くし、グラフの内側に。
ax.tick_params(width=2.5, direction="in", length=6)

# 実測データ
ax.plot(dates, revenue, "o", label=X_LEGEND)

# 指数減衰フィット曲線
ax.plot(dates_fit, y_fit, "-", label=FIT_LEGEND)

# ターゲットライン
ax.axhline(TARGET + 3, color="grey", linestyle="dotted", label=TARGET_LABLE_1)
ax.axhline(TARGET, color="red", linestyle="--", label=TARGET_LABEL_2)
ax.axhline(TARGET - 3, color="green", linestyle="--", label=TARGET_LABEL_3)

# 各点に日数注釈
for d, r, day in zip(dates, revenue, days):
    ax.annotate(
        f"{day}日",
        xy=(d, r),
        xytext=(3, -8),
        textcoords="offset points",
        fontsize=10,
        ha="left",
        rotation=-45,
        weight="bold",
        rotation_mode="anchor",
    )

# 軸設定
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.set_xlabel(X_LABLE)
ax.set_ylabel(Y_LABLE)

# 目盛りラベルを全て太字にする（x軸・y軸）
for label in ax.get_xticklabels():
    label.set_fontweight("bold")
for label in ax.get_yticklabels():
    label.set_fontweight("bold")

ax.set_title(
    label=GRAPF_TITLE,
    fontweight="bold",
)

ax.grid(True)
ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX, ncol=LEGEND_NCOL)
plt.tight_layout()
ax.set_ylim(bottom=0)

canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
canvas.print_figure(FILE_NAME, dpi=300)
print(FILE_NAME + ' has been saved.')

plt.show()
