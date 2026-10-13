# Biomedical suite

When drafting, revising or reviewing biomedical prose, read
[the author's writing principles](skills/biomed-shared/writing-principles.md).
That file is the governing source for scientific interest, biological significance
and preservation of scientific ambition.

When changing skill responsibilities, triggers or shared references, use
[the task boundaries](docs/writing-architecture.md). Put common rules in their
shared file and task-specific actions in the responsible entry point.

After writing-package edits, run `python3 scripts/check_writing.py --integration`
and `python3 -m unittest discover -s tests -v`. These check package structure;
use `tests/writing-cases.json` for separate agent behavior evaluation.
