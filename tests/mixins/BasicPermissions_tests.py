import smartpy as sp

from tz1and_contracts_smartpy.mixins.Administrable import Administrable
from tz1and_contracts_smartpy.mixins import BasicPermissions


class BasicPermissionsTest(
    Administrable,
    BasicPermissions.BasicPermissions,
    sp.Contract):
    def __init__(self, administrator):
        sp.Contract.__init__(self)
        Administrable.__init__(self, administrator = administrator)
        BasicPermissions.BasicPermissions.__init__(self)

    @sp.entry_point
    def testOnlyAdministratorOrPermitted(self):
        self.onlyAdministratorOrPermitted()

    @sp.entry_point
    def testOnlyPermitted(self):
        self.onlyPermitted()

    @sp.entry_point
    def testIsPermitted(self, address):
        sp.verify(self.isPermitted(address), "NOT_PERMITTED")


@sp.add_test(name = "BasicPermissions_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("BasicPermissions contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test BasicPermissions")

    scenario.h3("Contract origination")
    basic_permissions = BasicPermissionsTest(admin.address)
    scenario += basic_permissions

    #
    # manage_permissions
    #
    scenario.h3("manage_permissions")

    # test manage_permissions
    scenario.verify(basic_permissions.data.permitted_accounts.contains(alice.address) == False)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(bob.address) == False)

    basic_permissions.manage_permissions([sp.variant("add_permissions", sp.set([alice.address]))]).run(sender=bob, valid=False, exception="ONLY_ADMIN")
    basic_permissions.manage_permissions([sp.variant("add_permissions", sp.set([bob.address]))]).run(sender=alice, valid=False, exception="ONLY_ADMIN")

    basic_permissions.manage_permissions([sp.variant("add_permissions", sp.set([bob.address]))]).run(sender=admin)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(alice.address) == False)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(bob.address) == True)

    basic_permissions.manage_permissions([sp.variant("add_permissions", sp.set([alice.address]))]).run(sender=admin)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(alice.address) == True)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(bob.address) == True)

    basic_permissions.manage_permissions([sp.variant("remove_permissions", sp.set([bob.address, alice.address]))]).run(sender=admin)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(alice.address) == False)
    scenario.verify(basic_permissions.data.permitted_accounts.contains(bob.address) == False)

    scenario.h3("testOnlyAdministratorOrPermitted")

    for acc in [admin, alice, bob]:
        basic_permissions.testOnlyAdministratorOrPermitted().run(
            sender=acc,
            valid=(True if acc is admin else False),
            exception=(None if acc is admin else "NOT_PERMITTED"))

    basic_permissions.manage_permissions([sp.variant("add_permissions", sp.set([alice.address, bob.address]))]).run(sender=admin)

    for acc in [admin, alice, bob]:
        basic_permissions.testOnlyAdministratorOrPermitted().run(sender=acc)

    scenario.h3("testOnlyPermitted")

    for acc in [admin, alice, bob]:
        basic_permissions.testOnlyPermitted().run(
            sender=acc,
            valid=(False if acc is admin else True),
            exception=("NOT_PERMITTED" if acc is admin else None))

    basic_permissions.manage_permissions([sp.variant("remove_permissions", sp.set([alice.address, bob.address]))]).run(sender=admin)

    for acc in [admin, alice, bob]:
        basic_permissions.testOnlyPermitted().run(sender=acc, valid=False, exception="NOT_PERMITTED")

    scenario.h3("testIsPermitted")

    for acc in [admin, alice, bob]:
        basic_permissions.testIsPermitted(acc.address).run(sender=acc, valid=False, exception="NOT_PERMITTED")

    basic_permissions.manage_permissions([sp.variant("add_permissions", sp.set([alice.address, bob.address]))]).run(sender=admin)

    for acc in [admin, alice, bob]:
        basic_permissions.testIsPermitted(acc.address).run(
            sender=acc,
            valid=(False if acc is admin else True),
            exception=("NOT_PERMITTED" if acc is admin else None))
