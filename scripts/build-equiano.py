#!/usr/bin/env python3
"""Build the student-facing Equiano page from its reviewed source fragments."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'frst-110-resources/equiano-assets'

def render():
    template = (ASSETS / 'page.template.html').read_text()
    visuals = (ASSETS / 'images/visuals.fragment.html').read_text()
    portraits, ship = visuals.split('<figure class="brookes-figure">', 1)
    return (template.replace('{{CHAPTERS}}', (ASSETS / 'chapters.fragment.html').read_text())
            .replace('{{PORTRAITS}}', portraits)
            .replace('{{SHIP}}', '<figure class="brookes-figure">' + ship))

if __name__ == '__main__':
    target = ROOT / 'frst-110-resources/equiano-chapters-1-2.html'
    target.write_text(render())
    print(target)
