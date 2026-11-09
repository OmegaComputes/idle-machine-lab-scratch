# Copyright 2026 Omega Compute
# SPDX-License-Identifier: Apache-2.0
"""Write docs/projects/<slug>.md for every project (teacher pages). Apache-2.0. Text output is CC BY 4.0."""
import json, zipfile, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECK = {
 'w02-in-think-out': 'Click Juno. Type **Ana**. Juno should say **Hi Ana!**',
 'w04-packets': 'Click the green flag. Dex should say **Got it!** three times, and **packets got** should reach 3.',
 'w05-bug-hunt': 'Click the green flag. Kip should say **Hello, Rollo! All fixed.**',
 'w06-packet-relay': 'Click the green flag. Pia should say **Arrived!** and then Juno should say **Thank you!**',
 'w07-maze-route': 'Click the green flag. Kip should reach the clinic without crossing a wall and say **I made it to the clinic!**',
 'w09-loop-shapes': 'Click the green flag to draw a square. Press **H** to draw a hexagon. The pen script should use a **repeat** loop.',
 'w10-night-rota': 'Click the green flag. Juno, Dex, Pia and Rollo should each say **My shift!** in turn.',
 'w11-handover': 'Click the green flag. Juno counts to 5, then Dex carries on and says **Done! I stopped at 10**.',
 'w12-share-the-sum': 'Click the green flag. Kip should say **The total is 40**.',
 'w14-lights-out': 'Green flag, then press **SPACE**: in the hub town every lamp goes dark. Press **W** to switch to the web town, then **SPACE** again: the lamps stay lit.',
 'w16-vote-counter': 'Green flag. Type the five votes: clinic, reading, clinic, clinic, reading. Rollo should say **Clinic first! 3 votes.**',
 'w20-copy-compare': 'Click the green flag. Dex should say **Line 3 is different!** and **differences** should be 1.',
 'w21-check-number': 'Green flag. Type **CAT**. The check number should be **24** (3 + 1 + 20).',
 'w22-ledger-keeper': 'Click Pia. Type **Ana**, **Ben**, **2**. The ledger should show **Line 1: Ana gives 2 to Ben**.',
 'w26-code-machine': 'Press **E** and type **HELLO WORLD**: Kip says **KHOOR ZRUOG**. Press **D** and type **KHOOR**: Kip says **HELLO**.',
 'w27-password-door': 'Click the door and type **1234**: it stays shut. Click again and type **lamp-river-pickle**: it opens. (Pretend passwords only.)',
 'w29-careful-helper': 'Click Kip and type **here is my address**: Kip says **Please ask a grown-up first.** Click again and type **a fun fact about owls**: Kip is happy to help.',
 'capstone-idle-machine-network': 'Green flag, then press **SPACE** while the machines work. Machine 2 goes dark, but the Checker should still say **Checked 12 jobs. 0 sent back.** Press **C** for the credits.',
}
LINK = '../../README.md'
def todos(path):
    j = json.loads(zipfile.ZipFile(path).read('project.json'))
    out = []
    for t in j['targets']:
        for c in t.get('comments', {}).values():
            if 'TODO' in c['text'] or 'BUG' in c['text'].upper():
                out.append((t['name'], c['text'].strip()))
    return out
def main():
    idx = json.load(open(ROOT / 'projects/index.json'))
    rows = []
    for e in sorted(idx, key=lambda e: e['week']):
        s = e['slug']; d = ROOT / 'projects' / s
        wk = 'Capstone (Weeks 32–36)' if s.startswith('capstone') else f"Week {e['week']}"
        md = [f"# {e['title']}", '', f"**{wk}** · Idle Machine Lab · CONCEPT / NOT FINAL", '',
              f"> {e['summary']}", '',
              '| Starter (what pupils open) | Finished solution |', '|---|---|',
              f"| ![starter](../img/{s}-starter.png) | ![solution](../img/{s}-solution.png) |", '',
              '*Screenshots are real stage renders made with scratch-vm and scratch-render, after the green flag. Variable boxes and the editor are not shown.*', '',
              '## Files', '',
              f"- Starter: [`projects/{s}/{s}-starter.sb3`](../../projects/{s}/{s}-starter.sb3)",
              f"- Solution: [`projects/{s}/{s}-solution.sb3`](../../projects/{s}/{s}-solution.sb3) (teacher copy; hand out after the lesson if you like)", '',
              'Open in Scratch: **File → Load from your computer**. No Scratch account is needed.', '',
              '## What pupils do', '', 'These notes are inside the starter, as yellow comments next to the code:', '']
        for who, t in todos(d / f'{s}-starter.sb3'):
            md.append(f"**{who}**"); md.append(''); md += ['> ' + ln if ln else '>' for ln in t.split('\n')]; md.append('')
        md += ['## How to check it works', '', CHECK[s], '',
               'The same check runs automatically in `tests/validate.js`.', '',
               '## In the curriculum', '',
               f"See the {wk} lesson in *The Idle Machine Lab* (Semester {'1' if e['week'] <= 18 else '2'} plan). Standards are listed by code only in the curriculum's standards map.", '',
               '---', '', 'Created by Rian L. Gabrielle · © Omega Compute · Text and art CC BY 4.0 · Code Apache-2.0 · Scratch is a project of the Scratch Foundation; this is not an official Scratch product.']
        (ROOT / 'docs/projects' / f'{s}.md').write_text('\n'.join(md) + '\n')
        rows.append(f"| {wk.replace('Capstone (Weeks 32–36)','32–36')} | [{e['title']}](docs/projects/{s}.md) | {e['summary']} |")
    return rows
if __name__ == '__main__': main()
