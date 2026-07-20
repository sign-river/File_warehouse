---
title: "Uncertainty-Aware Soft Demodulation for Hybrid Digital--Analog Semantic Image Transmission with Imperfect CSI"
author:
  - "First Author"
  - "Second Author"
date: "Draft prepared July 2026"
lang: en-US
---

# Abstract

Hybrid digital--analog semantic communication combines a digital branch for essential semantic information with an analog branch for continuous residual information. This paper reproduces an image-transmission implementation of HDA-DeepSC and studies its digital receiver when the channel estimate is imperfect. We first show that replacing a least-squares equalizer with a linear robust minimum-mean-square-error equalizer does not necessarily improve channel-decoding performance. When the residual gain and filtered-noise variance are both passed consistently to the soft demodulator, the linear equalization coefficient cancels from the likelihood metric. We therefore formulate an uncertainty-aware maximum-a-posteriori soft demodulator directly in the received-signal domain. Channel-estimation error is modeled as a candidate-dependent variance term, so constellation points with different energies receive different reliability corrections while the original adaptive modulation and coding table remains unchanged. Controlled experiments in the 16-ary quadrature-amplitude-modulation region show average absolute bit-error-rate reductions of 0.0096, 0.0162, and 0.0230 at channel-estimation normalized mean-square-error levels of 0.1, 0.2, and 0.5, respectively. The corresponding average peak-signal-to-noise-ratio gains are 1.04, 1.45, and 1.06 dB. The observed benefit is modulation- and error-regime-dependent rather than universal.

**Keywords:** semantic communications; hybrid digital--analog transmission; imperfect channel state information; robust soft demodulation; Rician fading

# 1. Introduction

The objective of a conventional communication system is to reproduce transmitted symbols or bits with high fidelity. In contrast, semantic communication aims to preserve task-relevant meaning while using the available channel resources efficiently. Shannon's information theory provides the fundamental basis for reliable transmission [@shannon1948], while recent learning-based systems jointly optimize representation learning, channel mapping, and end-task distortion. DeepSC introduced an end-to-end semantic communication architecture for text [@xie2021deepsc], and deep joint source--channel coding demonstrated graceful image-quality degradation under channel mismatch and low signal-to-noise ratio [@bourtsoulatze2019deepjscc].

Purely analog and purely digital semantic links have complementary limitations. Continuous analog features are differentiable and degrade gradually, but they are difficult to integrate directly with standard modulation, channel coding, encryption, and packetized protocols. Quantized digital features are compatible with mature communication stacks, but they introduce quantization distortion and may exhibit a cliff effect near the channel-decoding threshold. HDA-DeepSC addresses this tradeoff by transmitting an essential representation through a digital branch and a residual representation through an analog branch [@xie2025hda].

A practical receiver does not know the propagation coefficient exactly. Finite pilot resources and receiver noise produce channel-estimation errors that affect equalization, soft demodulation, and forward-error correction. A common baseline replaces the true coefficient by its estimate and computes log-likelihood ratios as though the estimate were exact. This mismatched operation can generate overconfident soft information, especially when a high-order nonconstant-modulus constellation is selected by adaptive modulation and coding. Simply replacing least-squares equalization by a robust linear equalizer is not sufficient if the soft-demodulation model is transformed consistently, because the equalizer coefficient can cancel from the normalized distance.

This paper makes four contributions:

1. It reproduces the principal HDA-DeepSC image-transmission chain, including semantic coding, digital--analog allocation, scalar quantization, low-density parity-check coding, adaptive modulation and coding, Rician block fading, and analog residual transmission.
2. It extends the digital branch to pilot-aided and controlled-error channel-state-information models, and diagnoses why least-squares and linear robust minimum-mean-square-error equalizers can yield nearly identical decoded bit-error rates under gain-aware matched soft demodulation.
3. It develops a received-domain uncertainty-aware maximum-a-posteriori soft metric in which channel-estimation error contributes a constellation-candidate-dependent variance.
4. It uses same-checkpoint, same-channel, same-noise, and same-estimation-error paired experiments to isolate receiver effects. The results support a clear benefit in the 16-ary quadrature-amplitude-modulation region for moderate estimation errors, while also identifying the conditions under which the gain vanishes.

