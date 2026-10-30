#!/usr/bin/env python3
"""Build the reviewed chapters III–IV student resource."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'frst-110-resources/equiano-3-4-assets'
def render():
    text = (ASSETS / 'page.template.html').read_text()
    for token, name in [('MAPS','maps.fragment.html'), ('CHAPTERS','chapters.fragment.html'), ('IMAGES','images.fragment.html')]:
        text = text.replace('{{' + token + '}}', (ASSETS / name).read_text())
    return text
if __name__ == '__main__':
    target = ROOT / 'frst-110-resources/equiano-chapters-3-4.html'
    target.write_text(render())
    print(target)
