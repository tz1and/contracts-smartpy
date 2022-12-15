import smartpy as sp

from examples import Counter


# Some *very* basic tests for the Counter contract.
@sp.add_test(name = "Counter_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    bob = sp.test_account("Bob")
    scenario = sp.test_scenario()

    scenario.h1("Counter contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin])

    scenario.h2("Test Counter")

    scenario.h3("Contract origination")
    counter = Counter.Counter(admin.address)
    scenario += counter

    # Verify the defaults.
    scenario.verify(counter.data.counter == sp.nat(0))
    scenario.verify(counter.data.settings.increment == sp.nat(1))

    scenario.h3("update_settings")

    # Increment the settings.
    # NOTE: must be a list, you can update multiple settings in one op!
    counter.update_settings([sp.variant("increment", sp.nat(3))]).run(admin)

    scenario.h3("increment")

    counter.increment().run(admin)

    # Counter should be 3 now!
    scenario.verify(counter.data.counter == sp.nat(3))

    # I'll expand this some day.