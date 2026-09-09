"""Generate linked monochrome README artwork using only GitHub-supported images."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'profile'
OUT.mkdir(exist_ok=True)
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"


def write(name, width, height, draw):
    for theme in ('light', 'dark'):
        c = dict(bg='#ffffff', fg='#111111', muted='#666666', line='#dddddd') if theme == 'light' else dict(bg='#111111', fg='#eeeeee', muted='#aaaaaa', line='#444444')
        def text(x, y, value, size=16, fill='fg', mono=False, weight=400, extra=''):
            return f'<text x="{x}" y="{y}" fill="{c[fill]}" font-family="{MONO if mono else SANS}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'
        content = draw(c, text)
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="{c["bg"]}"/>{content}</svg>'
        ET.fromstring(svg)
        (OUT / f'{name}-{theme}.svg').write_text(svg)


def picture(name, alt, width='100%', href=None, base='profile/'):
    light=f'./assets/{base}{name}-light.svg'
    dark=f'./assets/{base}{name}-dark.svg'
    p=f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}" /><img src="{light}" alt="{escape(alt, quote=True)}" width="{width}" /></picture>'
    return f'<a href="{href}">{p}</a>' if href else p


def heading(name, num, title, note):
    def draw(c,t):
        return t(0,37,num+' /',13,'muted',True)+t(53,38,title,23,mono=True,weight=600)+t(900,36,note,12,'muted',True,extra='text-anchor="end"')+f'<path d="M0 57H900" stroke="{c["fg"]}"/>'
    write(name,900,64,draw)


projects=[
 ('flowpix','F','FlowPix','IMAGE + VIDEO','An agentic canvas for images, video, and visual ideas.','flowpix.ai','https://flowpix.ai'),
 ('uooki','U','uooki','AGENT WORKSPACE','Turn a conversation into a website, report, dashboard, or deck.','uooki.com','https://uooki.com'),
 ('reelfo','R','reelfo','AI FILMMAKING','From one line to a short film: script, cast, storyboard, and cut.','reelfo.com','https://reelfo.com'),
 ('kiso','K','kiso','AGENT CORE','A small, durable TypeScript core for agents that pause and resume.','source','https://github.com/vincemakes/kiso'),
 ('model-boss','M','Model Boss','MODEL ORCHESTRATION','Big models think. Small models ship. For Claude Code & Codex.','source','https://github.com/vincemakes/model-boss'),
]
for name,letter,title,tag,desc,dest,url in projects:
    def draw(c,t,letter=letter,title=title,tag=tag,desc=desc,dest=dest):
        tag_x=49+len(title)*12.2+21
        return t(0,34,f'[{letter}]',16,'muted',True)+t(49,35,title,21,mono=True,weight=600)+t(tag_x,33,'/ '+tag,12,'muted',True)+t(49,67,desc,18,'muted')+t(900,37,dest+' ↗',13,'muted',True,extra='text-anchor="end"')+f'<path d="M0 92H900" stroke="{c["line"]}"/>'
    write(name,900,96,draw)

heading('products','01','Products','/ SELECTED WORK')
heading('open-source','02','Open source','/ SOURCE AVAILABLE')
heading('notes','03','Field notes','/ WRITING')
articles=[
 ('microkernel','AGENT SYSTEMS','The Agent Microkernel:','Notes from Thinking and Building ↗','https://www.hivince.com/en/blog/the-agent-microkernel-notes-from-thinking-and-building'),
 ('harness','BUILDING WITH AI','From “Rower” to “Steersman”:','Harness Engineering in the AI Era ↗','https://www.hivince.com/en/blog/harness-engineering')
]
for name,cat,line1,line2,url in articles:
    write(name,440,120,lambda c,t,cat=cat,line1=line1,line2=line2: t(0,27,cat,12,'muted',True)+t(0,62,line1,18)+t(0,91,line2,18))
write('footer',900,65,lambda c,t:f'<path d="M0 1H900" stroke="{c["line"]}"/>'+t(0,40,'>_ Build. Learn. Iterate.',15,mono=True)+t(900,40,'explore kiso.work ↗',14,'muted',True,extra='text-anchor="end"'))
for name,label,width in [('blog','Blog ↗',80),('social','X / @hi__vince ↗',183),('more-notes','More on hivince.com ↗',245)]:
    write(name,width,31,lambda c,t,label=label,width=width:t(0,21,label,14,mono=True)+f'<path d="M0 27H{width-8}" stroke="{c["muted"]}"/>')

parts=[picture('vince-mono','Vince — independent builder. I build creative tools and the systems that power agents.',base=''),
 '<p>'+picture('blog','Blog ↗','80','https://www.hivince.com')+' &nbsp; '+picture('social','X / @hi__vince ↗','183','https://x.com/hi__vince')+'</p>',
 'I build **AI-powered tools for creating and getting things done** — from images and films to agent-powered workspaces. I also open-source the systems behind better agent workflows, and write about what I learn along the way.']
for name,title,items in [('products','01 / Products — Selected work',projects[:3]),('open-source','02 / Open source',projects[3:])]:
    parts.append(picture(name,title))
    parts.append('<p>\n'+'\n'.join(picture(p[0],f'{p[2]} — {p[4]}','100%',p[6])+'<br />' for p in items)+'\n</p>')
parts.append(picture('notes','03 / Field notes'))
parts.append('<p>\n'+'\n'.join(picture(a[0],a[2]+' '+a[3],'49%',a[4]) for a in articles)+'\n</p>')
parts.append(picture('more-notes','More on hivince.com ↗','245','https://www.hivince.com'))
parts.append(picture('footer','Build. Learn. Iterate. Explore kiso.work.','100%','https://kiso.work'))
(ROOT/'README.md').write_text('\n\n'.join(parts)+'\n')
print('Generated monochrome assets and linked README.')
