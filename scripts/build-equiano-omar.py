#!/usr/bin/env python3
"""Build the reviewed Equiano / Omar ibn Said comparison."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'frst-110-resources/equiano-omar-assets'
def render():
    text = (ASSETS / 'page.template.html').read_text()
    for token, name in [('COMPARISON','comparison.fragment.html'), ('OMAR_IMAGE','images/visual.fragment.html')]:
        text = text.replace('{{' + token + '}}', (ASSETS / name).read_text())
    return text
if __name__ == '__main__':
    target = ROOT / 'frst-110-resources/equiano-and-omar-ibn-said.html'
    target.write_text(render())
    print(target)
