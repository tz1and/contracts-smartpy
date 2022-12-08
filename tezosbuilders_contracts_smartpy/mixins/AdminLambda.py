import smartpy as sp


# Required mixins: Administrable
class AdminLambda:
    """NOTE: Initialise AdminLambda after any mixins that update the storage."""
    def __init__(self):
        self.t_admin_lambda = sp.TLambda(sp.TUnit, sp.TList(sp.TOperation),
            with_storage="read-write", with_operations=True, tstorage=self.storage_type)

    @sp.entry_point(lazify=False)
    def run_lambda(self, lambda_function):
        """Allows the administrator to run a lambda."""
        sp.set_type(lambda_function, self.t_admin_lambda)
        self.onlyAdministrator()
        operations = lambda_function(sp.unit)
        sp.add_operations(operations)
