import smartpy as sp

from tz1and_contracts_smartpy.mixins.Administrable import Administrable
from tz1and_contracts_smartpy.mixins import MetaSettings


class MetaSettingsTest(
    Administrable,
    MetaSettings.MetaSettings,
    sp.Contract):
    def __init__(self, administrator):
        sp.Contract.__init__(self)

        self.init_storage(
            test_validate = sp.nat(0),
            test_nat = sp.nat(0),
            test_address = administrator
        )

        self.available_settings = [
            ("test_validate", sp.TNat, lambda x: sp.failwith("ERROR")),
            ("test_nat", sp.TNat, None),
            ("test_address", sp.TAddress, None),
        ]

        Administrable.__init__(self, administrator = administrator)
        MetaSettings.MetaSettings.__init__(self)


class MetaSettingsInitError(
    Administrable,
    MetaSettings.MetaSettings,
    sp.Contract):
    def __init__(self, administrator):
        sp.Contract.__init__(self)
        Administrable.__init__(self, administrator = administrator)
        MetaSettings.MetaSettings.__init__(self)


@sp.add_test(name = "MetaSettings_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("Fees contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test MetaSettings")

    scenario.h3("Contract origination")
    meta_settings = MetaSettingsTest(admin.address)
    scenario += meta_settings

    # TODO: Check default
    scenario.verify(meta_settings.data.test_nat == sp.nat(0))
    scenario.verify(meta_settings.data.test_address == admin.address)

    #
    # update_fees
    #
    scenario.h3("update_settings")

    # test_validate - No permission for anyone but admin
    for acc in [alice, bob, admin]:
        meta_settings.update_settings([sp.variant("test_validate", sp.nat(10))]).run(
            sender=acc,
            valid=False,
            exception=("ERROR" if acc is admin else "ONLY_ADMIN"))

    # test_nat - No permission for anyone but admin
    for acc in [alice, bob, admin]:
        meta_settings.update_settings([sp.variant("test_nat", sp.nat(10))]).run(
            sender=acc,
            valid=(True if acc is admin else False),
            exception=(None if acc is admin else "ONLY_ADMIN"))

        if acc is admin: scenario.verify(meta_settings.data.test_nat == sp.nat(10))

    # test_nat - No permission for anyone but admin
    for acc in [alice, bob, admin]:
        meta_settings.update_settings([sp.variant("test_address", alice.address)]).run(
            sender=acc,
            valid=(True if acc is admin else False),
            exception=(None if acc is admin else "ONLY_ADMIN"))

        if acc is admin: scenario.verify(meta_settings.data.test_address == alice.address)

    scenario.h2("Test MetaSettings - InitError")

    scenario.h3("Contract initialisation should fail")

    try:
        meta_settings_init_error = MetaSettingsInitError(admin.address)
        scenario += meta_settings_init_error
        scenario.verify(False)
    except Exception:
        scenario.show("Passed")