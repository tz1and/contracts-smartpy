import smartpy as sp


# Required mixins: Administrable
class AdminLambda:
    """NOTE: Initialise AdminLambda after any mixins that update the storage."""
    def __init__(self):
        t_admin_lambda = sp.TLambda(sp.TUnit, sp.TList(sp.TOperation),
            with_storage="read-write", with_operations=True, tstorage=self.storage_type)

        def run_lambda(self, lambda_function):
            """Allows the administrator to run a lambda."""
            self.onlyAdministrator()
            operations = lambda_function(sp.unit)
            sp.add_operations(operations)
        self.run_lambda = sp.entry_point(run_lambda, lazify=False, parameter_type=t_admin_lambda)
