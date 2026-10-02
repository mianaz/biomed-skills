# Imaging acquisition and reference standards

## Acquisition and geometry

Record modality, anatomy, contrast/tracer/stain, device/vendor/model, site, protocol,
reconstruction, dimensions, spacing, orientation, slice thickness, field of view,
bit depth/intensity transform, compression, and acquisition time when they affect use.

For DICOM, NIfTI, whole-slide, microscopy, video, or derived images, preserve stable
patient/specimen, study, series/slide, and instance/region hierarchy after approved
de-identification. Validate geometry and image-mask/annotation alignment after every
conversion, resampling, registration, or crop.

Document exclusions for motion, artifacts, incomplete coverage, protocol deviation,
corruption, and poor quality. Keep excluded and failed cases in cohort accounting.

## Reference standard

Specify whether labels come from pathology, clinical follow-up, laboratory testing,
expert readers, consensus/adjudication, report extraction, registry fields, or another
model. Record reader number, expertise, blinding, instructions, tools, access to other
information, repeat reads, adjudication, and uncertainty or indeterminate labels.

Check:

- spectrum of disease and normal/negative cases;
- partial or differential verification;
- incorporation of the index model/image feature into the reference;
- time interval and treatment between image and reference;
- inter/intra-reader variability;
- label provenance at patient, exam, lesion, image, or pixel level;
- whether missing or indeterminate references are outcome-dependent.

Do not call a noisy single-reader annotation ground truth without qualification.

## External validation

Describe which axis differs from development: institution, geography, time, device,
protocol, prevalence, referral pathway, population, disease severity, workflow, or
reader practice. Report overlap checks for participants, public datasets, repeated
exams, image derivatives, and annotations.
