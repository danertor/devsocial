# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, no-self-use
from copy import deepcopy
from typing import List


def remove_registered_at(input_list: List[dict]) -> List[dict]:
    """
    Removes the field 'registered_at' frm a list of connection results, for comparing two results without
    considering the time.
    """
    node_to_remove = 'registered_at'
    output_list = deepcopy(input_list)
    for item in output_list:
        if isinstance(item, dict) and node_to_remove in item:
            del item[node_to_remove]
    return output_list
