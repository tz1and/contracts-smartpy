import smartpy as sp


class Administrable:
    def __init__(self, administrator, include_views = True):
        self.update_initial_storage(
            administrator = sp.set_type_expr(administrator, sp.TAddress),
            proposed_administrator = sp.set_type_expr(sp.none, sp.TOption(sp.TAddress))
        )

        if include_views:
            def get_administrator(self):
                """Returns the administrator.
                """
                sp.result(self.data.administrator)

            self.get_administrator = sp.onchain_view(pure=True)(get_administrator)

    @sp.entry_point(parameter_type=sp.TAddress)
    def transfer_administrator(self, proposed_administrator):
        """Proposes to transfer the contract administrator to another address.
        """
        self.onlyAdministrator()

        # Set the new proposed administrator address
        self.data.proposed_administrator = sp.some(proposed_administrator)

    @sp.entry_point(parameter_type=sp.TUnit)
    def accept_administrator(self):
        """The proposed administrator accepts the contract administrator
        responsabilities.
        """
        # Check that there is a proposed administrator and
        # check that the proposed administrator executed the entry point
        sp.verify(sp.some(sp.sender) == self.data.proposed_administrator, message="NOT_PROPOSED_ADMIN")

        # Set the new administrator address
        self.data.administrator = sp.sender

        # Reset the proposed administrator value
        self.data.proposed_administrator = sp.none

    # inline helpers
    def isAdministrator(self, address):
        return self.data.administrator == sp.set_type_expr(address, sp.TAddress)

    def onlyAdministrator(self):
        sp.verify(self.isAdministrator(sp.sender), 'ONLY_ADMIN')