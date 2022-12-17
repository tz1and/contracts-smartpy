import smartpy as sp

import tests.mixins.Administrable_tests
import tests.mixins.ContractMetadata_tests

@sp.add_test(name="Mutation_tests_Administrable")
def test():
    s = sp.test_scenario()
    with s.mutation_test() as mt:
        mt.add_scenario("Administrable_tests")

@sp.add_test(name="Mutation_tests_ContractMetadata")
def test():
    s = sp.test_scenario()
    with s.mutation_test() as mt:
        #mt.add_scenario("Administrable_tests") # [error] mutation testing: must refer to same contract across scenarios
        mt.add_scenario("ContractMetadata_tests")