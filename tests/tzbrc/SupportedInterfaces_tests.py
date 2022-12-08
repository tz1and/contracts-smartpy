import smartpy as sp

from tezosbuilders_contracts_smartpy.tzbrc import SupportedInterfaces


class SupportedInterfacesTest(
    SupportedInterfaces.SupportedInterfaces,
    sp.Contract):
    def __init__(self, supported_interaces, interface_storage):
        sp.Contract.__init__(self)
        SupportedInterfaces.SupportedInterfaces.__init__(self, supported_interaces, interface_storage)


@sp.add_test(name = "SupportedInterfaces_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("SupportedInterfaces contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test SupportedInterfaces")

    test_interfaces = sp.set([
        sp.pair("TZBRC", sp.nat(1)),
        sp.pair("TZ1", sp.nat(666)),
        sp.pair("VIP", sp.nat(1337))]
    )

    storage_levels = [
        SupportedInterfaces.StorageLevel.BigMap,
        SupportedInterfaces.StorageLevel.TopLevel,
        SupportedInterfaces.StorageLevel.Inline
    ]

    for storage_level in storage_levels:
        scenario.h3(f"With {storage_level}")
        supported_interfaces = SupportedInterfacesTest(test_interfaces, storage_level)
        scenario += supported_interfaces

        #
        # view: supported_interfaces
        #
        scenario.h4("view: supported_interfaces")

        res = scenario.compute(supported_interfaces.supported_interfaces())
        scenario.show(res)
        scenario.verify_equal(res, test_interfaces)