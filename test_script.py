from hpcflow_execution import Execution
from hpcflow_execution import test_hybrid_commands


def test_hybrid():

    flow = test_hybrid_commands.remote_flow

    test_output = Execution.run_elements(flow)

    return test_output