The claims are deliberately bounded. The current evidence is obtained with a real-valued single-coefficient Rician block-fading model and controlled channel-estimation errors. It does not establish universal gains for all modulation formats, all signal-to-noise-ratio values, or frequency-selective and multiple-antenna channels.

# 2. Related Work

## 2.1 Learning-Based Semantic and Joint Source--Channel Coding

Deep joint source--channel coding maps source samples directly to channel symbols and can be optimized using image distortion or task loss [@bourtsoulatze2019deepjscc]. Transformer-based semantic communication extends this idea to learned representations with long-range dependencies [@xie2021deepsc; @liu2021swin]. These systems avoid a strict separation between source and channel coding, but continuous latent representations do not automatically inherit the reliability, security, and interoperability mechanisms of standardized digital links.

## 2.2 Hybrid Digital--Analog Semantic Communication

Classical hybrid digital--analog transmission sends a protected base description digitally and an uncoded or lightly coded residual through an analog layer. HDA-DeepSC transfers this principle to a learned semantic space [@xie2025hda]. A hyper-encoder extracts the essential digital component, a hyper-decoder reconstructs its base representation, and the analog branch carries the residual. The framework also includes rate--distortion losses and diffusion-based signal refinement. The present work preserves this allocation structure and focuses on the soft information delivered to the digital channel decoder.

## 2.3 Imperfect Channel Knowledge and Mismatched Reception

Channel estimation and detection under uncertain parameters are classical estimation and communication problems [@kay1993estimation; @proakis2007digital; @goldsmith2005wireless]. A mismatched decoder evaluates its metric under an assumed channel law that differs from the true one, which can reduce achievable rates and distort reliability information [@merhav1994mismatched]. For coded systems, symbol mean-square error alone is not sufficient: the sign, scale, and calibration of the bit log-likelihood ratio directly affect iterative decoding. This motivates uncertainty-aware likelihood construction rather than equalizer replacement alone.

# 3. System Model and Reproduced Baseline

## 3.1 Hybrid Semantic Transmitter and Receiver

Let $\mathbf{I}$ denote an input image and let the semantic encoder produce

$$
\mathbf{z}=S(\mathbf{I};\boldsymbol{\alpha}_t).
$$

A digital--analog allocation module decomposes $\mathbf{z}$ into a digital component $\mathbf{z}_D$ and an analog residual $\mathbf{z}_A$:

$$
\begin{aligned}
\mathbf{z}_D &= H(\mathbf{z}),\\
\mathbf{z}_D^q &= Q(\mathbf{z}_D),\\
\mathbf{z}_A &= \mathbf{z}-H^{-1}(\mathbf{z}_D^q).
\end{aligned}
$$

The digital branch serializes the quantized integers, applies a systematic low-density parity-check code, and selects a modulation and code-rate pair using an SNR-driven adaptive table. The analog branch encodes $\mathbf{z}_A$, normalizes the transmit power, and sends the continuous symbols directly. After reception, the two estimates are fused as

$$
\widehat{\mathbf{z}}=H^{-1}(\widehat{\mathbf{z}}_D)+\widehat{\mathbf{z}}_A,
\qquad
\widehat{\mathbf{I}}=S^{-1}(\widehat{\mathbf{z}};\boldsymbol{\alpha}_r).
$$

The implementation also supports a diffusion-based analog-signal denoiser with an SNR-aware residual gate, following the general denoising-diffusion principles in [@ho2020ddpm; @nichol2021improved]. This module is held fixed in the receiver comparisons so that the measured difference is attributable to the digital soft metric.

![Reproduced HDA-DeepSC chain and imperfect-CSI receiver extension.](figures/system_architecture.png){width=6.8in}

## 3.2 Digital Link and Adaptive Modulation and Coding

