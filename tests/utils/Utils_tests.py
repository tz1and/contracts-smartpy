import smartpy as sp

from contracts_smartpy.utils import Utils


class UtilsTest(sp.Contract):
    def __init__(self):
        self.init_storage()

    @sp.entry_point
    def testIsContract(self, address, expected):
        sp.verify(Utils.isContract(address) == expected)

    @sp.entry_point
    def testOnlyContract(self, address):
        Utils.onlyContract(address)

    @sp.entry_point
    def testOpenSomeOrDefault(self, option, default, expected):
        res = Utils.openSomeOrDefault(option, default)
        sp.verify(res == expected)

    @sp.entry_point
    def testIfSomeRun(self):
        Utils.ifSomeRun(sp.some(sp.nat(10)), lambda x: sp.verify(x == sp.nat(10)))
        Utils.ifSomeRun(sp.set_type_expr(sp.none, sp.TOption(sp.TNat)), lambda x: sp.verify(False))

    @sp.entry_point
    def testValidateIpfsUri(self, uri):
        Utils.validateIpfsUri(uri)

    @sp.entry_point
    def testIsPowerOfTwoMinusOne(self, value, expected):
        sp.verify(Utils.isPowerOfTwoMinusOne(value) == expected)


@sp.add_test(name = "Utils_tests", profile = True)
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

    scenario.h2("Test Fees")

    scenario.h3("Contract origination")
    utils = UtilsTest()
    scenario += utils

    scenario.h3("isContract")

    addresses_validity = [
        (bob.address, False),
        (utils.address, True),
        (sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU"), False),
        (sp.address("tz28KEfLTo3wg2wGyJZMjC1MaDA1q68s6tz5"), False),
        (sp.address("tz3LL3cfMfBV4fPaPZdcj9TjPa3XbvLiXw9V"), False),
        #(sp.address("tz4aL3Z372duFfPawg2wG9TjPa3XbvLiXw9V"), False) # Some day...
        (sp.address("KT1WmMn55RjXwk5Xb4YE6asjy5BvMiEsB6nA"), True),
    ]

    for t in addresses_validity:
        addr, valid = t
        utils.testIsContract(address=addr, expected=valid).run(sender=admin)

    scenario.h3("onlyContract")

    for t in addresses_validity:
        addr, valid = t
        utils.testOnlyContract(addr).run(sender=admin, valid=valid, exception=(None if valid else "NOT_CONTRACT"))

    scenario.h3("testOpenSomeOrDefault")

    utils.testOpenSomeOrDefault(option=sp.some(sp.nat(10)), default=sp.nat(2), expected=sp.nat(10)).run(sender=admin)
    utils.testOpenSomeOrDefault(option=sp.none, default=sp.nat(2), expected=sp.nat(2)).run(sender=admin)

    scenario.h3("testIfSomeRun")

    utils.testIfSomeRun().run(sender=admin)

    scenario.h3("testValidateIpfsUri")

    ipfs_uri_validity = [
        ("", False),
        ("https://newtoken.com", False),
        ("ipfs://newtoken.com", False),
        ("ipfs://QmbWqxBEKC3P8tqsKc98xmWNzrzDtRLMiMPL8wBuTGsMn", False),
        ("ipfs://QmbWqxBEKC3P8tqsKc98xmWNzrzDtRLMiMPL8wBuTGsMnR", True),
        ("ipfs://bafkreicce3xlhin5oyconwqyqxp2pf7fzxf27i77iuh4xiwebvtf3ffqym", True),
        ("ipfs://bafkreibunhe5632xyodlx7r52kzf7aleeh3ttfrodjpowxnjbrxnsgy36u/metadata.json", True),
    ]

    for t in ipfs_uri_validity:
        uri, valid = t
        utils.testValidateIpfsUri(sp.utils.bytes_of_string(uri)).run(sender=admin, valid=valid, exception=(None if valid else "INVALID_METADATA"))

    scenario.h3("testIsPowerOfTwoMinusOne")

    for x in [10, 8, 16, 1048576]:
        utils.testIsPowerOfTwoMinusOne(value=sp.nat(x), expected=False).run(sender=admin)
    
    for x in [3, 7, 63, 127, 1048575]:
        utils.testIsPowerOfTwoMinusOne(value=sp.nat(x), expected=True).run(sender=admin)

    # TODO: sendIfValue