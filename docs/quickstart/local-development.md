# Local development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip pytest
python -m unittest discover -s tests
pytest -q
```

Run both commands: this repository includes tests collected by `unittest` and additional tests that are only collected by `pytest`.
