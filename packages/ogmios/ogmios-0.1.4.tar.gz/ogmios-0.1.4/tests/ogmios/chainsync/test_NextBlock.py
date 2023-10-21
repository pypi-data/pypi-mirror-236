import pytest
from pydantic.error_wrappers import ValidationError

from ogmios.chainsync.NextBlock import _parse_direction, _parse_NextBlock_response
from ogmios.errors import InvalidMethodError, InvalidResponseError
from ogmios.datatypes import Origin
from ogmios.model.model_map import Direction

from test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_NextBlock_origin(client):
    intersection, _, _ = client.find_intersection.execute([Origin()])
    assert isinstance(intersection, Origin)

    my_id = "12345"
    direction, tip, block, id = client.next_block.execute(my_id)
    assert direction == Direction.backward
    assert block == Origin()
    assert id == my_id
    assert tip.height > 0
    assert tip.slot > 0

    direction, _, block, _ = client.next_block.execute()
    assert direction == Direction.forward
    assert block.height == 0
    assert block.era == "byron"

    direction, _, block, _ = client.next_block.execute()
    assert direction == Direction.forward
    assert block.height == 1
    assert block.era == "byron"
