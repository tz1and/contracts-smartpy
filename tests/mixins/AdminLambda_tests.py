import smartpy as sp

from tezosbuilders_contracts_smartpy.mixins.Administrable import Administrable
from tezosbuilders_contracts_smartpy.mixins import AdminLambda


class AdminLambdaTest(
    Administrable,
    AdminLambda.AdminLambda,
    sp.Contract):
    def __init__(self, administrator):
        self.init_storage(test = sp.nat(10))
        Administrable.__init__(self, administrator = administrator)
        AdminLambda.AdminLambda.__init__(self)


@sp.add_test(name = "AdminLambda_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("AdminLambda contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test AdminLambda")

    scenario.h3("Contract origination")
    admin_lambda = AdminLambdaTest(admin.address)
    scenario += admin_lambda

    #
    # run_lambda
    #
    scenario.h3("run_lambda")

    def update_storage(self, params):
        sp.set_type(params, sp.TUnit)
        self.data.test = sp.nat(20)
        sp.send(admin.address, sp.tez(10))
        sp.result([])

    update_storage_lambda = sp.build_lambda(update_storage, with_storage="read-write", with_operations=True)
    scenario.show(update_storage_lambda)

    # No permission for anyone but admin
    for acc in [bob, alice, admin]:
        admin_lambda.run_lambda(update_storage_lambda).run(
            sender=acc,
            valid=(True if acc is admin else False),
            exception=(None if acc is admin else "ONLY_ADMIN"))

    # Make sure the lambda ran.
    scenario.verify(admin_lambda.data.test == sp.nat(20))