The digital link uses a fixed-length 8-bit representation for each quantized feature value, a systematic low-density parity-check code of block length 672, and the operating regions below. Because the modulation order or code rate changes near 8, 12, and 16 dB, the decoded bit-error rate is not required to be globally monotonic across all nominal signal-to-noise-ratio values. Receiver comparisons must use the same signal-to-noise ratio, adaptive profile, and paired channel realization.

| Nominal SNR | Modulation | LDPC rate |
|---:|:---:|:---:|
| Below 4 dB | BPSK | 1/2 |
| 4--8 dB | QPSK | 1/2 |
| 8--12 dB | QPSK | 3/4 |
| 12--16 dB | 16-QAM | 1/2 |
| 16 dB and above | 16-QAM | 3/4 |

## 3.3 Rician Block-Fading and Channel Estimation

The current simulator uses a real-valued block-Rician coefficient shared by all symbols of one image sample:

$$
\mathbf{y}=h\mathbf{x}+\mathbf{n},
\qquad
h=\mu+\sigma w,
\quad w\sim\mathcal{N}(0,1).
$$

The Rician factor is $K=3$. This model captures sample-to-sample fading and occasional deep fades, but it does not represent complex baseband rotation, multipath delay spread, or frequency selectivity.

For pilot-aided estimation, let $\sigma_h^2$ be the channel prior variance, $E_p$ the total pilot energy, and $\sigma_n^2$ the noise variance. A linear minimum-mean-square-error estimate satisfies

$$
h=\widehat{h}+e,
\qquad
\sigma_e^2=
\frac{\sigma_h^2\sigma_n^2}
{E_p\sigma_h^2+\sigma_n^2}.
$$

A controlled additive-error mode, $\widehat{h}=h+e$, is also used to set a prescribed realized normalized mean-square error. The pilot-aided and controlled-error settings serve different purposes: the former represents a receiver procedure and overhead, whereas the latter isolates the effect of error strength.

# 4. Receiver Diagnosis and Proposed Soft Metric

## 4.1 Why Linear Equalizer Replacement Can Be Ineffective

A robust linear equalizer can be written as

$$
w_R=
\frac{P_x\widehat{h}}
{P_x(\widehat{h}^2+\sigma_e^2)+\sigma_n^2},
\qquad
\widehat{x}=w_Ry.
$$

Suppose that the soft demodulator is given the effective gain $g_{\mathrm{eff}}=w\widehat{h}$ and the filtered-noise variance $\sigma_{\mathrm{out}}^2=w^2\sigma_v^2$. For candidate symbol $s$,

$$
\frac{|wy-w\widehat{h}s|^2}{w^2\sigma_v^2}
=
\frac{|y-\widehat{h}s|^2}{\sigma_v^2}.
$$

The nonzero scalar equalizer coefficient cancels exactly. In the early diagnostic experiment, the maximum absolute decoded-bit-error-rate difference between least-squares and robust linear equalization was approximately $6.59\times10^{-4}$, and the mean absolute difference was approximately $1.82\times10^{-4}$. This result does not imply that the continuous symbol estimates are identical; it shows that a consistently normalized likelihood can erase the expected benefit at the decoder input.

## 4.2 Mismatched Baseline

With imperfect channel knowledge, the received sample can be expressed as

$$
y=\widehat{h}s+es+n.
$$

The mismatched baseline treats $\widehat{h}$ as exact and uses

$$
\mathcal{M}_B(s)
=-\frac{|y-\widehat{h}s|^2}{2\sigma_n^2}.
$$

This metric assigns one common variance to every constellation candidate and can therefore produce excessively confident log-likelihood ratios when $\sigma_e^2$ is non-negligible.

## 4.3 Uncertainty-Aware Maximum-A-Posteriori Metric

Conditioned on candidate $s$, the error term $es$ contributes variance proportional to $|s|^2$. The proposed metric is

$$
\begin{aligned}
v(s) &= \sigma_n^2+|s|^2\sigma_e^2,\\
\mathcal{M}_C(s)
&=-\frac{|y-\widehat{h}s|^2}{2v(s)}
-\frac{1}{2}\ln v(s).
\end{aligned}
$$

