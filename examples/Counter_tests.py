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
    scenario.show([admin, bob])

    scenario.h2("Test Counter")

    scenario.h3("Contract origination")
    counter = Counter.Counter(admin = admin.address,
        # For tests, we can just put whatever link into the metadata.
        # The metadata is intended to contain (offchain) information
        # about a contract. To be used by services and indexers and whatnot.
        metadata = sp.utils.metadata_of_url("https://unusedintests.com"),)
    scenario += counter

    # Verify the defaults.
    scenario.verify(counter.data.counter == sp.nat(0))
    scenario.verify(counter.data.settings.increment == sp.nat(1))

    scenario.h3("update_settings")

    # Increment the settings.
    # NOTE: must be a list, you can update multiple settings in one op!
    counter.update_settings([sp.variant("increment", sp.nat(3))]).run(admin)
    scenario.verify(counter.data.settings.increment == sp.nat(3))

    scenario.h3("increment")

    counter.increment().run(admin)
    # Counter should be 3 now!
    scenario.verify(counter.data.counter == sp.nat(3))

    scenario.h3("transfer_administrator")

    # We can transfer the couting powers to bob.
    # Bob is a pretty trustworthy guy. Carol isn't real though.
    counter.transfer_administrator(bob.address).run(admin)

    # Bob needs to accept his mythical admin powers.
    counter.accept_administrator().run(bob)
    scenario.verify(counter.data.administrator == bob.address)

    # Now admin shouldn't be able to count anymore.
    counter.increment().run(admin, valid=False, exception="ONLY_ADMIN")

    # But Bob can...
    counter.increment().run(bob)
    # Counter should be 6 now!
    scenario.verify(counter.data.counter == sp.nat(6))

    # I'll expand this some day. How to do upgrades and all that.