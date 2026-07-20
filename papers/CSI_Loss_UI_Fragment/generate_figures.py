from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

matplotlib.rcParams["font.family"] = "Noto Sans CJK SC"
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["axes.unicode_minus"] = False


def box(ax, x, y, w, h, text, fc="#f4f6f8", ec="#34495e", fs=9):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.018",
        linewidth=1.0,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def arrow(ax, x1, y1, x2, y2, rad=0.0):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=11,
        linewidth=1.0, color="#34495e",
        connectionstyle=f"arc3,rad={rad}",
    ))


def make_integrated_framework():
    fig, ax = plt.subplots(figsize=(13.2, 5.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box(ax, 0.015, 0.40, 0.075, 0.18, "输入图像")
    box(ax, 0.11, 0.40, 0.10, 0.18, "语义编码器")
    box(ax, 0.235, 0.40, 0.12, 0.18, "数字—模拟\n特征分配")

    box(ax, 0.39, 0.67, 0.14, 0.18, "量化 / LDPC / AMC", fc="#eaf2ff")
    box(ax, 0.39, 0.13, 0.14, 0.18, "模拟编码与\n功率归一化", fc="#edf7ed")

    box(ax, 0.565, 0.67, 0.13, 0.18, "Rician信道\n不完美CSI", fc="#fff4e6")
    box(ax, 0.565, 0.13, 0.13, 0.18, "Rician信道\n模拟检测", fc="#fff4e6")

    box(ax, 0.73, 0.73, 0.12, 0.13, "不确定性感知\n软解调", fc="#fdecec")
    box(ax, 0.73, 0.56, 0.12, 0.11, "物理层人工擦除", fc="#fdecec")
    box(ax, 0.73, 0.39, 0.12, 0.11, "LDPC译码")
    box(ax, 0.73, 0.22, 0.12, 0.11, "语义包人工擦除", fc="#f5ecff")
    box(ax, 0.73, 0.07, 0.12, 0.10, "模拟支路恢复", fc="#edf7ed")

    box(ax, 0.875, 0.37, 0.09, 0.19, "可调权重\n特征融合")
    box(ax, 0.97, 0.40, 0.025, 0.13, "解\n码", fs=8)

    arrow(ax, 0.09, 0.49, 0.11, 0.49)
    arrow(ax, 0.21, 0.49, 0.235, 0.49)
    arrow(ax, 0.355, 0.52, 0.39, 0.76, -0.10)
    arrow(ax, 0.355, 0.46, 0.39, 0.22, 0.10)
    arrow(ax, 0.53, 0.76, 0.565, 0.76)
    arrow(ax, 0.53, 0.22, 0.565, 0.22)
    arrow(ax, 0.695, 0.76, 0.73, 0.795)
    arrow(ax, 0.79, 0.73, 0.79, 0.67)
    arrow(ax, 0.79, 0.56, 0.79, 0.50)
    arrow(ax, 0.79, 0.39, 0.79, 0.33)
    arrow(ax, 0.79, 0.22, 0.885, 0.465, -0.20)
    arrow(ax, 0.695, 0.22, 0.73, 0.12)
    arrow(ax, 0.85, 0.12, 0.885, 0.425, 0.16)
    arrow(ax, 0.965, 0.465, 0.97, 0.465)

    ax.text(0.455, 0.91, "数字支路", fontsize=11, fontweight="bold", ha="center")
    ax.text(0.455, 0.045, "模拟支路", fontsize=11, fontweight="bold", ha="center")
    ax.text(0.79, 0.93, "接收端可靠性控制", fontsize=11, fontweight="bold", ha="center")

    fig.tight_layout(pad=0.5)
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"integrated_framework.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def make_operator_interface():
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box(ax, 0.03, 0.84, 0.94, 0.11,
        "参数控制区：SNR｜CSI模式｜NMSE｜丢包模式｜人工丢包率｜数字/模拟权重｜填充策略",
        fc="#edf3ff", fs=10)
    box(ax, 0.05, 0.41, 0.41, 0.35, "输入图像\n\n（上传或选择测试图）", fc="#f8f8f8", fs=11)
    box(ax, 0.54, 0.41, 0.41, 0.35, "重建图像\n\n（实时显示接收结果）", fc="#f8f8f8", fs=11)

    metrics = [
        ("BER", "比特级"), ("PER", "包级"), ("FER", "帧级"),
        ("PSNR", "像素质量"), ("MS-SSIM", "结构质量"),
        ("LPIPS", "感知距离"), ("VIF", "视觉信息"), ("FID", "批量统计"),
    ]
    x0, y0 = 0.04, 0.15
    w, h, gap = 0.105, 0.12, 0.012
    for idx, (name, desc) in enumerate(metrics):
        x = x0 + idx * (w + gap)
        box(ax, x, y0, w, h, f"{name}\n{desc}", fc="#f6f1ff", fs=9)

    ax.text(0.50, 0.97, "操作者交互界面信息结构", ha="center", va="center", fontsize=13, fontweight="bold")
    ax.text(0.50, 0.06, "单图模式不报告FID；批量评估时统一记录随机种子、目标率、实际率和掩码重叠率。",
            ha="center", va="center", fontsize=9)

    fig.tight_layout(pad=0.5)
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"operator_interface.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_integrated_framework()
    make_operator_interface()
    print(f"Figures generated in {FIG_DIR}")
