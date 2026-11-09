# Copyright 2026 Omega Compute
# SPDX-License-Identifier: Apache-2.0
"""Tiny builder for valid Scratch 3 (.sb3) projects.

Write scripts as nested Python calls, get a project.json plus SVG assets zipped as .sb3.
Licence: Apache-2.0. Part of idle-machine-lab-scratch (Omega Compute).
"""
import hashlib, json, re, zipfile, itertools
from pathlib import Path

_ids = itertools.count(1)
def uid(prefix='b'):
    return f"{prefix}{next(_ids):04d}"

# input kinds: int = primitive code; 'bool' = boolean slot; 'stack' = substack;
# 'bcast' = broadcast menu; ('menu', opcode, FIELD) = shadow menu block
NUM, POS, WHOLE, INT, ANGLE, COLOR, TEXT = 4, 5, 6, 7, 8, 9, 10
SPEC = {
 'event_whenflagclicked': {}, 'event_whenthisspriteclicked': {},
 'event_whenkeypressed': {}, 'event_whenbroadcastreceived': {},
 'event_broadcast': {'BROADCAST_INPUT': 'bcast'}, 'event_broadcastandwait': {'BROADCAST_INPUT': 'bcast'},
 'looks_say': {'MESSAGE': TEXT}, 'looks_sayforsecs': {'MESSAGE': TEXT, 'SECS': NUM},
 'looks_think': {'MESSAGE': TEXT}, 'looks_thinkforsecs': {'MESSAGE': TEXT, 'SECS': NUM},
 'looks_show': {}, 'looks_hide': {}, 'looks_setsizeto': {'SIZE': NUM},
 'looks_switchcostumeto': {'COSTUME': ('menu', 'looks_costume', 'COSTUME')},
 'looks_switchbackdropto': {'BACKDROP': ('menu', 'looks_backdrops', 'BACKDROP')},
 'motion_movesteps': {'STEPS': NUM}, 'motion_turnright': {'DEGREES': NUM}, 'motion_turnleft': {'DEGREES': NUM},
 'motion_gotoxy': {'X': NUM, 'Y': NUM}, 'motion_glidesecstoxy': {'SECS': NUM, 'X': NUM, 'Y': NUM},
 'motion_glideto': {'SECS': NUM, 'TO': ('menu', 'motion_glideto_menu', 'TO')},
 'motion_pointindirection': {'DIRECTION': ANGLE}, 'motion_changeyby': {'DY': NUM}, 'motion_changexby': {'DX': NUM},
 'control_wait': {'DURATION': POS}, 'control_repeat': {'TIMES': WHOLE, 'SUBSTACK': 'stack'},
 'control_forever': {'SUBSTACK': 'stack'}, 'control_if': {'CONDITION': 'bool', 'SUBSTACK': 'stack'},
 'control_if_else': {'CONDITION': 'bool', 'SUBSTACK': 'stack', 'SUBSTACK2': 'stack'},
 'control_repeat_until': {'CONDITION': 'bool', 'SUBSTACK': 'stack'}, 'control_wait_until': {'CONDITION': 'bool'},
 'control_stop': {},
 'operator_add': {'NUM1': NUM, 'NUM2': NUM}, 'operator_subtract': {'NUM1': NUM, 'NUM2': NUM},
 'operator_multiply': {'NUM1': NUM, 'NUM2': NUM}, 'operator_divide': {'NUM1': NUM, 'NUM2': NUM},
 'operator_mod': {'NUM1': NUM, 'NUM2': NUM}, 'operator_random': {'FROM': NUM, 'TO': NUM},
 'operator_equals': {'OPERAND1': TEXT, 'OPERAND2': TEXT}, 'operator_gt': {'OPERAND1': TEXT, 'OPERAND2': TEXT},
 'operator_lt': {'OPERAND1': TEXT, 'OPERAND2': TEXT}, 'operator_and': {'OPERAND1': 'bool', 'OPERAND2': 'bool'},
 'operator_or': {'OPERAND1': 'bool', 'OPERAND2': 'bool'}, 'operator_not': {'OPERAND': 'bool'},
 'operator_join': {'STRING1': TEXT, 'STRING2': TEXT}, 'operator_letter_of': {'LETTER': WHOLE, 'STRING': TEXT},
 'operator_length': {'STRING': TEXT}, 'operator_contains': {'STRING1': TEXT, 'STRING2': TEXT},
 'data_setvariableto': {'VALUE': TEXT}, 'data_changevariableby': {'VALUE': NUM},
 'data_addtolist': {'ITEM': TEXT}, 'data_deleteoflist': {'INDEX': INT}, 'data_deletealloflist': {},
 'data_itemoflist': {'INDEX': INT}, 'data_lengthoflist': {}, 'data_itemnumoflist': {'ITEM': TEXT},
 'data_listcontainsitem': {'ITEM': TEXT}, 'data_replaceitemoflist': {'INDEX': INT, 'ITEM': TEXT},
 'sensing_askandwait': {'QUESTION': TEXT}, 'sensing_answer': {},
 'pen_clear': {}, 'pen_penDown': {}, 'pen_penUp': {}, 'pen_setPenColorToColor': {'COLOR': COLOR},
 'pen_setPenSizeTo': {'SIZE': NUM},
}
DEFAULTS = {NUM: '0', POS: '1', WHOLE: '1', INT: '1', ANGLE: '90', COLOR: '#a9d8c5', TEXT: ''}

