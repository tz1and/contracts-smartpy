import smartpy as sp

Administrable = sp.io.import_script_from_url("file:contracts/mixins/Administrable.py").Administrable
withdraw_mutez_mixin = sp.io.import_script_from_url("file:contracts/mixins/WithdrawMutez.py")


class WithdrawMutezTest(
    Administrable,
    withdraw_mutez_mixin.WithdrawMutez,
    sp.Contract):
    def __init__(self, administrator):
        Administrable.__init__(self, administrator = administrator)
        withdraw_mutez_mixin.WithdrawMutez.__init__(self)


@sp.add_test(name = "WithdrawMutez_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("WithdrawMutez contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test WithdrawMutez")

    scenario.h3("Contract origination")
    withdraw_mutez = WithdrawMutezTest(admin.address)
    withdraw_mutez.set_initial_balance(sp.tez(10))
    scenario += withdraw_mutez

    #
    # withdraw_mutez
    #
    scenario.h3("withdraw_mutez")

    # No permission for anyone but admin
    for acc in [bob, alice, admin]:
        withdraw_mutez.withdraw_mutez(amount=sp.tez(10), destination=admin.address).run(
            sender=acc,
            valid=(True if acc is admin else False),
            exception=(None if acc is admin else "ONLY_ADMIN"))

    # Can't withdraw more than balance. Duh.
    withdraw_mutez.withdraw_mutez(amount=sp.tez(1), destination=admin.address).run(sender=admin, valid=False)