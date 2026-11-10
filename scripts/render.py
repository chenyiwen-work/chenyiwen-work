from pathlib import Path
from html import escape
import argparse

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'dark': dict(bg='#0d1117', panel='#151b23', border='#303b46', text='#e6edf3', muted='#8594a6', accent='#79e2ba', portrait='#aebcc9', tag='#1c302d'),
    'light': dict(bg='#ffffff', panel='#f6f8fa', border='#d1d9e0', text='#1f2937', muted='#64748b', accent='#176b52', portrait='#4b6073', tag='#e6f2ec'),
}


def text(x, y, value, color, size=14, **attrs):
    extra = ' '.join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(value)}</text>'


def render(theme):
    c = PALETTES[theme]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="650" viewBox="0 0 1120 650" role="img" aria-labelledby="title desc">',
           '<title id="title">chenyiwen-work — ASCII terminal profile</title>',
           '<desc id="desc">An ASCII rendering of my GitHub avatar beside a terminal-style introduction. Exploring AI agents, model gateways and developer tools.</desc>',
           '<style>text{font-family:Consolas,"Liberation Mono",Menlo,monospace;white-space:pre}.cursor{animation:blink 1.2s step-end infinite}@keyframes blink{50%{opacity:0}}@media(prefers-reduced-motion:reduce){.cursor{animation:none}}</style>',
           f'<rect x="0.5" y="0.5" width="1119" height="649" rx="16" fill="{c["panel"]}" stroke="{c["border"]}"/>',
           f'<path d="M1 57H1119" stroke="{c["border"]}"/>']
    for i, color in enumerate(['#ed6a5e', '#f4bf50', '#61c454']):
        out.append(f'<circle cx="{29+i*20}" cy="29" r="5" fill="{color}"/>')
    out += [text(104, 34, '~/chenyiwen-work', c['muted'], 13), text(1090, 34, 'PROFILE.SH', c['muted'], 11, text_anchor='end'),
            text(32, 94, '$ whoami --ascii', c['accent'], 13), text(32, 595, 'CHENYIWEN / WORK IN PROGRESS', c['muted'], 11),
            f'<path d="M495 99V565" stroke="{c["border"]}" stroke-dasharray="3 7"/>']
    rows = (ROOT / 'assets' / 'portrait.txt').read_text(encoding='utf-8').splitlines()
    for i, row in enumerate(rows):
        # Higher density characters retain the bright hair and hands of the avatar.
        out.append(text(28, 125 + i * 10.8, row, c['portrait'], 11, textLength=len(row)*6.65, lengthAdjust='spacingAndGlyphs'))
    out += [text(532, 135, 'chenyiwen@github', c['accent'], 25, font_weight='700'),
            text(532, 165, 'Building tools for the agent era.', c['text'], 14),
            text(532, 193, '-----------------------------------------------', c['border'], 15)]
    fields = [
        ('Handle', '@chenyiwen-work'),
        ('Focus', 'AI agents / developer tools'),
        ('Workspace', 'Go / TypeScript / Python'),
        ('Environment', 'Windows / WSL / Linux'),
    ]
    for i, (key, value) in enumerate(fields):
        y = 226 + i * 29
        out.extend([text(532, y, key, c['accent'], 14), text(663, y, ':', c['muted'], 14), text(686, y, value, c['text'], 14)])
    out += [text(532, 370, '$ ls interests/', c['accent'], 13)]
    interest_rows = [
        ('01', 'Agent runtimes & sandboxes'),
        ('02', 'Model gateways & orchestration'),
        ('03', 'Reactive notebooks & automation'),
    ]
    for i, (index, value) in enumerate(interest_rows):
        y = 402 + i * 29
        out += [text(532, y, index, c['muted'], 12), text(568, y, value, c['text'], 14)]
    out += [text(532, 510, '$ cat mindset.txt', c['accent'], 13), text(532, 540, 'Stay curious. Make it work. Keep iterating.', c['text'], 13),
            f'<path d="M28 615H1092" stroke="{c["border"]}"/>', text(32, 637, '~/chenyiwen-work', c['muted'], 11),
            text(1090, 637, 'EOF', c['accent'], 11, text_anchor='end'), text(532, 589, '> ', c['accent'], 15),
            f'<rect class="cursor" x="554" y="576" width="8" height="16" rx="1" fill="{c["accent"]}"/>', '</svg>']
    return '\n'.join(out) + '\n'


def button(theme, index, label, detail):
    c = PALETTES[theme]
    return '\n'.join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="82" viewBox="0 0 360 82">',
        f'<rect x=".5" y=".5" width="359" height="81" rx="10" fill="{c["panel"]}" stroke="{c["border"]}"/>',
        '<style>text{font-family:Consolas,"Liberation Mono",Menlo,monospace}</style>',
        text(18, 27, index, c['accent'], 11), text(18, 52, label, c['text'], 16, font_weight='700'),
        text(342, 27, detail, c['muted'], 10, text_anchor='end'), text(342, 55, '->', c['accent'], 20, text_anchor='end'), '</svg>', ''])


def main():
    parser = argparse.ArgumentParser(description='Render self-contained GitHub profile SVGs from the committed ASCII portrait.')
    parser.parse_args()
    assets = ROOT / 'assets'
    for theme in PALETTES:
        (assets / f'profile-{theme}.svg').write_text(render(theme), encoding='utf-8', newline='\n')
        for slug, index, label, detail in [('repositories', '01', 'Repositories', 'EXPLORE'), ('activity', '02', 'Recent activity', 'FOLLOW'), ('stars', '03', 'Starred projects', 'DISCOVER')]:
            (assets / f'{slug}-{theme}.svg').write_text(button(theme, index, label, detail), encoding='utf-8', newline='\n')
    print('Rendered 8 self-contained SVG assets.')


if __name__ == '__main__':
    main()