class Var:
    def __init__(self, name, value=0, is_list=False):
        self.name, self.value, self.is_list = name, value, is_list
        self.id = uid('l' if is_list else 'v')

class N:
    """A block node."""
    def __init__(self, op, inputs=None, fields=None, comment=None, mutation=None):
        assert op in SPEC, op
        self.op, self.inputs, self.fields = op, inputs or {}, fields or {}
        self.comment, self.mutation = comment, mutation
    def note(self, text):
        self.comment = text; return self

# ---- block helpers (readable names) ----
def flag(): return N('event_whenflagclicked')
def clicked(): return N('event_whenthisspriteclicked')
def key(k): return N('event_whenkeypressed', fields={'KEY_OPTION': [k, None]})
def when_receive(msg): return N('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': msg})
def broadcast(msg): return N('event_broadcast', {'BROADCAST_INPUT': msg})
def broadcast_wait(msg): return N('event_broadcastandwait', {'BROADCAST_INPUT': msg})
def say(m, secs=None): return N('looks_sayforsecs', {'MESSAGE': m, 'SECS': secs}) if secs is not None else N('looks_say', {'MESSAGE': m})
def think(m, secs): return N('looks_thinkforsecs', {'MESSAGE': m, 'SECS': secs})
def costume(c): return N('looks_switchcostumeto', {'COSTUME': c})
def backdrop(c): return N('looks_switchbackdropto', {'BACKDROP': c})
def show(): return N('looks_show')
def hide(): return N('looks_hide')
def move(n): return N('motion_movesteps', {'STEPS': n})
def turn_right(d): return N('motion_turnright', {'DEGREES': d})
def turn_left(d): return N('motion_turnleft', {'DEGREES': d})
def goto(x, y): return N('motion_gotoxy', {'X': x, 'Y': y})
def glide_xy(s, x, y): return N('motion_glidesecstoxy', {'SECS': s, 'X': x, 'Y': y})
def glide_to(s, sprite): return N('motion_glideto', {'SECS': s, 'TO': sprite})
def point(d): return N('motion_pointindirection', {'DIRECTION': d})
def change_y(d): return N('motion_changeyby', {'DY': d})
def wait(s): return N('control_wait', {'DURATION': s})
def repeat(n, *body): return N('control_repeat', {'TIMES': n, 'SUBSTACK': list(body)})
def forever(*body): return N('control_forever', {'SUBSTACK': list(body)})
def if_(c, *body): return N('control_if', {'CONDITION': c, 'SUBSTACK': list(body)})
def if_else(c, a, b): return N('control_if_else', {'CONDITION': c, 'SUBSTACK': a, 'SUBSTACK2': b})
def until(c, *body): return N('control_repeat_until', {'CONDITION': c, 'SUBSTACK': list(body)})
def wait_until(c): return N('control_wait_until', {'CONDITION': c})
def stop(opt='all'):
    return N('control_stop', fields={'STOP_OPTION': [opt, None]},
             mutation={'tagName': 'mutation', 'children': [], 'hasnext': 'true' if opt == 'other scripts in sprite' else 'false'})
def add(a, b): return N('operator_add', {'NUM1': a, 'NUM2': b})
def sub(a, b): return N('operator_subtract', {'NUM1': a, 'NUM2': b})
def mul(a, b): return N('operator_multiply', {'NUM1': a, 'NUM2': b})
def mod(a, b): return N('operator_mod', {'NUM1': a, 'NUM2': b})
def rnd(a, b): return N('operator_random', {'FROM': a, 'TO': b})
def eq(a, b): return N('operator_equals', {'OPERAND1': a, 'OPERAND2': b})
def gt(a, b): return N('operator_gt', {'OPERAND1': a, 'OPERAND2': b})
def lt(a, b): return N('operator_lt', {'OPERAND1': a, 'OPERAND2': b})
def and_(a, b): return N('operator_and', {'OPERAND1': a, 'OPERAND2': b})
def or_(a, b): return N('operator_or', {'OPERAND1': a, 'OPERAND2': b})
def not_(a): return N('operator_not', {'OPERAND': a})
def join(*parts):
    parts = list(parts)
    if len(parts) == 1: return parts[0]
    return N('operator_join', {'STRING1': parts[0], 'STRING2': join(*parts[1:])})
