# CHANGELOG


## v0.12.1 (2024-12-07)

### Bug Fixes

- 🐛 Do not build on Ubuntu 24, yet
  ([`d70b8b3`](https://github.com/getcodelimit/codelimit/commit/d70b8b3ad64132bd07c090b9fc09219e007ec6a0))

### Continuous Integration

- 💚 Do not build on Ubuntu 24, yet
  ([`6a71989`](https://github.com/getcodelimit/codelimit/commit/6a71989ab87f9b3ac479e0f660f2edcdce790f12))


## v0.12.0 (2024-12-07)

### Chores

- 🚨 Fix MyPy issues
  ([`79997a3`](https://github.com/getcodelimit/codelimit/commit/79997a3b09c45801a8a788acc440e2bcbea5baf3))

### Features

- ✨ Include pathspec library ([#49](https://github.com/getcodelimit/codelimit/pull/49),
  [`5239051`](https://github.com/getcodelimit/codelimit/commit/52390511ae8a4dba7bd1820cf639a2f2fb080e94))

Co-authored-by: robvanderleek <robvanderleek@users.noreply.github.com>

- ✨ Move excludes option to check and scan commands
  ([#47](https://github.com/getcodelimit/codelimit/pull/47),
  [`d5ea049`](https://github.com/getcodelimit/codelimit/commit/d5ea049f37327d8b1c3c5de0829a2d97e89b5347))


## v0.11.3 (2024-12-04)

### Bug Fixes

- 🐛 Fix markdown formatting
  ([`e1e57f9`](https://github.com/getcodelimit/codelimit/commit/e1e57f9bc146df79265961319a7e9ae1229eb5a5))

### Chores

- 🚧 Improve markdown report, remove GH App commands
  ([`48656f2`](https://github.com/getcodelimit/codelimit/commit/48656f24e3a1e386323f4ff68da75f09eea5eaa1))


## v0.11.2 (2024-12-03)

### Bug Fixes

- 🐛 Fix markdown output
  ([`63808f6`](https://github.com/getcodelimit/codelimit/commit/63808f653dd08c48425327127b09ebde20171d7b))


## v0.11.1 (2024-12-03)

### Bug Fixes

- 🐛 Handle ignores similar for scan and check commands
  ([`5e98a84`](https://github.com/getcodelimit/codelimit/commit/5e98a8454614b21333b9dae8591954bcb8171980))

- 🩹 Fix Markdown report
  ([`a3552b1`](https://github.com/getcodelimit/codelimit/commit/a3552b1c1f8905c0328c4b74e61235240e98dc2e))

### Performance Improvements

- ⚡️ Store predicates in pattern to prevent deepcopy DFA
  ([`df200f0`](https://github.com/getcodelimit/codelimit/commit/df200f059839987060ed6af1784114998cf09f39))


## v0.11.0 (2024-12-02)

### Features

- ✨ Extend report command with `--totals` and `--format` options
  ([#44](https://github.com/getcodelimit/codelimit/pull/44),
  [`b10c798`](https://github.com/getcodelimit/codelimit/commit/b10c7985013655bf2c78a7a43ae25ad92281e99c))

- ✨ Extend report command with `--totals` and `--format` options
  ([#45](https://github.com/getcodelimit/codelimit/pull/45),
  [`1838968`](https://github.com/getcodelimit/codelimit/commit/1838968b71c04e3a3537108bc14ae50c15e99b3f))

Co-authored-by: robvanderleek <robvanderleek@users.noreply.github.com>


## v0.10.0 (2024-10-16)

### Chores

- Support py3.13 ([#40](https://github.com/getcodelimit/codelimit/pull/40),
  [`b8d0a8e`](https://github.com/getcodelimit/codelimit/commit/b8d0a8e8d2b93055defcc56c7ad57f515f81c1ff))

Signed-off-by: Rui Chen <rui@chenrui.dev>

### Features

- ✨ Colorize output ([#39](https://github.com/getcodelimit/codelimit/pull/39),
  [`5c07214`](https://github.com/getcodelimit/codelimit/commit/5c0721464ff87322ed3a7ef2b68a767e97b570bf))

Co-authored-by: robvanderleek <robvanderleek@users.noreply.github.com>

- ✨ Default path to "." ([#37](https://github.com/getcodelimit/codelimit/pull/37),
  [`9c0ced6`](https://github.com/getcodelimit/codelimit/commit/9c0ced6b87ef8571d21e9f0917a0ba96e959639f))

Co-authored-by: robvanderleek <robvanderleek@users.noreply.github.com>

- ✨ Fix analyze code workflow ([#42](https://github.com/getcodelimit/codelimit/pull/42),
  [`d80e66c`](https://github.com/getcodelimit/codelimit/commit/d80e66c7b371e3407a0067e087a13f93b875d3a0))

- ✨ Support JS arrow notation ([#35](https://github.com/getcodelimit/codelimit/pull/35),
  [`a568145`](https://github.com/getcodelimit/codelimit/commit/a568145a565b5b75c61194d74ee9640c146ff365))

Co-authored-by: robvanderleek <robvanderleek@users.noreply.github.com>


## v0.9.5 (2024-08-10)

### Bug Fixes

- Fix for PyInstaller bundling
  ([`ab43a4c`](https://github.com/getcodelimit/codelimit/commit/ab43a4c66bd401921a9c456df047b491d4170bbb))

- Release workflow
  ([`5ce902f`](https://github.com/getcodelimit/codelimit/commit/5ce902f0c21b0698766175caf3f5fe18deec3187))


## v0.9.4 (2024-08-08)

### Bug Fixes

- Bundle all files
  ([`30ca142`](https://github.com/getcodelimit/codelimit/commit/30ca1427d371d468305ee9c95e083d795271f682))


## v0.9.3 (2024-04-27)

### Bug Fixes

- Always show refactoring candidates
  ([`83e1e13`](https://github.com/getcodelimit/codelimit/commit/83e1e13ec146a2d87e0ea1e0abac6b5a1dc92cf8))

- Do not fail check on unsupported files
  ([`043f06a`](https://github.com/getcodelimit/codelimit/commit/043f06a1026566248851ea6a135da5b039bc5a49))


## v0.9.2 (2024-04-19)

### Bug Fixes

- Another fix check for lexer name in languages
  ([`2cedaee`](https://github.com/getcodelimit/codelimit/commit/2cedaee9e8f5b734f08fe41c4863802bd5de6746))


## v0.9.1 (2024-04-18)

### Bug Fixes

- Drop Python 3.9 support
  ([`b3a84df`](https://github.com/getcodelimit/codelimit/commit/b3a84df165344d0f48b769030548ca2315e3e567))

- Fix check for lexer name in languages
  ([`7716939`](https://github.com/getcodelimit/codelimit/commit/771693957d6c3cb7a510ac0ae1ed60d5d5611b04))

- Quote Python version
  ([`86ad99e`](https://github.com/getcodelimit/codelimit/commit/86ad99ea994ec3bff1b141f5ad6cd3e8b45a2ea3))

- Update lock file
  ([`bdb58ba`](https://github.com/getcodelimit/codelimit/commit/bdb58ba35c231b1342865a2bf6adb8c38741b929))

### Chores

- Use GPL-3.0-or-later and update lic ref ([#33](https://github.com/getcodelimit/codelimit/pull/33),
  [`765ed43`](https://github.com/getcodelimit/codelimit/commit/765ed436c540c4f474d476a576c19af43927c60d))

Signed-off-by: Rui Chen <rui@chenrui.dev>


## v0.9.0 (2024-04-18)

### Features

- ✨ Multi-language support ([#32](https://github.com/getcodelimit/codelimit/pull/32),
  [`96aba04`](https://github.com/getcodelimit/codelimit/commit/96aba04f58a3216444c1cd78654797a58accecbf))

Co-authored-by: robvanderleek <robvanderleek@users.noreply.github.com>


## v0.8.1 (2024-02-29)

### Bug Fixes

- Do not show defaults
  ([`1af54de`](https://github.com/getcodelimit/codelimit/commit/1af54de57f49a2a0ac8e5753894e2f0c870ad0e7))

- Trigger patch release
  ([`6424204`](https://github.com/getcodelimit/codelimit/commit/6424204becd846d8ba18421d5cb1f1c8bcb11964))

- Update docs
  ([`dada84e`](https://github.com/getcodelimit/codelimit/commit/dada84e755af7066ed8433d35958f1366c94b952))

- Update semantic versioning config
  ([`380ada1`](https://github.com/getcodelimit/codelimit/commit/380ada1004a0dd31b69933e55847630da9fadb52))

- Update semantic versioning config
  ([`bed104b`](https://github.com/getcodelimit/codelimit/commit/bed104bdd73692f09b20041a1db1b8ca707d94ec))

### Build System

- Update py3.12 constraint ([#28](https://github.com/getcodelimit/codelimit/pull/28),
  [`95ba321`](https://github.com/getcodelimit/codelimit/commit/95ba3213e55bc04f6633c490c721c6909a5e0aa8))

Signed-off-by: Rui Chen <rui@chenrui.dev>


## v0.8.0 (2024-02-21)


## v0.7.0 (2023-10-07)


## v0.6.2 (2023-08-20)


## v0.6.1 (2023-08-20)


## v0.6.0 (2023-08-17)


## v0.5.0 (2023-08-16)


## v0.4.0 (2023-08-11)


## v0.3.1 (2023-08-10)


## v0.3.0 (2023-08-10)


## v0.2.1 (2023-08-09)

### Bug Fixes

- :bug: Fix readme
  ([`ea4bfa2`](https://github.com/getcodelimit/codelimit/commit/ea4bfa203ce58121384f1985b66de730043547c0))


## v0.2.0 (2023-01-14)

### Features

- :sparkles: Issue 7 add basic repository browser
  ([#8](https://github.com/getcodelimit/codelimit/pull/8),
  [`9645be2`](https://github.com/getcodelimit/codelimit/commit/9645be2e378f15fcfa38e26c8db98e02568a66e3))

* WIP

* Show units in browser

* Fixed tests

* Add source location

* Show code snippet

* Very basic report browser


## v0.1.0 (2023-01-07)

### Features

- :sparkles: WIP ([#6](https://github.com/getcodelimit/codelimit/pull/6),
  [`e792b24`](https://github.com/getcodelimit/codelimit/commit/e792b24a1b79058cc9c09e655eefe04ad3b1c6da))

* WIP

* Hello profiles 👋
