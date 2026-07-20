# IEEE Submission Checklist and Revision Notes

## Completed in this revision

- Replaced the Chinese `ctexart` single-column document with `IEEEtran` conference mode.
- Rewrote the manuscript as an English conference paper rather than placing Chinese and English abstracts in one submission file.
- Reduced the title to a technical, searchable statement of the method and problem.
- Rewrote the abstract as one self-contained paragraph and limited the keyword list to five terms.
- Reorganized the paper into Introduction, Related Work, System Model, Receiver Method, Experimental Methodology, Results and Discussion, and Conclusion.
- Converted implementation history into reproducible methodology and removed diary-like or thesis-only material.
- Added an explicit paired-comparison protocol to separate receiver effects from checkpoint differences.
- Preserved the exact controlled-NMSE aggregate values reported in the source manuscript.
- Restricted the claims to nonconstant-modulus 16-QAM and moderate channel-estimation error, where the evidence is strongest.
- Added explicit negative and boundary results, including the weak image-level gain at NMSE 1.0.
- Added packet error rate and frame error rate definitions without claiming unmeasured recovery improvements.
- Corrected the HDA-DeepSC reference to IEEE JSAC, vol. 43, no. 7, pp. 2478--2492, July 2025, DOI 10.1109/JSAC.2025.3559149.
- Added reproducible vector/PDF figure generation and an editable Word-source manuscript.

## Required before submission

- [ ] Replace `First Author, Second Author` with the complete author list.
- [ ] Replace department, institution, city/country, and email placeholders.
- [ ] Check whether the target conference requires anonymous review; remove or restore author metadata accordingly.
- [ ] Add a funding acknowledgment only when one applies.
- [ ] Check the target conference's exact page limit, reference policy, and overlength fees.
- [ ] Add the conference-specific copyright notice or footer only when instructed by the conference.
- [ ] Insert the submission identifier only when the submission system requests it.
- [ ] Confirm whether the target venue permits arXiv or other preprints.
- [ ] Verify every numerical claim against the final CSV or experiment log.
- [ ] Run at least 30 paired Monte Carlo repetitions per SNR for the main system-level experiment.
- [ ] Report 95% paired confidence intervals for BER and PSNR differences.
- [ ] Repeat the paired experiment with at least two independently trained checkpoints.
- [ ] Add pilot-limited results for one and four pilot symbols if they are part of the final claim.
- [ ] Verify that paired groups have the same realized CSI NMSE and effective SNR.
- [ ] Add reconstruction examples only from the actual evaluation set; do not use the Lena image.
- [ ] Compute FID only from image sets, not from one image.
- [ ] Check that figures remain legible when printed in grayscale and at one-column width.
- [ ] Confirm that all figure labels and text use embedded or subset fonts.
- [ ] Remove any unused figures, tables, source comments, and temporary files from the final upload.
- [ ] Run IEEE PDF eXpress or the conference's equivalent validation service.
- [ ] Check that the final PDF has no security settings, bookmarks, attachments, crop marks, or external hyperlinks unless the venue explicitly permits them.
- [ ] Proofread the final title, author order, affiliations, abstract, and references in the submission portal as well as in the PDF.

## Result integrity notes

The generated aggregate figure contains only these reported values:

| Target CSI NMSE | Average BER reduction | Average PSNR gain (dB) |
|---:|---:|---:|
| 0.10 | 0.009557 | 1.040 |
| 0.20 | 0.016187 | 1.445 |
| 0.50 | 0.022957 | 1.058 |
| 1.00 | 0.019637 | 0.022 |

No per-SNR values, standard deviations, confidence intervals, or recovery gains are synthesized by the figure-generation script.

## Relationship to the current software extension

The software project now records BER, PER, and FER and supports natural channel loss, physical-layer LLR erasure, post-decoding semantic-feature erasure, and independent natural-plus-artificial semantic loss. These additions are suitable for a follow-up recovery study. They are not presented as completed performance improvements in the current conference manuscript because the required controlled experiments and paired statistical results have not yet been supplied.