def letter(i, s): return N('operator_letter_of', {'LETTER': i, 'STRING': s})
def length(s): return N('operator_length', {'STRING': s})
def contains(a, b): return N('operator_contains', {'STRING1': a, 'STRING2': b})
def set_(v, val): return N('data_setvariableto', {'VALUE': val}, {'VARIABLE': v})
def change(v, by=1): return N('data_changevariableby', {'VALUE': by}, {'VARIABLE': v})
def list_add(item, l): return N('data_addtolist', {'ITEM': item}, {'LIST': l})
def list_del(i, l): return N('data_deleteoflist', {'INDEX': i}, {'LIST': l})
def list_clear(l): return N('data_deletealloflist', fields={'LIST': l})
def item(i, l): return N('data_itemoflist', {'INDEX': i}, {'LIST': l})
def list_len(l): return N('data_lengthoflist', fields={'LIST': l})
def item_num(x, l): return N('data_itemnumoflist', {'ITEM': x}, {'LIST': l})
def list_has(l, x): return N('data_listcontainsitem', {'ITEM': x}, {'LIST': l})
def ask(q): return N('sensing_askandwait', {'QUESTION': q})
def answer(): return N('sensing_answer')
def pen_clear(): return N('pen_clear')
def pen_down(): return N('pen_penDown')
def pen_up(): return N('pen_penUp')
def pen_color(c): return N('pen_setPenColorToColor', {'COLOR': c})
def pen_size(s): return N('pen_setPenSizeTo', {'SIZE': s})

def svg_size(svg):
    m = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', svg)
    return float(m.group(1)), float(m.group(2))

class Target:
    def __init__(self, name, is_stage=False, x=0, y=0, size=100, visible=True):
        self.name, self.is_stage, self.x, self.y, self.size, self.visible = name, is_stage, x, y, size, visible
        self.vars, self.lists, self.scripts, self.notes, self.costumes = [], [], [], [], []
    def var(self, name, value=0):
        v = Var(name, value); self.vars.append(v); return v
    def list(self, name, items=()):
        v = Var(name, list(items), True); self.lists.append(v); return v
    def costume(self, name, svg):
        self.costumes.append((name, svg)); return self
    def script(self, *blocks):
        self.scripts.append(list(blocks)); return self
    def todo(self, text):
        """A free-floating workspace comment (used for TODO notes)."""
        self.notes.append(text); return self

