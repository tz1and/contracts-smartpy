# contracts-smartpy

Reusable SmartPy components to build custom contracts.

To test/compile, run SmartPy with modified `PYTHONPATH`:

```
poetry install
source .venv/bin/activate
PYTHONPATH="./" path/to/SmartPy.sh test tests/utils/Utils_tests.py test_output/ --html
```

Or edit `test.sh` and change `SMARTPY_CLI` to point to your SmartPy installation and run it.

For an example/tutorial, see `examples/Counter.py`.

## Contributors

| Contributor | Gratuity |
| --- | --- |
| [852Kerfunkle](https://github.com/852Kerfunkle) | tz1UQpm4CRWUTY9GBxmU8bWR8rxMHCu7jxjV |
