// Copyright 2026 Omega Compute
// SPDX-License-Identifier: Apache-2.0
// Validate every .sb3: (1) scratch-parser schema check, (2) load in scratch-vm headless,
// (3) run the behaviour scenario: solutions must pass, starters must load (and are expected not to pass yet).
// Usage: node tests/validate.js [projectsDir]
const fs = require('fs'), path = require('path');
const parser = require('scratch-parser');
const VM = require('scratch-vm');
const ScratchStorage = require('scratch-storage').ScratchStorage || require('scratch-storage').default || require('scratch-storage');
const scenarios = require('./scenarios.js');
const dir = process.argv[2] || path.join(__dirname, '..', 'projects');

function parse(buf) { return new Promise((res, rej) => parser(buf, false, (err, out) => err ? rej(err) : res(out))); }
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function run(file, sc) {
  const vm = new VM();
  vm.attachStorage(new ScratchStorage());
  let missing = 0; const w = console.warn; 
  vm.runtime.setCompatibilityMode(true);
  const st = { says: [], history: [] };
  vm.runtime.on('SAY', (target, type, text) => { if (text !== '') st.says.push({ sprite: target.sprite.name, text: String(text), at: Date.now() - t0 }); });
  const answers = [...(sc.answers || [])];
  vm.runtime.on('QUESTION', q => { if (q !== null) setTimeout(() => vm.runtime.emit('ANSWER', answers.length ? answers.shift() : ''), 50); });
  await vm.loadProject(fs.readFileSync(file));
  for (const t of vm.runtime.targets) for (const c of t.getCostumes()) if (!c.asset) missing++;
  st.missingAssets = missing;
  const snap = () => {
    const vars = {}, lists = {}, pos = {}, costume = {}, blocks = {};
    for (const t of vm.runtime.targets) {
      for (const v of Object.values(t.variables)) { if (v.type === '') vars[v.name] = v.value; else if (v.type === 'list') lists[v.name] = [...v.value].map(String); }
      if (!t.isStage) { pos[t.sprite.name] = { x: t.x, y: t.y }; costume[t.sprite.name] = t.getCostumes()[t.currentCostume].name;
        blocks[t.sprite.name] = Object.values(t.blocks._blocks).map(b => b.opcode); }
    }
    return { vars, lists, pos, costume, blocks };
  };
  vm.start(); const t0 = Date.now(); vm.greenFlag();
  const events = [...(sc.keys || []).map(([at, k]) => ({ at, k })), ...(sc.clicks || []).map(([at, s]) => ({ at, s }))].sort((a, b) => a.at - b.at);
  const keyName = k => k === 'space' ? ' ' : k;
  for (let elapsed = 0; elapsed < sc.ms; elapsed += 100) {
    while (events.length && events[0].at <= elapsed) {
      const e = events.shift();
      if (e.k) { vm.postIOData('keyboard', { key: keyName(e.k), isDown: true }); setTimeout(() => vm.postIOData('keyboard', { key: keyName(e.k), isDown: false }), 60); }
      if (e.s) { const t = vm.runtime.getSpriteTargetByName(e.s); vm.runtime.startHats('event_whenthisspriteclicked', null, t); }
    }
    await sleep(100);
    st.history.push({ at: Date.now() - t0, vars: snap().vars });
  }
  Object.assign(st, snap()); vm.stopAll(); vm.quit && vm.quit();
  return st;
}

(async () => {
  const results = []; let failures = 0;
  const slugs = fs.readdirSync(dir).filter(d => fs.statSync(path.join(dir, d)).isDirectory()).sort();
  await Promise.all(slugs.map(async slug => {
    for (const kind of ['starter', 'solution']) {
      const file = path.join(dir, slug, `${slug}-${kind}.sb3`);
      const r = { slug, kind, parser: 'fail', vmLoad: 'fail', behaviour: 'n/a' };
      try { await parse(fs.readFileSync(file)); r.parser = 'ok'; } catch (e) { r.parserError = String(e).slice(0, 300); }
      try {
        const sc = scenarios[slug];
        const st = await run(file, sc || { ms: 1000 });
        r.vmLoad = 'ok';
        if (sc) { let pass = false; try { pass = !!sc.check(st); } catch (e) { pass = false; }
          r.behaviour = pass ? 'pass' : 'not yet'; }
        r.says = st.says.length; r.missingAssets = st.missingAssets; if (st.missingAssets) r.vmLoad = 'assets missing';
      } catch (e) { r.vmError = String(e).slice(0, 300); }
      const ok = r.parser === 'ok' && r.vmLoad === 'ok' && (kind === 'starter' ? r.behaviour !== 'pass' : r.behaviour === 'pass');
      if (!ok) failures++;
      r.ok = ok; results.push(r);
    }
  }));
  results.sort((a, b) => (a.slug + a.kind).localeCompare(b.slug + b.kind));
  for (const r of results) console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.slug.padEnd(32)} ${r.kind.padEnd(8)} parser:${r.parser} vm:${r.vmLoad} behaviour:${r.behaviour}${r.parserError ? ' ' + r.parserError : ''}${r.vmError ? ' ' + r.vmError : ''}`);
  fs.writeFileSync(path.join(dir, '..', 'tests', 'validation-report.json'), JSON.stringify(results, null, 1));
  console.log(`\n${results.length - failures}/${results.length} checks passed`);
  process.exit(failures ? 1 : 0);
})();
