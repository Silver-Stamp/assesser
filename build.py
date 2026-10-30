#!/usr/bin/env python3
"""Build the standalone GitHub Pages copy from the Perplexity source.
Usage: python3 build.py   (reads ../assesser/index.html, writes ./index.html)
Strips the agent's personal details (AGENT block), adds My info setup, PWA tags and service worker."""
import re, os, sys
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', 'assesser', 'index.html')).read()
h, n = re.subn(r"/\*AGENT_START\*/.*?/\*AGENT_END\*/", """/*AGENT_START*/const AGENT=(()=>{try{return JSON.parse(localStorage.getItem('assesser_agent'))||{}}catch(e){return{}}})();
function agentSetup(){const f=[['name','Your name (shown on client files and emails)'],['npn','Your NPN'],['phone','Your phone'],['email','Email to send client files to']];
for(const [k,q] of f){const v=prompt(q,AGENT[k]||'');if(v===null)return;AGENT[k]=v.trim()}
try{localStorage.setItem('assesser_agent',JSON.stringify(AGENT));alert('Saved on this device.')}catch(e){alert('Could not save on this device.')}}/*AGENT_END*/""", src, flags=re.S)
assert n == 1, 'AGENT block missing in source'
nav = """<button class="sec" onclick="show('cf')">Client Files</button>"""
assert nav in h, 'nav anchor missing'
h = h.replace(nav, nav + """<button class="sec" onclick="agentSetup()">My info</button>""", 1)
head = '<link rel="manifest" href="manifest.json"><link rel="apple-touch-icon" href="icon-180.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Assesser"><meta name="theme-color" content="#0f1419">\n'
h = h.replace('<title>', head + '<title>', 1)
i = h.rindex('</script>')
h = h[:i] + "\nif('serviceWorker' in navigator&&location.protocol==='https:'){navigator.serviceWorker.register('sw.js').catch(()=>{})}\n" + h[i:]
leak = [p for p in ['22069228', '432-9964', 'bensoninsures', '1189280', 'B170-0801', 'Benson'] if p in h]
if leak: sys.exit('Personal info still present: ' + ', '.join(leak))
open(os.path.join(here, 'index.html'), 'w').write(h)
print('built index.html', len(h))
