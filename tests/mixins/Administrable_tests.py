import smartpy as sp

from tezosbuilders_contracts_smartpy.mixins import Administrable


class AdministrableTest(Administrable.Administrable, sp.Contract):
    def __init__(self, administrator):
        sp.Contract.__init__(self)
        Administrable.Administrable.__init__(self, administrator = administrator)

    @sp.entry_point
    def testOnlyAdmin(self):
        self.onlyAdministrator()

    @sp.entry_point
    def testIsAdmin(self, address):
        sp.set_type(address, sp.TAddress)
        with sp.if_(~self.isAdministrator(address)):
            sp.verify(False, "error")


@sp.add_test(name = "Administrable_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("Administrable contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test Administrable")

    scenario.h3("Contract origination")
    administrable = AdministrableTest(admin.address)
    scenario += administrable

    scenario.verify(administrable.data.administrator == admin.address)

    scenario.h3("onlyAdministrator")
    # only valid for admin
    for acc in [alice, bob, admin]:
        administrable.testOnlyAdmin().run(sender = acc, valid = (True if acc is admin else False))

    scenario.h3("isAdministrator")
    # never valid
    for acc in [alice, bob, admin]:
        administrable.testIsAdmin(bob.address).run(sender = acc, valid = False)

    # always valid
    for acc in [alice, bob, admin]:
        administrable.testIsAdmin(admin.address).run(sender = acc)

    scenario.h3("transfer_administrator")
    # only admin can transfer admin
    for acc in [alice, bob, admin]:
        administrable.transfer_administrator(bob.address).run(
            sender = acc,
            valid = (True if acc is admin else False),
            exception = (None if acc is admin else "ONLY_ADMIN"))
        
    scenario.verify(administrable.data.proposed_administrator == sp.some(bob.address))

    scenario.h3("accept_administrator")
    # only proposed admin can accept admin
    for acc in [alice, admin, bob]:
        administrable.accept_administrator().run(
            sender = acc,
            valid = (True if acc is bob else False),
            exception = (None if acc is bob else "NOT_PROPOSED_ADMIN"))

    scenario.verify(administrable.data.proposed_administrator == sp.none)
    scenario.verify(administrable.data.administrator == bob.address)
    
    administrable.transfer_administrator(admin.address).run(sender = admin, valid = False, exception = "ONLY_ADMIN")

    # never valid
    for acc in [alice, bob, admin]:
        administrable.accept_administrator().run(sender = acc, valid = False, exception = "NOT_PROPOSED_ADMIN")

    scenario.h3("get_administrator view")

    scenario.verify(administrable.get_administrator() != admin.address)
    scenario.verify(administrable.get_administrator() == bob.address)