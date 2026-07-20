from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.family"] = "DejaVu Sans"


def add_box(ax, x, y, w, h, text, face="#f6f7f9", edge="#3d4a57", size=8.5):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.018",
        linewidth=1.0,
        facecolor=face,
        edgecolor=edge,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def add_arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=10,
        linewidth=1.0, color="#3d4a57"
    ))


def framework():
    fig, ax = plt.subplots(figsize=(13.2, 5.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, 0.02, 0.41, 0.08, 0.17, "Input\nimage")
    add_box(ax, 0.125, 0.41, 0.10, 0.17, "Semantic\nencoder")
    add_box(ax, 0.25, 0.41, 0.11, 0.17, "HDA\nallocation")

    add_box(ax, 0.40, 0.68, 0.13, 0.18, "Quantization\nLDPC + AMC", face="#eaf2ff")
    add_box(ax, 0.40, 0.14, 0.13, 0.18, "Analog encoder\nPower norm.", face="#edf7ea")

    add_box(ax, 0.565, 0.68, 0.13, 0.18, "Rician channel\nImperfect CSI", face="#fff4e5")
    add_box(ax, 0.565, 0.14, 0.13, 0.18, "Rician channel\nAnalog detection", face="#fff4e5")

    add_box(ax, 0.73, 0.68, 0.13, 0.18, "Uncertainty-aware\nMAP demodulation", face="#fcebea", size=8.0)
    add_box(ax, 0.73, 0.14, 0.13, 0.18, "Analog decoder\nDiffusion denoiser", face="#edf7ea", size=8.0)

    add_box(ax, 0.73, 0.42, 0.13, 0.14, "Physical / semantic\nerasure control", face="#f3eefb", size=8.0)
    add_box(ax, 0.885, 0.42, 0.095, 0.14, "Weighted\nfusion", face="#eef5f5")

    add_arrow(ax, 0.10, 0.495, 0.125, 0.495)
    add_arrow(ax, 0.225, 0.495, 0.25, 0.495)
    add_arrow(ax, 0.36, 0.53, 0.40, 0.77)
    add_arrow(ax, 0.36, 0.46, 0.40, 0.23)
    add_arrow(ax, 0.53, 0.77, 0.565, 0.77)
    add_arrow(ax, 0.53, 0.23, 0.565, 0.23)
    add_arrow(ax, 0.695, 0.77, 0.73, 0.77)
    add_arrow(ax, 0.695, 0.23, 0.73, 0.23)
    add_arrow(ax, 0.795, 0.68, 0.795, 0.56)
    add_arrow(ax, 0.86, 0.49, 0.885, 0.49)
    add_arrow(ax, 0.795, 0.32, 0.92, 0.42)

    ax.text(0.465, 0.92, "Digital branch", ha="center", fontsize=10, fontweight="bold")
    ax.text(0.465, 0.07, "Analog branch", ha="center", fontsize=10, fontweight="bold")
    ax.text(0.82, 0.92, "Receiver and controllable impairment layer", ha="center", fontsize=10, fontweight="bold")

    ui_text = (
        "Operator interface controls: SNR | CSI mode | target NMSE | receiver | "
        "loss mode | target loss | alpha_d | recovery | seed"
    )
    ax.text(0.5, 0.015, ui_text, ha="center", va="bottom", fontsize=8.4)

    fig.tight_layout(pad=0.4)
    fig.savefig(FIG_DIR / "framework.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "framework.pdf", bbox_inches="tight")
    plt.close(fig)


def nmse_results():
    nmse = np.array([0.10, 0.20, 0.50, 1.00])
    ber = np.array([0.009557, 0.016187, 0.022957, 0.019637])
    psnr = np.array([1.040, 1.445, 1.058, 0.022])
    x = np.arange(len(nmse))
    labels = [f"{v:.2f}" for v in nmse]

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.8))
    bars = axes[0].bar(x, ber, width=0.62, edgecolor="black", linewidth=0.8, hatch="//")
    axes[0].set_xticks(x, labels)
    axes[0].set_xlabel("Target channel-estimation NMSE")
    axes[0].set_ylabel("Average BER reduction")
    axes[0].grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, ber):
        axes[0].text(bar.get_x() + bar.get_width()/2, value + 0.0005, f"{value:.3f}", ha="center", fontsize=8)

    bars = axes[1].bar(x, psnr, width=0.62, edgecolor="black", linewidth=0.8, hatch="..")
    axes[1].set_xticks(x, labels)
    axes[1].set_xlabel("Target channel-estimation NMSE")
    axes[1].set_ylabel("Average PSNR gain (dB)")
    axes[1].grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, psnr):
        axes[1].text(bar.get_x() + bar.get_width()/2, value + 0.04, f"{value:.3f}", ha="center", fontsize=8)

    fig.tight_layout(w_pad=2.0)
    fig.savefig(FIG_DIR / "nmse_results.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "nmse_results.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    framework()
    nmse_results()
    print(f"Generated figures in {FIG_DIR}")
