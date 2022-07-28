from hpcflow_execution import execution
from hpcflow_execution import test_hybrid_commands


def test_hybrid():

    flow = test_hybrid_commands.remote_flow

    test_output = execution.run_elements(flow)

    return test_output