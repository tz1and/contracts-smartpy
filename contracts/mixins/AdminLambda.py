import smartpy as sp


t_admin_lambda = sp.TLambda(sp.TUnit, sp.TList(sp.TOperation), with_storage="read-write", with_operations=True)


# Required mixins: Administrable
class AdminLambda:
    @sp.entry_point
    def run_lambda(self, lambda_function):
        """Allows the administrator to run a lambda."""
        sp.set_type(lambda_function, t_admin_lambda)
        self.onlyAdministrator()
        operations = lambda_function(sp.unit)
        sp.add_operations(operations)
