# Repository handoff

~~~text
Continue work on brainboxemb/template.cad.model-project.

Read AGENTS.md and docs/plan.md first.

Core rules:

- main is stable; dev is the only permanent development source branch;
- short-lived branch -> dev is squash;
- dev -> main promotion is a merge commit;
- main -> dev happens only for real stable-only content, never merely to copy a
  promotion merge commit;
- root ci.yml owns stable toolchain and generated branch configuration;
- root build.yml is the exact work-branch selection;
- main ignores build.yml and runs full;
- internal Python capabilities live under modules/<id>/ and execute from src/;
- CAD models are physical owner roots discovered from model-local ci.yml;
- one owner may expand into multiple build variants;
- generated CAD output is stored on build/{dev,main};
- model.png is implicit; STL and additional snapshots are opt-in model config;
- site/model presentation uses shared Hugo/Hextra layouts;
- model.yml owns presentation metadata, ci.yml owns build/source identity;
- optional page.md and extra_views extend a model page without custom
  model-name branches;
- Pages runs separately and is dispatched after build publication; CI does not wait for it;
- generated `gh-pages` publishes main at `/` and dev at `/dev/`;
- Pages uses branch publication, not `deploy-pages`/`github-pages` environment deployment;
- model-group priority/dependency work is tracked separately after the first
  live model page.
~~~
