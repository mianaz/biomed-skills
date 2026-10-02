# Cross-species integration

Cross-species similarity depends on orthology, developmental alignment, and the
presence of comparable cell states. Gene-symbol capitalization is not orthology.

## Prepare features

1. Record species, genome builds, annotation releases, and the orthology resource
   release.
2. Prefer one-to-one orthologs for direct expression alignment. Resolve duplicated
   mappings explicitly and retain the full species-specific objects.
3. Select variable or informative features within species, then construct the shared
   feature universe. Do not let one species' annotation depth determine it alone.
4. Check whether age, developmental stage, tissue compartment, and dissociation mode
   are biologically comparable.

## Map without forcing matches

- Integrate or anchor at a coarse lineage level before fine subtypes.
- Use reciprocal mapping or held-out known populations to estimate mapping quality.
- Include a no-match gate. Calibrate its similarity, posterior, or reconstruction
  threshold on positive and negative controls; a value such as 0.6 from one study is
  an example, not a portable default.
- Retain species-specific or stage-specific populations as unmatched when evidence
  supports that conclusion.
- Report mapping direction. Reference-to-query performance is directional even
  though agreement statistics on the same cell labels are not.

Validate mapped identities with species-appropriate markers and inspect whether
apparent differences reflect one-to-many orthologs, missing features, or stage
offsets rather than cell biology.
