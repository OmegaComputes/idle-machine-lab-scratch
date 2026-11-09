# Contributing

Thanks for helping with The Idle Machine Lab: Scratch projects. This is a CONCEPT / NOT FINAL draft from Omega Compute.

- Small, focused pull requests are easiest to review. Open an issue first for anything large.
- Run the checks before you push:

  ```sh
  npm ci
  python3 tools/projects.py   # rebuild every .sb3 from source
  npm test                    # parser + scratch-vm load + behaviour checks
  ```


## Changing a project

- Edit `tools/projects.py` (the projects) or `tools/art.py` (the art), never the .sb3 by hand. Then rebuild and test.
- Every project needs a starter (with TODO comments) **and** a solution, plus a behaviour check in `tests/scenarios.js`.
  The solution must pass; the starter must load and must **not** pass yet.
- Pupil text (TODO notes, speech) should read at about US grade 3–4. Short sentences. Plain words.
- Run `python3 tools/make_docs.py` to refresh the teacher pages.

## House rules for all content

- Say **SI** (synthetic intelligence) in story and lesson text, never "AI".
- Story characters (the Alphas and everyone in Kestrel Run) never mention real companies or real people. Real
  systems (Bitcoin, Ethereum, BOINC, IPFS and so on) appear only in clearly marked "In Our World" sections.
- The setting is the fictional town of Kestrel Run. Do not add real towns, counties or real addresses.
- Any phone number in a story prop is a fictional prop number (555 numbers). Never present it as a number to call.
- No prices, no investment advice, no real money and no real wallets. Grown-ups: do not buy crypto for or with children.
- No child accounts, no data collection, no QR codes, no contests, no prizes in pupil-facing material.
- Original art only. Do not add copyrighted images, sounds, characters or fonts.
- Standards: cite codes only. Do not paste standards text.
- Credit stays: "Created by Rian L. Gabrielle", owner Omega Compute.

## Licence of contributions

Code is licensed under the [Apache License 2.0](LICENSE). Text, docs and art are licensed under
[CC BY 4.0](LICENSE-CC-BY-4.0). Unless you state otherwise, a contribution you intentionally submit is licensed
under the licence that covers the file you change (Apache-2.0 section 5 for code), with no additional terms.
By contributing you confirm you have the right to submit it.

Conduct: see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Security: see [SECURITY.md](SECURITY.md).
