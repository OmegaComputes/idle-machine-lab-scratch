# Copyright 2026 Omega Compute
# SPDX-License-Identifier: Apache-2.0
"""Every Idle Machine Lab project, as a starter (with TODO notes) and a finished solution.
Run:  python3 tools/projects.py   ->  writes projects/<slug>/<slug>-starter.sb3 and -solution.sb3
Licence: Apache-2.0 (code). Art: CC BY 4.0 (see tools/art.py and NOTICE).
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from sb3build import *
import art

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = []
def project(slug, week, title, summary):
    def deco(fn):
        PROJECTS.append(dict(slug=slug, week=week, title=title, summary=summary, fn=fn)); return fn
    return deco

def base(title, bd=None):
    p = Project(title)
    p.stage.costume('backdrop', bd or art.bd_lab())
    return p

HEAD = 'Idle Machine Lab. Made with Scratch. Created by Rian L. Gabrielle. Owner: Omega Compute. CONCEPT / NOT FINAL.'

# ---------------------------------------------------------------- Week 2
@project('w02-in-think-out', 2, 'In, Think, Out', 'Click Juno. She says hello, asks your name and answers you.')
def w02(S):
    p = base('In, Think, Out')
    j = p.sprite('Juno', x=-60, y=-40); j.costume('juno', art.juno())
    p.stage.todo(HEAD)
    if S:
        j.script(clicked(), say('Hello!', 1), ask('What is your name?'), say(join('Hi ', answer(), '!'), 2))
    else:
        j.script(clicked(), say('Hello!', 1))
        j.todo('TODO 1: Add an "ask and wait" block. Make Juno ask, "What is your name?"\n\n'
               'TODO 2: Add a "say" block. Put a "join" block inside it, so Juno says "Hi" and then your answer.\n\n'
               'The click is the INPUT. Your blocks are the THINKING. The speech bubble is the OUTPUT.')
    return p

# ---------------------------------------------------------------- Week 4
@project('w04-packets', 4, 'Postcard Packets', 'Juno sends a message one word at a time. Dex says "Got it!" for every packet.')
def w04(S):
    p = base('Postcard Packets', art.bd_street(False))
    j = p.sprite('Juno', x=-150, y=-60); j.costume('juno', art.juno())
    d = p.sprite('Dex', x=150, y=-60); d.costume('dex', art.dex())
    got = p.stage.var('packets got', 0); p.show_var(got, 5, 5)
    p.stage.todo(HEAD)
    j.script(flag(), set_(got, 0), say('Share', 1), broadcast('packet'), wait(1), say('it', 1), broadcast('packet'),
             wait(1), say('grows', 1), broadcast('packet'))
    if S:
        d.script(when_receive('packet'), change(got, 1), say('Got it!', 0.5))
    else:
        d.todo('TODO: Dex needs to listen for each packet.\n\n'
               '1. Drag out "when I receive [packet]".\n'
               '2. Under it, add "change [packets got] by 1".\n'
               '3. Then add "say [Got it!] for 0.5 seconds".\n\n'
               'Test it: the counter should end at 3.')
    return p

# ---------------------------------------------------------------- Week 5
@project('w05-bug-hunt', 5, 'Bug Hunt', 'A broken project with three bugs to find and fix.')
def w05(S):
    p = base('Bug Hunt')
    r = p.sprite('Rollo', x=-120, y=-40); r.costume('rollo', art.rollo())
    k = p.sprite('Kip', x=120, y=-40); k.costume('kip', art.kip())
    p.stage.todo(HEAD)
    if S:
        r.script(flag(), say('Hello, Kip!', 1), wait(1), broadcast('hello kip'))
        k.script(when_receive('hello kip'), say('Hello, Rollo! All fixed.', 2))
    else:
        r.script(say('Hello, Kip!', 1), wait(10), broadcast('hello kipp'))
        k.script(when_receive('hello kip'), say('Hello, Rollo! All fixed.', 2))
        p.stage.todo('BUG HUNT! This project has 3 bugs.\n\n'
                     'What SHOULD happen: click the green flag. Rollo says hello. One second later, Kip says hello back.\n\n'
                     'Use the checklist: What should happen? What does happen? Where does it go wrong? Change ONE thing. Test again.\n\n'
                     'Hint: look at how Rollo\'s script starts, how long it waits, and the name of the message.')
    return p

# ---------------------------------------------------------------- Week 6
@project('w06-packet-relay', 6, 'Packet Relay', 'Three friends pass a message along and send back a thank-you.')
def w06(S):
    p = base('Packet Relay', art.bd_street(False))
    a = p.sprite('Juno', x=-170, y=-60); a.costume('juno', art.juno())
    b = p.sprite('Dex', x=-20, y=-60); b.costume('dex', art.dex())
    c = p.sprite('Pia', x=160, y=-60); c.costume('pia', art.pia())
    p.stage.todo(HEAD)
    a.script(flag(), say('Hello!', 1), broadcast('to2'))
    a.script(when_receive('ack'), say('Thank you!', 2))
    if S:
        b.script(flag(), goto(-20, -60))
        b.script(when_receive('to2'), glide_to(1, 'Pia'), say('Hello!', 1), broadcast('to3'))
        c.script(when_receive('to3'), say('Arrived!', 1), broadcast('ack'))
    else:
        b.todo('TODO for Dex (Sprite 2):\n1. "when I receive [to2]"\n2. "glide 1 secs to [Pia]"\n3. "say [Hello!] for 1 seconds"\n4. "broadcast [to3]"')
        c.todo('TODO for Pia (Sprite 3):\n1. "when I receive [to3]"\n2. "say [Arrived!] for 1 seconds"\n3. "broadcast [ack]" so Juno knows it got there.')
    return p

# ---------------------------------------------------------------- Week 7
@project('w07-maze-route', 7, 'Robot Route', 'Write the steps that take Kip through the maze to the clinic.')
def w07(S):
    p = base('Robot Route', art.bd_maze())
    k = p.sprite('Kip', x=-180, y=-140, size=40); k.costume('kip', art.kip())
    cl = p.sprite('Clinic', x=200, y=-140, size=70); cl.costume('clinic', art.clinic())
    p.stage.todo(HEAD)
    steps = [move(120), turn_left(90), move(260), turn_right(90), move(130), turn_right(90), move(260), turn_left(90), move(130)]
    first = [flag(), goto(-180, -140), point(90)]
    if S:
        k.script(*first, *[x for s in steps for x in (s, wait(0.3))], say('I made it to the clinic!', 2))
    else:
        k.script(*first, move(120), wait(0.3), turn_left(90), wait(0.3))
        k.todo('TODO: Finish the route to the clinic.\n\n'
               'Kip has gone right and turned up. Now add "move" and "turn" blocks to get past each wall.\n\n'
               'Tip: one square on the floor is about 60 steps. Test after every two blocks.\n\n'
               'Stretch: can you find a route with fewer blocks?')
    return p

# ---------------------------------------------------------------- Week 9
@project('w09-loop-shapes', 9, 'Loop It', 'Draw a square with a loop, then remix it into a hexagon.')
def w09(S):
    p = base('Loop It', art.bd_grid())
    j = p.sprite('Pen', x=0, y=0, size=30); j.costume('dot', art.dot('rust'))
    p.stage.todo(HEAD)
    start = [flag(), pen_clear(), pen_up(), goto(-60, -60), point(90), pen_color('#A64F36'), pen_size(4), pen_down()]
    if S:
        j.script(*start, repeat(4, move(120), turn_left(90), wait(0.2)), pen_up())
        j.script(key('h'), pen_clear(), pen_up(), goto(-40, -80), point(90), pen_color('#237D80'), pen_down(),
                 repeat(6, move(80), turn_left(60), wait(0.2)), pen_up())
    else:
        j.script(*start, move(120), turn_left(90), move(120), turn_left(90), move(120), turn_left(90), move(120), turn_left(90), pen_up())
        j.todo('TODO 1: This script copies the same two blocks 4 times. Rewrite it with ONE "repeat 4" loop.\n\n'
               'TODO 2: Make a new script: "when [h] key pressed". Use "repeat 6", "move 80" and "turn 60" to draw a hexagon.\n\n'
               'Pen blocks come from the Pen extension (bottom-left button).')
    return p

# ---------------------------------------------------------------- Week 10
@project('w10-night-rota', 10, 'Night Rota', 'Four friends take turns watching the clinic server.')
def w10(S):
    p = base('Night Rota', art.bd_street(True))
    names = ['Juno', 'Dex', 'Pia', 'Rollo']; arts = [art.juno, art.dex, art.pia, art.rollo]
    turn = p.stage.var('turn', 1); p.show_var(turn, 5, 5)
    p.stage.todo(HEAD)
    p.stage.script(flag(), set_(turn, 1), broadcast('next'))
    for i, (n, a) in enumerate(zip(names, arts)):
        s = p.sprite(n, x=-180 + i * 120, y=-60); s.costume(n.lower(), a())
        if S or i == 0:
            s.script(when_receive('next'), if_(eq(turn, i + 1), say('My shift!', 1), change(turn, 1), if_(lt(turn, 5), broadcast('next'))))
        elif i == 1:
            s.todo('TODO: Drag Juno\'s script onto Dex, Pia and Rollo.\n\n'
                   'Then fix the number in "turn = 1". Dex needs 2. Pia needs 3. Rollo needs 4.\n\n'
                   'Take turns. Eat first!')
    return p

# ---------------------------------------------------------------- Week 11
@project('w11-handover', 11, 'Someone to Take Over', 'Juno counts to 5 and hands over. Dex carries on from where she stopped.')
def w11(S):
    p = base('Someone to Take Over')
    j = p.sprite('Juno', x=-120, y=-40); j.costume('juno', art.juno())
    d = p.sprite('Dex', x=120, y=-40); d.costume('dex', art.dex())
    count = p.stage.var('count', 0); p.show_var(count, 5, 5)
    p.stage.todo(HEAD)
    j.script(flag(), set_(count, 0), repeat(5, change(count, 1), say(count, 0.4)), say('Your turn, Dex!', 1), broadcast('take over'))
    if S:
        d.script(when_receive('take over'), repeat(5, change(count, 1), say(count, 0.4)), say(join('Done! I stopped at ', count), 2))
    else:
        d.todo('TODO: Dex takes over the job.\n\n'
               '1. "when I receive [take over]"\n'
               '2. A "repeat 5" loop with "change [count] by 1" and "say (count) for 0.4 seconds".\n\n'
               'Dex should start from 6, because the count is shared. A good handover says where you stopped!')
    return p

# ---------------------------------------------------------------- Week 12
@project('w12-share-the-sum', 12, 'Share the Sum', 'Three helpers each add two numbers. Kip adds up the total.')
def w12(S):
    p = base('Share the Sum')
    total = p.stage.var('total', 0); done = p.stage.var('helpers done', 0)
    p.show_var(total, 5, 5); p.show_var(done, 5, 32)
    p.stage.todo(HEAD)
    boss = p.sprite('Kip', x=0, y=60, size=80); boss.costume('kip', art.kip())
    boss.script(flag(), set_(total, 0), set_(done, 0), broadcast('start'), wait_until(eq(done, 3)), say(join('The total is ', total), 3))
    pairs = [(4, 5), (7, 8), (10, 6)]
    for i, (n, a) in enumerate(zip(['Juno', 'Pia', 'Rollo'], [art.juno, art.pia, art.rollo])):
        h = p.sprite(n, x=-160 + i * 160, y=-90, size=80); h.costume(n.lower(), a())
        x, y = pairs[i]
        if S or i == 0:
            h.script(when_receive('start'), wait(0.5 * (i + 1)), say(join(x, ' + ', y), 0.5), change(total, add(x, y)), change(done, 1))
        else:
            h.todo(f'TODO for {n}: copy Juno\'s script here. Change the numbers to {x} + {y}.\n\n'
                   'Each helper adds its answer to the shared total, then adds 1 to "helpers done".')
    return p

# ---------------------------------------------------------------- Week 14
@project('w14-lights-out', 14, 'Lights Out', 'Compare a hub town with a web town when the hub goes dark.')
def w14(S):
    p = base('Lights Out', art.bd_street(True))
    net = p.stage.var('network', 'hub'); lit = p.stage.var('lamps lit', 0)
    p.show_var(net, 5, 5); p.show_var(lit, 5, 32)
    p.stage.todo(HEAD + '\n\nPress H for a hub town. Press W for a web town. Press SPACE to make the hub go dark.')
    hb = p.sprite('Hub', x=0, y=120, size=80); hb.costume('hub', art.hub())
    p.stage.script(key('h'), set_(net, 'hub'), broadcast('lights on'))
    p.stage.script(key('w'), set_(net, 'web'), broadcast('lights on'))
    p.stage.script(flag(), set_(net, 'hub'), broadcast('lights on'))
    hb.script(key('space'), broadcast('hub down'), say('The hub went dark!', 1))
    for i in range(5):
        l = p.sprite(f'Lamp {i+1}', x=-200 + i * 100, y=-70, size=80)
        l.costume('on', art.lamp(True)).costume('off', art.lamp(False))
        on_ = l.var('power', 1)
        l.script(when_receive('lights on'), set_(on_, 1), costume('on'))
        if S:
            l.script(when_receive('hub down'), if_(eq(net, 'hub'), set_(on_, 0), costume('off')))
        elif i == 0:
            l.todo('TODO: When the hub goes dark, what happens to this lamp?\n\n'
                   'Add "when I receive [hub down]". Inside "if <(network) = [hub]>", set power to 0 and switch to the "off" costume.\n\n'
                   'In a web town, the lamp has other links, so it stays on. Then copy your script to every lamp.')
    # stage counts lit lamps after each event
    p.stage.script(when_receive('hub down'), wait(0.5), broadcast('count'))
    p.stage.script(when_receive('lights on'), wait(0.5), broadcast('count'))
    p.stage.script(when_receive('count'), set_(lit, 0), broadcast('report'))
    for l in p.sprites[1:]:
        l.script(when_receive('report'), if_(eq(l.vars[0], 1), change(lit, 1)))
    return p

# ---------------------------------------------------------------- Weeks 16-17
@project('w16-vote-counter', 16, 'Neighbourhood Vote', 'Five neighbours vote. Rollo counts the votes and says which job goes first.')
def w16(S):
    p = base('Neighbourhood Vote', art.bd_street(False))
    r = p.sprite('Rollo', x=-140, y=-50); r.costume('rollo', art.rollo())
    cv = p.stage.var('clinic votes', 0); rv = p.stage.var('reading votes', 0); tv = p.stage.var('total votes', 0)
    for i, v in enumerate([cv, rv, tv]): p.show_var(v, 5, 5 + 27 * i)
    p.stage.todo(HEAD)
    count = [ask('Clinic or reading?'), change(tv, 1),
             if_(eq(answer(), 'clinic'), change(cv, 1)), if_(eq(answer(), 'reading'), change(rv, 1))]
    winner = if_else(gt(cv, rv), [say(join('Clinic first! ', cv, ' votes.'), 3)],
                     [if_else(gt(rv, cv), [say(join('Reading pack first! ', rv, ' votes.'), 3)], [say('It is a tie. Let us talk it through.', 3)])])
    if S:
        r.script(flag(), set_(cv, 0), set_(rv, 0), set_(tv, 0), repeat(5, *count), winner)
    else:
        r.script(flag(), set_(cv, 0), repeat(5, ask('Clinic or reading?'), if_(eq(answer(), 'clinic'), change(cv, 1))))
        r.todo('TODO 1: Reading votes are not counted yet! Add an "if" for "reading".\n\n'
               'TODO 2: Set "reading votes" and "total votes" to 0 at the start. Add 1 to "total votes" for every vote.\n\n'
               'TODO 3 (Week 17): After the loop, use "if ... else" with ">" to say which job won, or say it is a tie.')
    return p

# ---------------------------------------------------------------- Weeks 19-22
@project('w22-ledger-keeper', 22, 'Ledger Keeper', 'Pia writes every trade in a shared ledger list.')
def w22(S):
    p = base('Ledger Keeper', art.bd_plain('cream'))
    pia = p.sprite('Pia', x=-170, y=-60); pia.costume('pia', art.pia())
    led = p.stage.list('ledger'); p.show_var(led, 220, 10)
    giver = pia.var('giver', ''); getter = pia.var('getter', ''); n = pia.var('how many', 0)
    p.stage.todo(HEAD + '\n\nThe counters are pretend. They are not money.')
    if S:
        pia.script(flag(), list_clear(led), say('Click me to add a trade.', 2))
        pia.script(clicked(), ask('Who gives?'), set_(giver, answer()), ask('Who gets?'), set_(getter, answer()),
                   ask('How many counters?'), set_(n, answer()),
                   list_add(join('Line ', add(list_len(led), 1), ': ', giver, ' gives ', n, ' to ', getter), led),
                   say(join('The ledger has ', list_len(led), ' lines.'), 2))
    else:
        pia.script(flag(), list_clear(led), say('Click me to add a trade.', 2))
        pia.script(clicked(), ask('Who gives?'), set_(giver, answer()))
        pia.todo('TODO 1: Ask "Who gets?" and set [getter] to the answer.\n\n'
                 'TODO 2: Ask "How many counters?" and set [how many] to the answer.\n\n'
                 'TODO 3: Use "add [ ] to [ledger]" with "join" blocks, so a line reads: Line 1: Ana gives 2 to Ben\n\n'
                 'TODO 4: Say how many lines the ledger has, using "length of [ledger]".')
    return p

@project('w20-copy-compare', 20, 'Copy and Compare', 'Two copies of a ledger. Dex checks them line by line and finds the change.')
def w20(S):
    p = base('Copy and Compare', art.bd_plain('cream'))
    d = p.sprite('Dex', x=-180, y=-80); d.costume('dex', art.dex())
    lines = ['Ana gives 2 to Ben', 'Ben gives 1 to Cal', 'Cal gives 3 to Ana', 'Ana gives 1 to Dee']
    changed = list(lines); changed[2] = 'Cal gives 5 to Ana'
    A = p.stage.list('copy A', lines); B = p.stage.list('copy B', changed)
    p.show_var(A, 10, 10); p.show_var(B, 250, 10)
    i = d.var('line', 1); diffs = p.stage.var('differences', 0); p.show_var(diffs, 10, 300)
    p.stage.todo(HEAD)
    if S:
        d.script(flag(), set_(i, 1), set_(diffs, 0),
                 repeat(list_len(A), if_else(eq(item(i, A), item(i, B)), [say(join('Line ', i, ' matches.'), 0.6)],
                                            [say(join('Line ', i, ' is different!'), 1.2), change(diffs, 1)]), change(i, 1)),
                 say(join('I found ', diffs, ' difference(s).'), 3))
    else:
        d.script(flag(), set_(i, 1), set_(diffs, 0), say('I will check line 1.', 1))
        d.todo('TODO: Check every line.\n\n'
               '1. Use "repeat (length of [copy A])".\n'
               '2. Inside, use "if <(item (line) of [copy A]) = (item (line) of [copy B])> then ... else ...".\n'
               '3. If they are different, add 1 to [differences].\n'
               '4. Add 1 to [line] each time round.\n\nMany copies help us spot a change!')
    return p

@project('w21-check-number', 21, 'Check Numbers', 'Work out a check number for a word, using A=1 to Z=26.')
def w21(S):
    p = base('Check Numbers', art.bd_plain('cream'))
    j = p.sprite('Juno', x=-160, y=-60); j.costume('juno', art.juno())
    abc = p.stage.list('alphabet', list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    word = j.var('word', ''); i = j.var('i', 1); chk = p.stage.var('check number', 0); p.show_var(chk, 5, 5)
    p.stage.todo(HEAD + '\n\nReal computers use much stronger checks called hashes. This is a model.')
    loop = repeat(length(word), change(chk, item_num(letter(i, word), abc)), change(i, 1))
    if S:
        j.script(flag(), ask('Type a word'), set_(word, answer()), set_(i, 1), set_(chk, 0), loop,
                 say(join('The check number for ', word, ' is ', chk), 3))
    else:
        j.script(flag(), ask('Type a word'), set_(word, answer()), set_(i, 1), set_(chk, 0))
        j.todo('TODO: Add up the letter numbers.\n\n'
               'Use "repeat (length of (word))". Inside it:\n'
               '- change [check number] by (item # of (letter (i) of (word)) in [alphabet])\n'
               '- change [i] by 1\n\nThen say the check number. CAT should give 24.')
    return p

# ---------------------------------------------------------------- Week 26
@project('w26-code-machine', 26, 'Code Machine', 'A shift-code machine. Change the key, encode a message, then decode it.')
def w26(S):
    p = base('Code Machine', art.bd_plain('lilac'))
    k = p.sprite('Kip', x=-170, y=-60); k.costume('kip', art.kip())
    abc = p.stage.list('alphabet', list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    key_ = p.stage.var('key', 3); msg = k.var('message', ''); out = p.stage.var('result', ''); i = k.var('i', 1); n = k.var('n', 0)
    p.show_var(key_, 5, 5); p.show_var(out, 5, 32)
    p.stage.todo(HEAD + '\n\nPress E to encode. Press D to decode. Use capital letters and spaces.')
    def coder(sign):
        shifted = add(mod(sub(add(n, mul(sign, key_)), 1), 26), 1)
        return [ask('Type a message'), set_(msg, answer()), set_(out, ''), set_(i, 1),
                repeat(length(msg),
                       set_(n, item_num(letter(i, msg), abc)),
                       if_else(eq(n, 0), [set_(out, join(out, letter(i, msg)))], [set_(out, join(out, item(shifted, abc)))]),
                       change(i, 1)),
                say(out, 3)]
    k.script(key('e'), *coder(1))
    if S:
        k.script(key('d'), *coder(-1))
    else:
        k.todo('TODO: Build the decode button.\n\n'
               '1. Right-click the "when [e] key pressed" script and choose Duplicate.\n'
               '2. Change the key to [d].\n'
               '3. Decoding goes backwards, so change "1 x (key)" to "-1 x (key)".\n\n'
               'Test: encode HELLO with key 3. You get KHOOR. Decode KHOOR to get HELLO back.')
    return p

# ---------------------------------------------------------------- Week 27
@project('w27-password-door', 27, 'Password Door', 'A door that opens only for the right pretend password.')
def w27(S):
    p = base('Password Door', art.bd_street(False))
    dr = p.sprite('Door', x=60, y=-40); dr.costume('closed', art.door(False)).costume('open', art.door(True))
    secret = dr.var('secret', 'lamp-river-pickle')
    p.stage.todo(HEAD + '\n\nThis is a PRETEND password. Never use it, or any real password, here.')
    if S:
        dr.script(flag(), costume('closed'))
        dr.script(clicked(), ask('Password, please?'),
                  if_else(eq(answer(), secret), [costume('open'), say('Come in!', 2)], [say('Sorry, that is not it.', 2)]))
    else:
        dr.script(flag(), costume('closed'))
        dr.script(clicked(), ask('Password, please?'), costume('open'), say('Come in!', 2))
        dr.todo('TODO: Oops! This door opens for ANY answer.\n\n'
                'Use "if <(answer) = (secret)> then ... else ...". Open the door only when the answer matches. Otherwise say "Sorry, that is not it."\n\n'
                'Think: why should a real password never be shown on the screen?')
    return p

# ---------------------------------------------------------------- Week 29
@project('w29-careful-helper', 29, 'Careful Helper', 'An SI helper that says "Please ask a grown-up first" when a request has private words.')
def w29(S):
    p = base('Careful Helper', art.bd_lab())
    k = p.sprite('Kip', x=-150, y=-50); k.costume('kip', art.kip())
    priv = p.stage.list('private words', ['password', 'address', 'photo', 'phone', 'surname'])
    p.show_var(priv, 330, 10)
    i = k.var('i', 1); found = k.var('found', 0)
    p.stage.todo(HEAD + '\n\nIn the story, SI helpers do what they are asked. So the big question is always: who is asking, and what for?')
    check = [set_(i, 1), set_(found, 0), repeat(list_len(priv), if_(contains(answer(), item(i, priv)), set_(found, 1)), change(i, 1))]
    reply = if_else(eq(found, 1), [say('Please ask a grown-up first.', 3)], [say('Happy to help! What should I check when it is done?', 3)])
    if S:
        k.script(clicked(), ask('What do you need?'), *check, reply)
    else:
        k.script(clicked(), ask('What do you need?'), say('Happy to help!', 2))
        k.todo('TODO: Kip says yes to everything! Make him careful.\n\n'
               '1. Look through the [private words] list with "repeat" and "item (i) of [private words]".\n'
               '2. If the answer contains a private word, set [found] to 1.\n'
               '3. If found = 1, say "Please ask a grown-up first." Otherwise say "Happy to help!"')
    return p

# ---------------------------------------------------------------- Capstone (Weeks 33-35)
@project('capstone-idle-machine-network', 33, 'The Idle Machine Network',
         'Capstone: a job board, three idle machines, a checker, a machine that goes dark and a credits screen.')
def capstone(S):
    p = base('The Idle Machine Network', art.bd_street(True))
    JA = p.stage.list('job a'); JB = p.stage.list('job b'); RES = p.stage.list('results')
    CA = p.stage.list('check a'); CB = p.stage.list('check b'); CANS = p.stage.list('check answer')
    checked = p.stage.var('checked', 0); bad = p.stage.var('mismatches', 0)
    p.show_var(RES, 300, 10); p.show_var(checked, 5, 5); p.show_var(bad, 5, 32)
    p.stage.todo(HEAD + '\n\nGreen flag: start. SPACE: Machine 2 goes dark. C: credits.')
    jb = p.sprite('Job Board', x=-170, y=110, size=80); jb.costume('board', art.board())
    jb.script(flag(), list_clear(JA), list_clear(JB), list_clear(RES), list_clear(CA), list_clear(CB), list_clear(CANS),
              set_(checked, 0), set_(bad, 0),
              repeat(12, list_add(rnd(1, 50), JA), list_add(rnd(1, 50), JB)), say('12 jobs ready!', 1), broadcast('open'))
    lights = ['mint', 'lilac', 'coral']
    p.stage.script(flag(), broadcast('reset machines'))
    for m in range(3):
        s = p.sprite(f'Machine {m+1}', x=-150 + m * 110, y=-60, size=80)
        s.costume('idle', art.machine(lights[m], str(m + 1))).costume('dark', art.machine('#4A4A55', str(m + 1)))
        idle = s.var('idle', 'yes'); done = s.var('jobs done', 0); a = s.var('a', 0); b = s.var('b', 0); dark = s.var('dark', 'no')
        p.show_var(done, 5 + 0 * m, 60 + 27 * m, s.name)
        s.script(when_receive('reset machines'), set_(dark, 'no'), costume('idle'), say(''))
        work = [set_(idle, 'no'), set_(a, item(1, JA)), set_(b, item(1, JB)), list_del(1, JA), list_del(1, JB),
                say(join(a, ' + ', b)), wait(rnd(0.2, 0.6)),
                list_add(join(a, ' + ', b, ' = ', add(a, b)), RES),
                list_add(a, CA), list_add(b, CB), list_add(add(a, b), CANS),
                change(done, 1), say(''), set_(idle, 'yes')]
        if S or m == 0:
            s.script(when_receive('open'), set_(idle, 'yes'), set_(done, 0),
                     forever(if_(and_(and_(eq(idle, 'yes'), eq(dark, 'no')), gt(list_len(JA), 0)), *work)))
        else:
            s.todo(f'TODO: Machine {m+1} needs a brain!\n\nCopy Machine 1\'s "when I receive [open]" script here. '
                   'A machine only takes a job when it is idle.')
        if m == 1:
            if S:
                s.script(key('space'), stop('other scripts in sprite'), set_(dark, 'yes'), costume('dark'),
                         if_(eq(idle, 'no'), list_add(a, JA), list_add(b, JB), set_(idle, 'yes'), say('Gone dark. I put my job back.', 2)),
                         say('Gone dark', 2))
            else:
                s.todo('TODO (Week 35): When SPACE is pressed, make this machine go dark:\n'
                       '"stop [other scripts in sprite]", set [dark] to "yes", switch to the "dark" costume.\n'
                       'If it was busy (idle = no), put its job back on the job lists first.\n\n'
                       'Do the other machines still finish every job?')
    ck = p.sprite('Checker', x=170, y=-150, size=60); ck.costume('kip', art.kip())
    if S:
        ck.script(when_receive('open'), wait(0.5),
                  until(eq(checked, 12),
                        if_(gt(list_len(CA), 0),
                            if_else(eq(add(item(1, CA), item(1, CB)), item(1, CANS)), [change(checked, 1)],
                                    [change(bad, 1), list_add(item(1, CA), JA), list_add(item(1, CB), JB)]),
                            list_del(1, CA), list_del(1, CB), list_del(1, CANS)),
                        wait(0.05)),
                  say(join('Checked ', checked, ' jobs. ', bad, ' sent back.'), 3))
    else:
        ck.todo('TODO (Week 34): The Checker does each job again.\n\n'
                'While there are items in [check a]: add item 1 of [check a] and item 1 of [check b]. '
                'If it equals item 1 of [check answer], change [checked] by 1. If not, change [mismatches] by 1 and put the numbers back on the job lists.\n'
                'Then delete item 1 of all three check lists.')
    cr = p.sprite('Credits', x=0, y=0, visible=False); cr.costume('credits', art.board('CREDITS'))
    cr.script(flag(), hide())
    cr.script(key('c'), show(), say('Made by: (first names or initials only). Ideas from: The Idle Machine Lab. Art: Idle Machine Lab (CC BY 4.0).', 4), hide())
    return p

def build_all(out=ROOT / 'projects'):
    index = []
    for pr in PROJECTS:
        for kind in ('starter', 'solution'):
            proj = pr['fn'](kind == 'solution')
            path = out / pr['slug'] / f"{pr['slug']}-{kind}.sb3"
            proj.build(path)
        index.append({k: v for k, v in pr.items() if k != 'fn'})
    (out / 'index.json').write_text(json.dumps(index, indent=1))
    return index

if __name__ == '__main__':
    idx = build_all()
    print(len(idx), 'projects,', 2 * len(idx), '.sb3 files')
