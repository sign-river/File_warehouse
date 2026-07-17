# HDA-DeepSC 不完美 CSI 论文 LaTeX 版

本目录使用 `ctexart`，适合 **TeXstudio + CTeX**，推荐使用 **XeLaTeX** 编译。

## 文件说明

- `main.tex`：论文正文，已包含摘要、引言、系统模型、公式、实验表格、结论等。
- `references.bib`：参考文献数据库。
- `figures/`：实验图片目录。图片缺失时，正文仍可编译，只会显示占位框。

## TeXstudio 编译方法

1. 下载整个 `HDA_DeepSC_Imperfect_CSI_LaTeX` 文件夹。
2. 用 TeXstudio 打开 `main.tex`。
3. 菜单中选择：`选项 -> 设置 TeXstudio -> 构建 -> 默认编译器 -> XeLaTeX`。
4. 首次完整编译按以下顺序：

```text
XeLaTeX
BibTeX
XeLaTeX
XeLaTeX
```

也可以在命令行执行：

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

最终生成 `main.pdf`。

## 如何加入周记 Word 中的图片

`.docx` 本质上是压缩包，最简单的图片提取方法：

1. 复制一份 `周记 260620.docx`；
2. 将副本改名为 `周记 260620.zip`；
3. 解压后进入 `word/media/`；
4. 里面的 `image1.png`、`image2.jpeg` 等就是原文图片；
5. 按需要重命名并复制到本目录的 `figures/` 文件夹。

建议文件名：

```text
figures/reconstruction_progress.png
figures/absolute_psnr.png
figures/controlled_nmse_ber_gain.png
figures/controlled_nmse_psnr_gain.png
figures/paired_ber_gain_np1.png
figures/paired_ber_gain_np4.png
figures/paired_psnr_gain_np1.png
figures/paired_psnr_gain_np4.png
```

## 从项目结果目录复制图片

在 `/workspace/HDA_DeepSC_Reproduction` 下执行，可按实际存在路径调整：

```bash
mkdir -p paper_latex/figures

cp results/three_group_csi/plots/absolute_psnr.png \
   paper_latex/figures/absolute_psnr.png

cp results/receiver_evidence_report/plots/controlled_nmse_ber_gain.png \
   paper_latex/figures/controlled_nmse_ber_gain.png

cp results/receiver_evidence_report/plots/controlled_nmse_psnr_gain.png \
   paper_latex/figures/controlled_nmse_psnr_gain.png

cp results/receiver_evidence_report/plots/paired_ber_gain_np1.png \
   paper_latex/figures/paired_ber_gain_np1.png

cp results/receiver_evidence_report/plots/paired_ber_gain_np4.png \
   paper_latex/figures/paired_ber_gain_np4.png

cp results/receiver_evidence_report/plots/paired_psnr_gain_np1.png \
   paper_latex/figures/paired_psnr_gain_np1.png

cp results/receiver_evidence_report/plots/paired_psnr_gain_np4.png \
   paper_latex/figures/paired_psnr_gain_np4.png
```

## 公式排版

正文公式均已使用 `equation`、`align`、`bm` 和 `mathtools` 环境排版，能够自动编号并使用 `\cref{}` 交叉引用。修改公式时不要把公式截图粘贴进论文，应直接改写 LaTeX 公式。

## 常见问题

### 中文乱码

确认使用 XeLaTeX，不要使用 pdfLaTeX。

### 找不到 IEEEtran.bst

若本地 CTeX 不含该样式，可将 `main.tex` 最后的：

```latex
\bibliographystyle{IEEEtran}
```

改为：

```latex
\bibliographystyle{plain}
```

### 图片不存在

正文会显示占位框，不会阻止编译。把对应图片复制到 `figures/` 后再次编译即可。
