import smartpy as sp

from tezosbuilders_contracts_smartpy.mixins.Administrable import Administrable
from tezosbuilders_contracts_smartpy.mixins.MetaSettings import MetaSettings
from tezosbuilders_contracts_smartpy.mixins import Pausable


class PausableTest(
    Administrable,
    Pausable.Pausable,
    sp.Contract):
    def __init__(self, administrator):
        Administrable.__init__(self, administrator = administrator)
        Pausable.Pausable.__init__(self)
        sp.Contract.__init__(self)

    @sp.entry_point
    def testOnlyPaused(self):
        self.onlyPaused()

    @sp.entry_point
    def testOnlyUnpaused(self):
        self.onlyUnpaused()

    @sp.entry_point
    def testIsPaused(self, state):
        sp.set_type(state, sp.TBool)
        with sp.if_(self.isPaused() != state):
            sp.verify(False, "error")


class PausableTestMetaSettings(
    PausableTest,
    MetaSettings):
    def __init__(self, administrator):
        self.available_settings = []

        PausableTest.__init__(self, administrator = administrator)
        MetaSettings.__init__(self)


@sp.add_test(name = "Pausable_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("Pausable contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test Pausable")

    scenario.h3("Contract origination")
    pausable = PausableTest(admin.address)
    scenario += pausable

    scenario.verify(pausable.data.paused == False)

    scenario.h3("set_paused")

    # No permissions to anyone but admin
    for acc in [alice, bob, admin]:
        pausable.set_paused(True).run(
            sender = acc,
            valid = (True if acc is admin else False),
            exception = (None if acc is admin else "ONLY_ADMIN"))

        if acc is admin: scenario.verify(pausable.data.paused == True)

    pausable.set_paused(False).run(sender = admin)
    scenario.verify(pausable.data.paused == False)

    scenario.h3("testOnlyUnpaused")

    for acc in [alice, bob, admin]:
        pausable.testOnlyUnpaused().run(sender = acc)

    pausable.set_paused(True).run(sender = admin)

    for acc in [alice, bob, admin]:
        pausable.testOnlyUnpaused().run(sender = acc, valid = False)

    scenario.h3("testOnlyPaused")

    for acc in [alice, bob, admin]:
        pausable.testOnlyPaused().run(sender = acc)

    pausable.set_paused(False).run(sender = admin)

    for acc in [alice, bob, admin]:
        pausable.testOnlyPaused().run(sender = acc, valid = False)

    scenario.h3("testIsPaused")
    for acc in [alice, bob, admin]:
        pausable.testIsPaused(True).run(sender = acc, valid = False)
        pausable.testIsPaused(False).run(sender = acc)

    scenario.h3("is_paused view")
    scenario.verify(pausable.is_paused() == False)
    pausable.set_paused(True).run(sender = admin)
    scenario.verify(pausable.is_paused() == True)

    # test meta settings
    scenario.h2("Test Pausable - MetaSettings")

    scenario.h3("Contract origination")
    pausable_meta = PausableTestMetaSettings(admin.address)
    scenario += pausable_meta

    scenario.verify(pausable_meta.data.paused == False)

    scenario.h3("update_settings")

    # No permissions to anyone but admin
    for acc in [alice, bob, admin]:
        pausable_meta.update_settings([sp.variant("paused", True)]).run(
            sender = acc,
            valid = (True if acc is admin else False),
            exception = (None if acc is admin else "ONLY_ADMIN"))

        if acc is admin: scenario.verify(pausable_meta.data.paused == True)