class Project:
    def __init__(self, title):
        self.title = title
        self.stage = Target('Stage', is_stage=True)
        self.sprites, self.broadcasts, self.monitors, self.extensions = [], {}, [], set()
    def sprite(self, name, **kw):
        t = Target(name, **kw); self.sprites.append(t); return t
    def show_var(self, v, x, y, owner=None):
        self.monitors.append((v, x, y, owner))

    # ---- compile ----
    def _bid(self, name):
        if name not in self.broadcasts: self.broadcasts[name] = uid('m')
        return self.broadcasts[name]

    def _compile_target(self, t):
        blocks, comments = {}, {}
        def lit(kind, v):
            if isinstance(v, Var):
                return [13 if v.is_list else 12, v.name, v.id]
            return [kind, str(v) if v is not None else DEFAULTS[kind]]
        def emit(node, parent, top=None):
            bid = uid()
            if node.op.startswith('pen_'): self.extensions.add('pen')
            b = {'opcode': node.op, 'next': None, 'parent': parent, 'inputs': {}, 'fields': {},
                 'shadow': False, 'topLevel': top is not None}
            if top: b['x'], b['y'] = top
            blocks[bid] = b
            for fname, fval in node.fields.items():
                if isinstance(fval, Var): b['fields'][fname] = [fval.name, fval.id]
                elif fname == 'BROADCAST_OPTION': b['fields'][fname] = [fval, self._bid(fval)]
                else: b['fields'][fname] = fval
            if node.mutation: b['mutation'] = node.mutation
            for iname, kind in SPEC[node.op].items():
                if iname not in node.inputs: continue
                v = node.inputs[iname]
                if kind == 'stack':
                    if v: b['inputs'][iname] = [2, emit_stack(v, bid)]
                elif kind == 'bool':
                    if v is not None: b['inputs'][iname] = [2, emit(v, bid)]
                elif kind == 'bcast':
                    b['inputs'][iname] = [1, [11, v, self._bid(v)]]
                elif isinstance(kind, tuple):
                    _, mop, mfield = kind
                    sid = uid('s')
                    blocks[sid] = {'opcode': mop, 'next': None, 'parent': bid, 'inputs': {},
                                   'fields': {mfield: [v if isinstance(v, str) else '', None]}, 'shadow': True, 'topLevel': False}
                    b['inputs'][iname] = [1, sid] if not isinstance(v, N) else [3, emit(v, bid), sid]
                else:
                    if isinstance(v, N): b['inputs'][iname] = [3, emit(v, bid), [kind, DEFAULTS[kind]]]
                    elif isinstance(v, Var): b['inputs'][iname] = [3, lit(kind, v), [kind, DEFAULTS[kind]]]
                    else: b['inputs'][iname] = [1, lit(kind, v)]
            if node.comment:
                cid = uid('c'); b['comment'] = cid
                comments[cid] = {'blockId': bid, 'x': 0, 'y': 0, 'width': 260, 'height': 120,
                                 'minimized': False, 'text': node.comment}
            return bid
        def emit_stack(nodes, parent, top=None):
            first = prev = None
            for i, n in enumerate(nodes):
                bid = emit(n, parent if i == 0 else prev, top if i == 0 else None)
                if prev: blocks[prev]['next'] = bid
                else: first = bid
                prev = bid
            return first
        y = 40
        for s in t.scripts:
            emit_stack(s, None, (40, y)); y += 90 + 45 * self._height(s)
        for i, text in enumerate(t.notes):
            comments[uid('c')] = {'blockId': None, 'x': 520, 'y': 40 + 200 * i, 'width': 320, 'height': 180,
                                  'minimized': False, 'text': text}
        return blocks, comments

    def _height(self, nodes):
        h = 0
        for n in nodes:
            h += 1
            for iname, kind in SPEC[n.op].items():
                if kind == 'stack' and n.inputs.get(iname): h += self._height(n.inputs[iname]) + 1
        return h

    def build(self, out_path):
        assets, targets = {}, []
        all_t = [self.stage] + self.sprites
        for layer, t in enumerate(all_t):
            blocks, comments = self._compile_target(t)
            costumes = []
            for cname, svg in t.costumes:
                data = svg.encode('utf-8'); md5 = hashlib.md5(data).hexdigest()
                assets[md5 + '.svg'] = data
                w, h = svg_size(svg)
                costumes.append({'name': cname, 'bitmapResolution': 1, 'dataFormat': 'svg', 'assetId': md5,
                                 'md5ext': md5 + '.svg', 'rotationCenterX': w / 2, 'rotationCenterY': h / 2})
            d = {'isStage': t.is_stage, 'name': t.name,
                 'variables': {v.id: [v.name, v.value] for v in t.vars},
                 'lists': {v.id: [v.name, v.value] for v in t.lists},
                 'broadcasts': {}, 'blocks': blocks, 'comments': comments, 'currentCostume': 0,
                 'costumes': costumes, 'sounds': [], 'volume': 100, 'layerOrder': layer}
            if t.is_stage:
                d.update({'tempo': 60, 'videoTransparency': 50, 'videoState': 'on', 'textToSpeechLanguage': None})
            else:
                d.update({'visible': t.visible, 'x': t.x, 'y': t.y, 'size': t.size, 'direction': 90,
                          'draggable': False, 'rotationStyle': 'all around'})
            targets.append(d)
        targets[0]['broadcasts'] = {bid: name for name, bid in self.broadcasts.items()}
        mons = []
        for v, x, y, owner in self.monitors:
            m = {'id': v.id, 'mode': 'list' if v.is_list else 'default',
                 'opcode': 'data_listcontents' if v.is_list else 'data_variable',
                 'params': {'LIST' if v.is_list else 'VARIABLE': v.name}, 'spriteName': owner,
                 'value': v.value, 'width': 160 if v.is_list else 0, 'height': 200 if v.is_list else 0,
                 'x': x, 'y': y, 'visible': True}
            if not v.is_list: m.update({'sliderMin': 0, 'sliderMax': 100, 'isDiscrete': True})
            mons.append(m)
        proj = {'targets': targets, 'monitors': mons, 'extensions': sorted(self.extensions),
                'meta': {'semver': '3.0.0', 'vm': '0.2.0', 'agent': 'idle-machine-lab-scratch sb3build.py'}}
        out_path = Path(out_path); out_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
            def put(name, data):  # fixed timestamp so rebuilds are byte-identical
                zi = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, data)
            put('project.json', json.dumps(proj, separators=(',', ':')))
            for name, data in sorted(assets.items()): put(name, data)
        return proj