The second term is required by the Gaussian normalization and prevents a large-variance candidate from receiving an unjustified likelihood advantage. For coded bit $b_k$, the receiver computes

$$
L(b_k)=
\log\sum_{s\in\mathcal{S}_{k,1}}\exp[\mathcal{M}(s)]
-
\log\sum_{s\in\mathcal{S}_{k,0}}\exp[\mathcal{M}(s)],
$$

using the sign convention $L=\log P(b=1)/P(b=0)$. Exact log-sum-exp evaluation is retained instead of a max-log approximation.

The correction is modulation dependent. BPSK and QPSK are constant-modulus constellations, so $|s|^2$ is identical for every candidate and $v(s)$ becomes a common scale. Candidate ordering then changes little. In normalized 16-QAM, the real dimensions use amplitudes $\pm1/\sqrt{10}$ and $\pm3/\sqrt{10}$, so the candidate energies differ. The uncertainty term can therefore change both candidate probabilities and log-likelihood-ratio calibration.

# 5. Experimental Methodology

## 5.1 Data, Network, and Channel Configuration

Training uses DIV2K images and evaluation uses the Kodak image set. Images are randomly cropped to $128\times128$ during training. The batch size is 4, the Rician factor is 3, and the nominal evaluation SNR values are 0, 2, ..., 18 dB. The semantic encoder and decoder use a Swin-Transformer-style hierarchy [@liu2021swin]. The digital branch uses 8-bit scalar quantization, the adaptive modulation and coding configurations listed above, and exact soft demodulation. The analog branch and diffusion denoiser remain identical in every paired receiver comparison.

## 5.2 Paired Receiver Protocol

All compared groups load the same learned checkpoint. Before every forward pass, the random state is restored so that groups B and C observe the same transmitted image, true fading coefficient, thermal noise, and channel-estimation error. This paired design avoids the confounding that occurs when separately trained semantic encoders are compared as though their output difference were caused only by the receiver.

| Group | Channel knowledge | Digital receiver |
|:---:|:---:|:---|
| A | Perfect | Matched soft demodulation |
| B | Imperfect | Mismatched metric that ignores estimation uncertainty |
| C | Same as B | Candidate-dependent uncertainty-aware metric |

## 5.3 Metrics and Statistical Interpretation

The principal communication metric is decoded bit-error rate. Image quality is measured primarily by peak signal-to-noise ratio, with multi-scale structural similarity, visual-information fidelity, learned perceptual image-patch similarity, and Fréchet Inception distance available for broader evaluation [@wang2003msssim; @sheikh2006vif; @zhang2018lpips; @heusel2017fid]. Fréchet Inception distance is a distribution-level metric and is not interpreted from a single image.

The implementation also records packet error rate and frame error rate for packet-level reliability studies. A semantic information packet contains 256 information bits, corresponding to 32 fixed-length 8-bit quantized values. A packet is erroneous if at least one decoded information bit differs, while a frame is erroneous if at least one information bit in a low-density parity-check information block differs. These diagnostics are distinct from any artificial post-decoding semantic-feature erasure used in later recovery experiments.

For the paired comparison,

$$
\Delta\mathrm{BER}=\mathrm{BER}_B-\mathrm{BER}_C,
\qquad
\Delta\mathrm{PSNR}=\mathrm{PSNR}_C-\mathrm{PSNR}_B.
$$

Positive values favor the uncertainty-aware receiver. Confidence intervals should be obtained by paired bootstrap resampling over common image/channel realizations. The controlled results below report aggregate means from the available study; camera-ready system-level claims should additionally include at least 30 Monte Carlo repetitions and 95% confidence intervals at each signal-to-noise ratio.

# 6. Results and Discussion

## 6.1 Controlled Channel-Estimation Error

The table below summarizes the average results in the 16-QAM operating region. At normalized mean-square-error values of 0.1, 0.2, and 0.5, the uncertainty-aware metric reduces decoded bit-error rate by 0.009557, 0.016187, and 0.022957, respectively. The corresponding average peak-signal-to-noise-ratio gains are 1.040, 1.445, and 1.058 dB. The largest average bit-error-rate reduction occurs at normalized mean-square error 0.5, while the largest average image-quality gain occurs at normalized mean-square error 0.2.

