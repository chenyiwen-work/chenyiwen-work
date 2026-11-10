from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'dark': dict(text='#e6edf3', muted='#8594a6', accent='#79e2ba', portrait='#aebcc9', track='#263b38'),
    'light': dict(text='#1f2937', muted='#64748b', accent='#176b52', portrait='#4b6073', track='#cddfd7'),
}
STYLE = '''<style>text{font-family:Consolas,"Liberation Mono",Menlo,monospace;white-space:pre}.blink{animation:blink 1.2s step-end infinite}.scan{animation:scan 12s linear infinite}.runner{animation:run 12s linear infinite}.pulse{animation:pulse 12s ease-in-out infinite}.arrow{animation:nudge 3s ease-in-out infinite}@keyframes blink{50%{opacity:0}}@keyframes scan{0%,8%{transform:translateY(-470px);opacity:0}10%{opacity:.8}42%{transform:translateY(470px);opacity:.8}44%,100%{transform:translateY(470px);opacity:0}}@keyframes run{0%,10%{transform:translateX(0)}30%,35%{transform:translateX(300px)}55%,60%{transform:translateX(600px)}80%,95%{transform:translateX(900px)}100%{transform:translateX(0)}}@keyframes pulse{0%,20%,100%{opacity:.25}30%,60%{opacity:1}80%{opacity:.25}}@keyframes nudge{0%,70%,100%{transform:translateX(0)}80%{transform:translateX(5px)}}@media(prefers-reduced-motion:reduce){.blink,.scan,.runner,.pulse,.arrow{animation:none}.scan{display:none}}</style>'''


def text(x,y,value,color,size=14,**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{escape(str(v),quote=True)}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(value)}</text>'


def svg(width,height,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>',STYLE]


def render(theme):
    c=PALETTES[theme]
    out=svg(1120,540,'chenyiwen-work — ASCII avatar, AI agents and developer tools')
    rows=(ROOT/'assets/portrait.txt').read_text(encoding='utf-8').splitlines()
    portrait=''.join(text(20,40+i*10.8,row,c['portrait'],11,textLength=f'{len(row)*6.65:.2f}',lengthAdjust='spacingAndGlyphs') for i,row in enumerate(rows) if row)
    highlight=portrait.replace(c['portrait'],c['accent'])
    out += ['<defs><clipPath id="portrait-window"><rect x="16" y="20" width="450" height="465"/></clipPath><clipPath id="scan-band"><rect class="scan" x="16" y="20" width="450" height="40"/></clipPath></defs>',portrait,
            f'<g clip-path="url(#portrait-window)"><g clip-path="url(#scan-band)">{highlight}</g></g>',
            text(520,48,'chenyiwen@github',c['accent'],25,font_weight='700'),text(520,78,'Building tools for the agent era.',c['text']),
            text(520,109,'-----------------------------------------------',c['muted'],14)]
    fields=[('Handle','@chenyiwen-work'),('Focus','AI agents / developer tools'),('Workspace','Go / TypeScript / Python'),('Environment','Windows / WSL / Linux')]
    for i,(key,value) in enumerate(fields):
        y=143+i*29
        out += [text(520,y,key,c['accent']),text(652,y,':',c['muted']),text(675,y,value,c['text'])]
    out += [text(520,286,'$ ls interests/',c['accent'],13)]
    for i,value in enumerate(['Agent runtimes & sandboxes','Model gateways & orchestration','Reactive notebooks & automation']):
        out += [text(520,317+i*29,f'0{i+1}',c['muted'],12),text(556,317+i*29,value,c['text'])]
    out += [text(520,425,'$ cat mindset.txt',c['accent'],13),text(520,455,'Stay curious. Make it work. Keep iterating.',c['text'],13),
            text(520,505,'>',c['accent'],15),f'<rect class="blink" x="542" y="492" width="8" height="16" fill="{c["accent"]}"/>','</svg>']
    return '\n'.join(out)+'\n'


def button(theme,index,label,detail):
    c=PALETTES[theme]
    out=svg(360,60,label)
    out += [text(18,35,index,c['accent'],12),text(55,35,label,c['text'],16),f'<g class="arrow">{text(320,35,"->",c["accent"],18)}</g>','</svg>']
    return '\n'.join(out)+'\n'


def agent(theme):
    c=PALETTES[theme]
    out=svg(1120,190,'Agent loop — a decorative pixel agent moves from task to reasoning, tools and output; not a contribution chart')
    out += [text(20,26,'$ agent.run()',c['accent'],14),text(1090,26,'TASK / REASON / ACT / RETURN',c['muted'],11,text_anchor='end'),
            f'<path d="M100 99H1000" fill="none" stroke="{c["track"]}" stroke-width="2" stroke-dasharray="3 9"/>']
    for i,(label,sub) in enumerate([('TASK','understand'),('REASON','plan'),('TOOLS','execute'),('OUTPUT','iterate')]):
        x=100+300*i
        out += [f'<circle cx="{x}" cy="99" r="4" fill="{c["accent"]}"/>',text(x,143,label,c['text'],13,text_anchor='middle'),text(x,165,sub,c['muted'],11,text_anchor='middle')]
    # An original 9 x 7 pixel robot, with an independent blinking eye layer.
    pixels=['..#####..','.#######.','##.###.##','#########','.#######.','..#...#..','.##...##.']
    path=''.join(f'M{100+(x-4)*3} {73+y*3}h3v3h-3z' for y,row in enumerate(pixels) for x,ch in enumerate(row) if ch=='#')
    out += [f'<g class="runner" fill="{c["accent"]}" shape-rendering="crispEdges"><path d="{path}"/><g class="blink"><rect x="94" y="79" width="3" height="3"/><rect x="106" y="79" width="3" height="3"/></g></g>','</svg>']
    return '\n'.join(out)+'\n'


def main():
    assets=ROOT/'assets'
    for theme in PALETTES:
        (assets/f'profile-{theme}.svg').write_text(render(theme),encoding='utf-8',newline='\n')
        (assets/f'agent-loop-{theme}.svg').write_text(agent(theme),encoding='utf-8',newline='\n')
        for slug,index,label in [('repositories','01','Repositories'),('activity','02','Recent activity'),('stars','03','Starred projects')]:
            (assets/f'{slug}-{theme}.svg').write_text(button(theme,index,label,''),encoding='utf-8',newline='\n')
    print('Rendered 10 transparent, borderless SVG assets with reduced-motion support.')


if __name__=='__main__':
    main()
