# Prediction and learning

Use when the target is performance on new observations or when features and model
complexity are selected from data. Define the prediction time, available inputs,
outcome, target population and intended use before choosing an algorithm.

## Match model complexity to the information

| Candidate | Useful starting point | Main choice to validate |
|---|---|---|
| Simple regression or clinically meaningful rule | A baseline with interpretable inputs | Functional form, inputs available at prediction time |
| Ridge, lasso or elastic net | Many or correlated predictors | Scaling and penalty; stability of selected variables |
| Decision tree | An explicit sequence of decision rules | Depth, minimum leaf size and pruning |
| Bagging or random forest | Nonlinearities and interactions | Tree complexity, candidate features and stable performance |
| SVM or k-nearest neighbors | A suitable separating boundary or neighborhood | Scaling, C/kernel or k; irrelevant dimensions |
| Neural network | Adequate information for a flexible nonlinear model | Capacity, regularization, learning and stopping choices |
| Convolutional network | Local structure in images, sequences or ordered signals | Encoding, receptive field, padding and required location precision |

Compare a meaningful simple model and a naive baseline using the same held-out
observations and metrics. Model size, more features or a larger training fit do not
establish better generalization. Use learning curves to distinguish an information
limit from model or measurement limits. Choose inputs from what will be available
at deployment. A selected feature's predictive contribution requires a separate
biological argument before it becomes a mechanistic claim.

## Separate fitting, selection and evaluation

Fit on training data, select the model and threshold on validation data, and
evaluate on an untouched test set. With limited data, use suitable nested
resampling: selection stays within the training portion of each outer split.
Choose the split structure for the intended generalization, not a fixed percentage.

- Keep records from an independent subject together. Use time or site separation
  when predicting future periods or new centers is the intended use.
- Learn scaling, imputation, PCA, feature selection, sampling and tuning inside
  training folds. Apply the learned steps to held-out observations.
- Keep the test set representative of the deployment setting. Class weights,
  undersampling, oversampling and synthetic examples are training choices.
  Repeated or synthetic observations do not increase independent sample size.
- Preserve split IDs and held-out predictions. Fold scores share training data;
  use an uncertainty method suited to the evaluation design.
- A final refit can use the development data after choices are fixed. Its training
  fit is not an additional performance estimate. State which development procedure
  the held-out estimate evaluates.

Out-of-bag evaluation is useful internal information for tree ensembles. Assess
whether preprocessing and tuning have already used those observations; OOB alone
does not evaluate transport to a new site or time. Assess calibration when the
output is a probability, as well as discrimination and error costs. For binary
outcomes, read [diagnostic evaluation](binary-and-diagnostic.md#evaluate-a-diagnostic-test).

## Examine what drives the result

Report performance and uncertainty at the intended operating point, class counts,
the comparator and relevant subgroups. For rare outcomes, the actual number of
independent positives limits precision. A large imbalance ratio alone does not
dictate a sampling strategy. Reassess probabilities after changing training class
proportions or weights, using representative validation data.

Check stability across plausible splits and important design groups. Correlated
predictors can exchange importance or lasso membership. Record selection when
reporting coefficients; ordinary preselection P values and intervals do not
automatically account for it. Use primary method documentation for selective
inference, model explanation or a specialized architecture when needed.

Deliver the pipeline, trained object, splits, held-out predictions, baseline
comparison and uncertainty. Keep inference about biological effects in the
design-appropriate analysis, with a clear link to the prediction finding.

## Sources

- *Model selection and overfitting*, pp. 703–704: [nmeth.3968](https://doi.org/10.1038/nmeth.3968).
- *Regularization*, pp. 803–804: [nmeth.4014](https://doi.org/10.1038/nmeth.4014).
- *Classification and regression trees*, pp. 757–758, with correction: [nmeth.4370](https://doi.org/10.1038/nmeth.4370).
- *Ensemble methods: bagging and random forests*, pp. 933–934: [nmeth.4438](https://doi.org/10.1038/nmeth.4438).
- *Machine learning: a primer*, pp. 1119–1120: [nmeth.4526](https://doi.org/10.1038/nmeth.4526).
- *Machine learning: supervised methods*, pp. 5–6: [nmeth.4551](https://doi.org/10.1038/nmeth.4551).
- *Statistics versus machine learning*, pp. 233–234: [nmeth.4642](https://doi.org/10.1038/nmeth.4642).
- *The curse(s) of dimensionality*, pp. 399–400: [s41592-018-0019-x](https://doi.org/10.1038/s41592-018-0019-x).
- *The class imbalance problem*, pp. 1270–1272: [s41592-021-01302-4](https://doi.org/10.1038/s41592-021-01302-4).
- *Neural networks primer*, pp. 165–167: [s41592-022-01747-1](https://doi.org/10.1038/s41592-022-01747-1).
- *Convolutional neural networks*, pp. 1269–1270: [s41592-023-01973-1](https://doi.org/10.1038/s41592-023-01973-1).
- *Comparing classifier performance with baselines*, pp. 546–548: [s41592-024-02234-5](https://doi.org/10.1038/s41592-024-02234-5).

Leakage, clustered splits and deployment checks are the suite's implementation of
the separation and generalization principles. Verify model-specific software choices.