| Target NMSE | Average BER reduction | Average PSNR gain (dB) |
|---:|---:|---:|
| 0.10 | 0.009557 | 1.040 |
| 0.20 | 0.016187 | 1.445 |
| 0.50 | 0.022957 | 1.058 |
| 1.00 | 0.019637 | 0.022 |

![Aggregate controlled channel-estimation-error results.](figures/controlled_nmse_results.png){width=6.5in}

The result at normalized mean-square error 1.0 is an important boundary case. The average bit-error-rate reduction remains positive, but the mean peak-signal-to-noise-ratio gain falls to 0.022 dB. One reason is that ordinary bit-error rate weights all bit positions equally, whereas an error in a high-order bit of an 8-bit quantized feature can be far more destructive than an error in a low-order bit. A second reason is that the HDA fusion stage adds the recovered digital base representation to the analog residual, so a small number of severe digital-feature errors can contaminate the final semantic latent. The observation supports using both link-level and end-to-end metrics.

## 6.2 Modulation and Adaptive-Mode Dependence

Under perfect channel knowledge, the exact likelihood and the earlier soft-demodulation implementation are nearly identical in the QPSK region. Differences appear mainly at 12--18 dB, where 16-QAM is selected. At 12, 14, 16, and 18 dB, the measured absolute bit-error-rate reductions were approximately 0.00422, 0.00439, 0.00247, and 0.00190, respectively. These perfect-knowledge differences reflect likelihood implementation and noise-variance scaling rather than robustness to estimation error.

The original adaptive modulation and coding table changes code rate or modulation near 8, 12, and 16 dB. A local increase in bit-error rate at a switching point is therefore consistent with reduced redundancy or a denser constellation and should not be interpreted as a broken SNR trend. The appropriate comparison is the paired difference between receivers under the same profile.

## 6.3 Reproducibility, Limitations, and Next Experiments

The controlled-error study isolates the mechanism but does not include pilot overhead. A full receiver evaluation should report pilot-limited cases, such as one and four pilot symbols, on at least two independently trained checkpoints. It should verify that groups B and C have the same realized channel-estimation normalized mean-square error and effective signal-to-noise ratio, and should report decoded bit-error rate, packet error rate, frame error rate, soft-information cross-entropy, digital-feature mean-square error, peak signal-to-noise ratio, and perceptual image metrics with paired confidence intervals.

The present channel is real-valued, block flat, and single-input single-output. Extension to complex baseband, orthogonal frequency-division multiplexing, frequency-selective fading, carrier offsets, and multiple antennas is required before engineering deployment claims can be made. A further direction is reliability-aware HDA fusion: parity checks, packet-error indicators, average absolute log-likelihood ratio, and effective signal-to-noise ratio can be used to attenuate unreliable digital features rather than adding them to the analog residual with a fixed coefficient. Controlled semantic-feature erasure and mask-conditioned recovery provide a natural test bed for this extension, but no recovery gain is claimed in the present paper.

# 7. Conclusion

This paper reproduced an HDA-DeepSC image-transmission chain and extended its digital receiver to imperfect channel knowledge. The analysis showed that a linear robust equalizer does not automatically improve coded performance when the soft demodulator consistently accounts for residual gain and filtered-noise variance, because the scalar equalizer coefficient cancels from the normalized likelihood distance. The proposed received-domain metric instead incorporates estimation uncertainty through a candidate-dependent variance and Gaussian normalization term. Controlled experiments support decoded-bit-error-rate and end-to-end peak-signal-to-noise-ratio improvements for nonconstant-modulus 16-QAM under moderate estimation error, while constant-modulus operation and very severe uncertainty show limited or inconsistent image-level gains. The central implication is that robust semantic reception should optimize the reliability of the soft information delivered to the channel decoder, not only the mean-square error of the equalized symbols.

# References
