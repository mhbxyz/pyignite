# Changelog

## [0.2.0](https://github.com/mhbxyz/pyquick/compare/v0.1.0...v0.2.0) (2026-02-21)


### ⚠ BREAKING CHANGES

* hard-migrate config file name to pyquick.toml
* rename project to PyQuick and migrate to pyqck

### Features

* add cli profile scaffold baseline ([39dcfe5](https://github.com/mhbxyz/pyquick/commit/39dcfe51a28b8837929bc7347f7696dedc9fcbe0))
* Add configuration validation system ([c028212](https://github.com/mhbxyz/pyquick/commit/c028212c0b3c3fa143badf280707750fd73c8c90))
* add dev watcher loop with reload pipeline ([413e2c7](https://github.com/mhbxyz/pyquick/commit/413e2c73e7e63e33aea77d7fd9f9309b32370993))
* add fastapi scaffold template engine ([0e5185b](https://github.com/mhbxyz/pyquick/commit/0e5185b7ccd8e729ebce72f392b182155ff0c8e4))
* add incremental checks strategy for dev loop ([fca4edb](https://github.com/mhbxyz/pyquick/commit/fca4edb4c952084f027593b3c9e90706ddb4aa55))
* add lib profile scaffold baseline ([7189690](https://github.com/mhbxyz/pyquick/commit/7189690168a08567f2ca4e1acc54efb7d045dbf3))
* add pluggable scaffold registry for pyqck new ([30978ee](https://github.com/mhbxyz/pyquick/commit/30978eea68fe9780e90c1d6de170713202f1da59))
* add pyqck install wrapper command ([554d9fd](https://github.com/mhbxyz/pyquick/commit/554d9fd75e695bc7300cb6395bd76ee3e449c3d9))
* add scaffolded health endpoint and baseline test ([555d3c3](https://github.com/mhbxyz/pyquick/commit/555d3c3a20b93ebeb70de4bc97853d7fd38234dd))
* add semi-automated release workflows with manual gates ([d5270b4](https://github.com/mhbxyz/pyquick/commit/d5270b48258319846d0b0414da5585d2f3419c4a))
* add strict pyignite.toml schema and validation ([6ad3ee0](https://github.com/mhbxyz/pyquick/commit/6ad3ee04be1fe7903c4f84ccf03491a5c5b62b2c))
* add structured terminal UX for dev loop ([3d02f8b](https://github.com/mhbxyz/pyquick/commit/3d02f8b6d4a58729a5b04f368a46e9d3bb1a4373))
* add sync alias for dependency install ([a562189](https://github.com/mhbxyz/pyquick/commit/a562189aa0a14c0ff5c64d020325fd2eddc5086e))
* add tooling adapter layer and availability checks ([2dbeee0](https://github.com/mhbxyz/pyquick/commit/2dbeee03bfdd38f0310c473b55fd88a646972bd5))
* add trusted publishing workflows for PyPI release ([846aab7](https://github.com/mhbxyz/pyquick/commit/846aab7d66b708c0c8ad2f25754b4c94ad6607d4))
* automate GitHub releases from version tags ([f5d9162](https://github.com/mhbxyz/pyquick/commit/f5d91629c0e4358a9030d03daab3fe278ac9769c))
* Complete Phase 1 MVP implementation ([0ba15d4](https://github.com/mhbxyz/pyquick/commit/0ba15d4f170572352e58e53b550bf83d9cfc552d))
* enforce src layout in generated fastapi scaffold ([c0c8702](https://github.com/mhbxyz/pyquick/commit/c0c87029caab5b489e1ce495148056613f7f5b75))
* execute python tooling through uv run ([3f8c2fa](https://github.com/mhbxyz/pyquick/commit/3f8c2faf6f5642f3cc466443b45ce37e3e268f00))
* harden run defaults and runtime diagnostics ([3e805fb](https://github.com/mhbxyz/pyquick/commit/3e805fbb3b46712fa2c16366a372305b995b0a58))
* Implement Phase 2 Patch Engine MVP ([62e0a5b](https://github.com/mhbxyz/pyquick/commit/62e0a5b5996b336d8386ae7458f5d6da7bc086bf))
* implement pyignite new scaffold command ([862ba48](https://github.com/mhbxyz/pyquick/commit/862ba48c41d3617cb2cb7e1859dd5864b1982198))
* implement run/test/lint/fmt/check command wrappers ([a5d846b](https://github.com/mhbxyz/pyquick/commit/a5d846bd4181bcd4e3365681b05043f92177a186))
* rename tooling config keys to semantic roles ([615de72](https://github.com/mhbxyz/pyquick/commit/615de72fbd7d8c1debf8ca3e8e1ad8df62fff6de))
* scaffold project structure with CLI stubs and smoke tests ([fc8a69b](https://github.com/mhbxyz/pyquick/commit/fc8a69b56d17c7992312d48097a120abec692732))


### Bug Fixes

* finalize PyQuick naming cleanup ([2f94b93](https://github.com/mhbxyz/pyquick/commit/2f94b935f3c1d03e867a83c973ad4905fbff0456))
* harden manual release preflight checks ([1b4ee03](https://github.com/mhbxyz/pyquick/commit/1b4ee03f4acf3678eab6cdd1e18ed27bb89253e1))
* keep release workflow tree clean after benchmarks ([9755857](https://github.com/mhbxyz/pyquick/commit/975585753efb16650d0f07d1198486f69d9b028e))
* prevent test artifacts from being committed ([a872058](https://github.com/mhbxyz/pyquick/commit/a87205867a06764c85255194a0cab24729c0e260))
* Resolve linting issues and complete check command ([61dbaca](https://github.com/mhbxyz/pyquick/commit/61dbacaa09e790af080009b4ce988394826eeec0))
* resolve memory leak in test_cli.py and update test assertions ([cb6d926](https://github.com/mhbxyz/pyquick/commit/cb6d926a6f890a0eced1ca1e9b5a5a88682a13b1))
* stabilize benchmark guardrails on hosted runners ([aaed9be](https://github.com/mhbxyz/pyquick/commit/aaed9bec299f2a6e08f0ef5a47a7aeed57f87b3f))
* stabilize tests and behavior ([15569b5](https://github.com/mhbxyz/pyquick/commit/15569b5ba99debcda0608428615967a6bbb12c32))
* stream live output for pyqck run ([692a5ca](https://github.com/mhbxyz/pyquick/commit/692a5cac8ae7467a9628aadbda870886ca1592a4))


### Refactoring

* hard-migrate config file name to pyquick.toml ([2a235e6](https://github.com/mhbxyz/pyquick/commit/2a235e6842a16cc3f2dff426caf28dd6a4f5d5f8))
* rename project to PyQuick and migrate to pyqck ([53cae1f](https://github.com/mhbxyz/pyquick/commit/53cae1fab1a4fa76a2ae8d469c22a54ce33c2af4))


### Performance

* add benchmark guardrails and alpha baseline ([943d1fd](https://github.com/mhbxyz/pyquick/commit/943d1fdb60532b0445207a6ae0a3d9a305263c69))


### Documentation

* add alpha feedback intake and triage roadmap ([ed37ce5](https://github.com/mhbxyz/pyquick/commit/ed37ce53e52ed2aed3ad99e0e99c96e62803e4cd))
* add cross-linked navigation across docs sections ([3421d59](https://github.com/mhbxyz/pyquick/commit/3421d59a9240eb48fb5a6b1ec911f8eded0869a4))
* add install guide for pipx and venv usage ([dfc5ba1](https://github.com/mhbxyz/pyquick/commit/dfc5ba1220d1961bb18914ca7875b14deb892235))
* add internal alpha quickstart and troubleshooting guides ([a83bcca](https://github.com/mhbxyz/pyquick/commit/a83bccaa4769cf9d1df743d61acd50d57a7134b5))
* add internal alpha release checklist and gates ([eddf2cd](https://github.com/mhbxyz/pyquick/commit/eddf2cd1ed5a2180389d2299a2e3aa0323d8dac3))
* add project vision README and MIT license ([d538a81](https://github.com/mhbxyz/pyquick/commit/d538a81bd55aa51d75343cd37dcd3a5b145c7394))
* clarify standalone UX and uv delegation model ([f03f2c3](https://github.com/mhbxyz/pyquick/commit/f03f2c33826c38d5bd1b92f6d1606427dfd64a60))
* define profile-template contract v2 ([a6545a5](https://github.com/mhbxyz/pyquick/commit/a6545a58abd15a94b9bf5e8566e33fc0889e3ee9))
* define v1 command contract and defer non-goals ([2add656](https://github.com/mhbxyz/pyquick/commit/2add656b96f3db0dab85694736af30a9f6344941))
* improve README docs navigation links ([d545b6d](https://github.com/mhbxyz/pyquick/commit/d545b6d7b3b5ac15bb783f2dda8f8134e4f432c9))
* rebrand project name to PyIgnite ([5d81851](https://github.com/mhbxyz/pyquick/commit/5d81851a0e312b34ed8809a42b9604c442c6eef1))
* reorganize documentation and simplify README navigation ([2efc394](https://github.com/mhbxyz/pyquick/commit/2efc394e39967b43821143c3158bb3ebb3bd5606))
* reposition messaging to profile-based toolchain ([2988128](https://github.com/mhbxyz/pyquick/commit/29881289dc3f96be149b20f0e179201014ea0dd8))
* Update memory bank context for Phase 2 MVP completion ([e41d5a0](https://github.com/mhbxyz/pyquick/commit/e41d5a02e3f28f3066d5a450f620953de7a636e8))
* update memory bank context with test fixes ([d440e50](https://github.com/mhbxyz/pyquick/commit/d440e505e66a3b3f293e1eddd2ebcaec7e48290f))


### Tests

* add API workflow e2e coverage and failure diagnostics ([4e8edc6](https://github.com/mhbxyz/pyquick/commit/4e8edc65a9f842707a4e0f22b345624d54d9e2d3))
* add cross-profile E2E matrix and failure checks ([e11369f](https://github.com/mhbxyz/pyquick/commit/e11369f2e5429ef07eb4ea35760045f811227ebf))
* add TestPyPI pip/pipx smoke flows ([86f26df](https://github.com/mhbxyz/pyquick/commit/86f26dffb9b27d8f37d83ab08112bcc7e41f1289))
