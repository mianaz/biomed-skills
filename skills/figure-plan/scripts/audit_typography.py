"""Effective type from source sizes, placement and final manuscript scaling."""
import argparse
import json
from pathlib import Path


def audit_figure(figure, floor=10, target=11, spread=1.2):
    final_scale = figure['manuscript_width_mm'] / figure['export_width_mm']
    rows, unknown, coverage, small, large = [], [], [], [], []
    by_role = {}
    for panel in figure['panels']:
        scale = panel['placed_width_mm'] / panel['source_width_mm'] * final_scale
        profiles = panel.get('role_profiles', {})
        if not profiles:
            unknown.append(panel['id'])
        if panel.get('text_coverage') != 'complete':
            coverage.append(panel['id'])
        for role, profile in profiles.items():
            row = dict(panel=panel['id'], role=role, scale=scale,
                       **{k: profile[k] * scale for k in ['min', 'q10', 'median', 'max']})
            rows.append(row)
            if role not in ['label', 'numeric']:
                continue
            by_role.setdefault(role, []).append(row['median'])
            if row['min'] <= floor:
                small.append(dict(panel=panel['id'], role=role, pt=row['min']))
            if row['median'] > target * spread:
                large.append(dict(panel=panel['id'], role=role, pt=row['median']))
    ratios = {role: max(values) / min(values) for role, values in by_role.items()}
    inconsistent = {role: value for role, value in ratios.items() if value > spread}
    letters = figure.get('letter_pt', 11) * final_scale
    native_pass = not (small or large or inconsistent or unknown) and letters > floor
    return dict(figure=figure['id'], manuscript_scale=final_scale, letter_pt=letters,
                floor_exclusive_pt=floor, target_pt=target, median_upper_pt=target * spread,
                same_role_max_ratio=spread, rows=rows, role_ratios=ratios,
                small=small, large=large, inconsistent=inconsistent,
                unknown_panels=unknown, coverage_unverified=coverage,
                native_measurements_pass=native_pass,
                complete_typography_pass=native_pass and not coverage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--floor', type=float, default=10, help='Exclusive ordinary-text floor in pt')
    parser.add_argument('--target', type=float, default=11)
    parser.add_argument('--max-ratio', type=float, default=1.2)
    args = parser.parse_args()
    figures = json.loads(args.manifest.read_text())
    args.output.write_text(json.dumps([audit_figure(f, args.floor, args.target, args.max_ratio)
                                     for f in figures], indent=2) + '\n')
