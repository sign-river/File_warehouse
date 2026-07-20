from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False


def add_box(ax, x, y, w, h, text, facecolor="#f5f7fb", edgecolor="#3b4a5a", fontsize=9):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.1,
        facecolor=facecolor,
        edgecolor=edgecolor,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)
    return box


def add_arrow(ax, x1, y1, x2, y2, connectionstyle="arc3"):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=11,
        linewidth=1.0,
        color="#34495e",
        connectionstyle=connectionstyle,
    )
    ax.add_patch(arrow)


def make_system_architecture() -> None:
    fig, ax = plt.subplots(figsize=(12.8, 4.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    y_mid = 0.50
    add_box(ax, 0.015, 0.405, 0.085, 0.19, "Input\nimage")
    add_box(ax, 0.125, 0.405, 0.105, 0.19, "Semantic\nencoder")
    add_box(ax, 0.255, 0.405, 0.115, 0.19, "Digital--analog\nallocation")

    add_box(ax, 0.405, 0.675, 0.145, 0.19, "Quantization,\nLDPC, AMC", facecolor="#eaf2ff")
    add_box(ax, 0.405, 0.135, 0.145, 0.19, "Analog encoder\nand power norm.", facecolor="#f1f8ed")

    add_box(ax, 0.585, 0.675, 0.145, 0.19, "Rician channel\nand CSI estimate", facecolor="#fff4e6")
    add_box(ax, 0.585, 0.135, 0.145, 0.19, "Rician channel\nand LS detection", facecolor="#fff4e6")

    add_box(ax, 0.765, 0.675, 0.145, 0.19, "Uncertainty-aware\nsoft demodulation", facecolor="#fcebea")
    add_box(ax, 0.765, 0.135, 0.145, 0.19, "Analog decoder\n/ DiffSDNet", facecolor="#f1f8ed")

    add_box(ax, 0.805, 0.405, 0.095, 0.16, "Feature\nfusion")
    add_box(ax, 0.925, 0.405, 0.06, 0.16, "Semantic\ndecoder", fontsize=8.5)

    add_arrow(ax, 0.100, y_mid, 0.125, y_mid)
    add_arrow(ax, 0.230, y_mid, 0.255, y_mid)

    add_arrow(ax, 0.370, 0.53, 0.405, 0.77, connectionstyle="arc3,rad=-0.12")
    add_arrow(ax, 0.370, 0.47, 0.405, 0.23, connectionstyle="arc3,rad=0.12")

    add_arrow(ax, 0.550, 0.77, 0.585, 0.77)
    add_arrow(ax, 0.550, 0.23, 0.585, 0.23)
    add_arrow(ax, 0.730, 0.77, 0.765, 0.77)
    add_arrow(ax, 0.730, 0.23, 0.765, 0.23)

    add_arrow(ax, 0.837, 0.675, 0.852, 0.565, connectionstyle="arc3,rad=0.10")
    add_arrow(ax, 0.837, 0.325, 0.852, 0.405, connectionstyle="arc3,rad=-0.10")
    add_arrow(ax, 0.900, 0.485, 0.925, 0.485)

    ax.text(0.47, 0.92, "Digital branch", ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(0.47, 0.075, "Analog branch", ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(0.84, 0.925, "Receiver extension", ha="center", va="center", fontsize=10.5, fontweight="bold")

    fig.tight_layout(pad=0.4)
    for suffix in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"system_architecture.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def make_controlled_nmse_results() -> None:
    nmse = np.asarray([0.10, 0.20, 0.50, 1.00], dtype=float)
    ber_reduction = np.asarray([0.009557, 0.016187, 0.022957, 0.019637], dtype=float)
    psnr_gain = np.asarray([1.040, 1.445, 1.058, 0.022], dtype=float)

    x = np.arange(nmse.size)
    labels = [f"{value:.2f}" for value in nmse]

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.75))

    bars1 = axes[0].bar(x, ber_reduction, width=0.62, edgecolor="black", linewidth=0.8, hatch="//")
    axes[0].set_xticks(x, labels)
    axes[0].set_xlabel("Target channel-estimation NMSE")
    axes[0].set_ylabel("Average BER reduction")
    axes[0].grid(axis="y", alpha=0.25, linewidth=0.7)
    axes[0].set_axisbelow(True)
    for bar, value in zip(bars1, ber_reduction):
        axes[0].text(bar.get_x() + bar.get_width() / 2, value + 0.00055, f"{value:.3f}", ha="center", va="bottom", fontsize=8)

    bars2 = axes[1].bar(x, psnr_gain, width=0.62, edgecolor="black", linewidth=0.8, hatch="..")
    axes[1].set_xticks(x, labels)
    axes[1].set_xlabel("Target channel-estimation NMSE")
    axes[1].set_ylabel("Average PSNR gain (dB)")
    axes[1].grid(axis="y", alpha=0.25, linewidth=0.7)
    axes[1].set_axisbelow(True)
    for bar, value in zip(bars2, psnr_gain):
        axes[1].text(bar.get_x() + bar.get_width() / 2, value + 0.045, f"{value:.3f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout(w_pad=2.2)
    for suffix in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"controlled_nmse_results.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_system_architecture()
    make_controlled_nmse_results()
    print(f"Generated figures in: {FIG_DIR}")


if __name__ == "__main__":
    main()
