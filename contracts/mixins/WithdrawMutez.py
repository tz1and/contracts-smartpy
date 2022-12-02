import smartpy as sp


# Required mixins: Administrable
class WithdrawMutez:
    @sp.entry_point
    def withdraw_mutez(self, destination, amount):
        """(Admin only) Transfer `amount` mutez to `destination`."""
        sp.set_type(destination, sp.TAddress)
        sp.set_type(amount, sp.TMutez)
        self.onlyAdministrator()
        sp.send(destination, amount)
