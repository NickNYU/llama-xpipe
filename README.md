---
title: Flash
emoji: 🌖
colorFrom: gray
colorTo: purple
sdk: streamlit
sdk_version: 1.21.0
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

Then, create a new Python virtual environment. The command below creates an environment in `.venv`,
and activates it:

```bash
python -m venv .venv
source .venv/bin/activate
```

if you are in windows, use the following to activate your virtual environment:

```bash
.venv\scripts\activate
```

Install the required dependencies (this will also install gpt-index through `pip install -e .`
so that you can start developing on it):

```bash
pip install -r requirements.txt
```

Now you should be set!

### Validating your Change

Let's make sure to `format/lint` our change. For bigger changes,
let's also make sure to `test` it and perhaps create an `example notebook`.

#### Formatting/Linting

You can format and lint your changes with the following commands in the root directory:

```bash
make format; make lint
```

You can also make use of our pre-commit hooks by setting up git hook scripts:

```bash
pre-commit install
```

We run an assortment of linters: `black`, `ruff`, `mypy`.