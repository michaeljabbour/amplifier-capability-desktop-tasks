# Desktop Tasks

Finish the task. Check the screen that proves it.

For people asking an agent to work in desktop apps. Desktop Tasks makes the agent use observed controls, stay within a clear action budget and verify the final state before calling the work complete.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-desktop-tasks/)

## What you get

- **Know whether it worked.** Separate a click that was attempted from a change that was actually visible afterward.
- **Recover from uncertain screens.** Re-observe when labels and pixels disagree, and stop repeated actions from compounding an ambiguous result.
- **Use the tools you already have.** Apply the method through an available host computer-use tool; install the native adapter only if needed.

## Start here

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-desktop-tasks.git
cd amplifier-skill-desktop-tasks
python3 scripts/capability.py install --dest ~/.agents/skills
```

This installs the portable method and its packaged references into your agent skill folder. If your host uses another folder, pass that path to `--dest`. Start a new session or use your host’s skill refresh so it can discover the installed skill. Optional native tools are installed separately.

Try this first task:

> Use Desktop Tasks to change the sort order in a fictional task app to newest first. First name the visible success condition. Use fresh observed controls, verify the resulting order and report any step you cannot confirm.

## What you need

- Python 3.11 or later for the portable install helper.
- The method needs an agent host with computer-use tools and the necessary OS permissions.
- The optional tool-cua package supplies platform backends; fixture tests alone do not establish live desktop access.
- Installing the skill does not change application state.

For the optional native interface, use a project virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install ./modules/tool-cua
```

## Evidence and limits

Native backend and fixture checks cover action plumbing and recovery logic. Live OS permissions and a successful task in your selected application remain a separate check.

The worked examples on the site are fictional. They illustrate the output and decisions; they are not user results or measured benefit. See [consolidation and runtime boundaries](docs/CONSOLIDATION.md) for retained interfaces and acceptance scope.

## Optional native Amplifier integration

The portable install above is sufficient when your agent already has a working
computer-use surface. The retained `cua` bundle and `tool-cua` package are an
optional adapter, not a second skill-install step.

Use the [native adapter guide](docs/NATIVE-README.md) only when you need that
Amplifier integration. It keeps the original bundle structure, development
commands, fixture smoke test and backend troubleshooting together. Native setup
requires a compatible Amplifier host and the dependencies and OS permissions for
the selected backend. A fixture test does not operate a real desktop.
