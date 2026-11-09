// Copyright 2026 Omega Compute
// SPDX-License-Identifier: Apache-2.0
// Behaviour checks for every solution project (and a "not finished yet" check for starters).
// Each scenario: what the pupil does (answers, key presses, clicks), how long to run, and what must be true.
const said = (st, sprite, text) => st.says.some(s => s.sprite === sprite && (text instanceof RegExp ? text.test(s.text) : s.text === text));
module.exports = {
  'w02-in-think-out': { clicks: [[200, 'Juno']], answers: ['Ana'], ms: 4000,
    check: st => said(st, 'Juno', 'Hi Ana!') },
  'w04-packets': { ms: 6000, check: st => st.vars['packets got'] == 3 && st.says.filter(s => s.sprite === 'Dex' && s.text === 'Got it!').length === 3 },
  'w05-bug-hunt': { ms: 4500, check: st => said(st, 'Kip', 'Hello, Rollo! All fixed.') },
  'w06-packet-relay': { ms: 8000, check: st => said(st, 'Pia', 'Arrived!') && said(st, 'Juno', 'Thank you!') },
  'w07-maze-route': { ms: 6000, check: st => Math.abs(st.pos.Kip.x - 200) < 1 && Math.abs(st.pos.Kip.y + 140) < 1 && said(st, 'Kip', 'I made it to the clinic!') },
  'w09-loop-shapes': { keys: [[2500, 'h']], ms: 5500, check: st => Math.abs(st.pos.Pen.x + 40) < 1 && Math.abs(st.pos.Pen.y + 80) < 1 && st.blocks.Pen.includes('control_repeat') },
  'w10-night-rota': { ms: 6500, check: st => st.vars.turn == 5 && ['Juno', 'Dex', 'Pia', 'Rollo'].every(n => said(st, n, 'My shift!')) },
  'w11-handover': { ms: 7000, check: st => st.vars.count == 10 && said(st, 'Dex', 'Done! I stopped at 10') },
  'w12-share-the-sum': { ms: 5000, check: st => st.vars.total == 40 && said(st, 'Kip', 'The total is 40') },
  'w14-lights-out': { keys: [[1500, 'space'], [3500, 'w'], [5000, 'space']], ms: 7000,
    check: st => st.history.some(h => h.at > 2000 && h.at < 3500 && h.vars['lamps lit'] == 0) && st.vars['lamps lit'] == 5 && st.vars.network === 'web' },
  'w16-vote-counter': { answers: ['clinic', 'reading', 'clinic', 'clinic', 'reading'], ms: 4000,
    check: st => st.vars['clinic votes'] == 3 && st.vars['reading votes'] == 2 && st.vars['total votes'] == 5 && said(st, 'Rollo', 'Clinic first! 3 votes.') },
  'w20-copy-compare': { ms: 8000, check: st => st.vars.differences == 1 && said(st, 'Dex', 'Line 3 is different!') },
  'w21-check-number': { answers: ['CAT'], ms: 3000, check: st => st.vars['check number'] == 24 },
  'w22-ledger-keeper': { clicks: [[300, 'Pia']], answers: ['Ana', 'Ben', '2'], ms: 4000,
    check: st => st.lists.ledger.length === 1 && st.lists.ledger[0] === 'Line 1: Ana gives 2 to Ben' },
  'w26-code-machine': { keys: [[300, 'e'], [3800, 'd']], answers: ['HELLO WORLD', 'KHOOR'], ms: 7000,
    check: st => said(st, 'Kip', 'KHOOR ZRUOG') && said(st, 'Kip', 'HELLO') },
  'w27-password-door': { clicks: [[300, 'Door'], [3000, 'Door']], answers: ['1234', 'lamp-river-pickle'], ms: 5500,
    check: st => said(st, 'Door', 'Sorry, that is not it.') && said(st, 'Door', 'Come in!') && st.costume.Door === 'open' },
  'w29-careful-helper': { clicks: [[300, 'Kip'], [3800, 'Kip']], answers: ['here is my address', 'a fun fact about owls'], ms: 7500,
    check: st => said(st, 'Kip', 'Please ask a grown-up first.') && said(st, 'Kip', /^Happy to help!/) },
  'capstone-idle-machine-network': { keys: [[2500, 'space']], ms: 14000,
    check: st => st.vars.checked == 12 && st.lists.results.length === 12 && st.costume['Machine 2'] === 'dark' &&
      said(st, 'Checker', /^Checked 12 jobs\. 0 sent back\.$/) },
};
