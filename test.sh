source .venv/bin/activate

SMARTPY_CLI=path/to/SmartPy.sh

PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/Administrable_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/AdminLambda_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/ContractMetadata_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/MetaSettings_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/Pausable_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/Upgradeable_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/mixins/WithdrawMutez_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/tzbrc/SupportedInterfaces_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test tests/utils/Utils_tests.py test_output/ --html
#PYTHONPATH="./" $SMARTPY_CLI test tests/Mutation_tests.py test_output/ --html
PYTHONPATH="./" $SMARTPY_CLI test examples/Counter_tests.py test_output/ --html
