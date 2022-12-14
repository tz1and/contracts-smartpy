import smartpy as sp


# Required mixins: Administrable
class WithdrawMutez:
    @sp.entry_point(parameter_type=sp.TRecord(destination=sp.TAddress, amount=sp.TMutez))
    def withdraw_mutez(self, params):
        """(Admin only) Transfer `amount` mutez to `destination`."""
        self.onlyAdministrator()
        sp.send(params.destination, params.amount)
