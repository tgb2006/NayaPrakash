"""Check the project glossary in current publication text."""

import argparse
from collections import Counter
from pathlib import Path
import re


OUTPUT = Path(__file__).resolve().parents[1] / 'output'
RULES = (
    (re.compile('મુક્તત્ત્વ'), 'મુક્તત્વ'),
    (re.compile('શાશ્વતત્ત્વ'), 'શાશ્વતત્વ'),
    (re.compile('મૂર્તત્ત્વ'), 'મૂર્તત્વ'),
    (re.compile('નિમિત્તત્ત્વ'), 'નિમિત્તત્વ'),
    # Keep the grammatical suffix -ત્વ in independent abstract nouns.
    (re.compile(r'(?<!ત્)(?<!શાશ્વ)(?<!મૂર્)(?<!મુક્)તત્વ'), 'તત્ત્વ'),
    (re.compile(r'સ[તદ]ગુર[ુૂ]|સદ્ગુરુ'), 'સદ્ગુરૂ'),
    (re.compile('મહત્વ'), 'મહત્ત્વ'),
    (re.compile(r'સાક્ષાત(?!્)'), 'સાક્ષાત્'),
    (re.compile('તાત્વિક'), 'તાત્ત્વિક'),
    (re.compile('દુખ'), 'દુઃખ'),
    (re.compile('મૂર્છા'), 'મૂર્ચ્છા'),
)


def publication_paths():
    groups = ('khanda_*', 'preface', 'samanya_prakaran', 'parishishta', 'compiled')
    return sorted(path for group in groups for path in OUTPUT.glob(f'{group}/*.md'))


def corrections(text):
    for pattern, replacement in RULES:
        for match in pattern.finditer(text):
            yield match, replacement


def require_clean(paths):
    errors = []
    for path in paths:
        text = path.read_bytes().decode('utf-8')
        for match, replacement in corrections(text):
            line = text.count('\n', 0, match.start()) + 1
            errors.append(f'{path}:{line}: {match[0]} → {replacement}')
    if errors:
        raise SystemExit('\n'.join(errors) + f'\nGujarati spelling issues: {len(errors)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fix', action='store_true')
    parser.add_argument('--backup', type=Path)
    args = parser.parse_args()
    if args.fix and not args.backup:
        parser.error('--fix requires a new --backup directory')
    paths = publication_paths()
    if args.fix:
        args.backup.mkdir(parents=True, exist_ok=False)
        totals = Counter()
        changed = 0
        for path in paths:
            original = path.read_bytes()
            text = original.decode('utf-8')
            for pattern, replacement in RULES:
                text, count = pattern.subn(replacement, text)
                totals[replacement] += count
            if text.encode('utf-8') != original:
                backup = args.backup / path.relative_to(OUTPUT)
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_bytes(original)
                path.write_bytes(text.encode('utf-8'))
                changed += 1
        print(f'Files corrected: {changed}. Substitutions: {dict(totals)}')
    require_clean(paths)
    print(f'Gujarati spelling check passed for {len(paths)} files')


if __name__ == '__main__':
    main()
