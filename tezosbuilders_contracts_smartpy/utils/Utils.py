import smartpy as sp


#
# Utility functions
#

#CONTRACT_ADDRESS_LOW = sp.address("KT18amZmM5W7qDWVt2pH6uj7sCEd3kbzLrHT")
#CONTRACT_ADDRESS_HIGH = sp.address("KT1XvNYseNDJJ6Kw27qhSEDF8ys8JhDopzfG")


def isPowerOfTwoMinusOne(x) -> sp.Expr:
    """Returns expression that evaluates to true if x is power of 2 - 1"""
    return ((x + 1) & x) == sp.nat(0)


def sendIfValue(to, amount):
    """Transfer `amount` to `to` if greater 0."""
    with sp.if_(amount > sp.tez(0)):
        sp.send(to, amount)


@sp.inline_result
def openSomeOrDefault(e, default) -> sp.Expr:
    """If option `e` is some, return its value, else return `default`."""
    with e.match_cases() as arg:
        with arg.match("None"):
            sp.result(default)
        with arg.match("Some") as open:
            sp.result(open)


def ifSomeRun(e, f) -> sp.Expr:
    """If option `e` is some, execute function `f`."""
    with e.match("Some") as open: f(open)


def isContract(addr) -> sp.Expr:
    """Returns expression that checks if `addr` is a contract address.

    In a packed address, the 7th byte is 0x01 for originated accounts
    and 0x00 for implicit accounts. The 8th byte is the curve. FYI."""
    #return (addr >= CONTRACT_ADDRESS_LOW) & (addr <= CONTRACT_ADDRESS_HIGH) # prob best not to.
    return sp.slice(sp.pack(sp.set_type_expr(addr, sp.TAddress)), 6, 1) == sp.some(sp.bytes("0x01"))


def onlyContract(addr):
    """Fails with NOT_CONTRACT if `addr` is not a contract address."""
    sp.verify(isContract(addr), "NOT_CONTRACT")


def validateIpfsUri(metadata_uri):
    """Validate IPFS Uri.

    Basic validation, try to make sure it's a somewhat valid ipfs URI.
    Ipfs cid v0 + proto is 53 chars."""
    sp.verify((sp.slice(sp.set_type_expr(metadata_uri, sp.TBytes), 0, 7) == sp.some(sp.utils.bytes_of_string("ipfs://")))
        & (sp.len(sp.set_type_expr(metadata_uri, sp.TBytes)) >= sp.nat(53)), "INVALID_METADATA")


def allCharsInSetOfValidChars(string, valid_set):
    """Verify all characters in a string are in the set of valid characters.
    
    NOTE: Assumes valid_set only contains single characters."""
    string = sp.set_type_expr(string, sp.TString)
    valid_set = sp.set_type_expr(valid_set, sp.TSet(sp.TString))
    with sp.for_("index", sp.range(0, sp.len(string))) as index:
        with sp.if_(~valid_set.contains(sp.slice(string, index, 1).open_some(sp.unit))):
            sp.failwith("INVALID_CHAR")