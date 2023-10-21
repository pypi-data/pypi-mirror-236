import pytest
import json
from pydantic.error_wrappers import ValidationError

from ogmios.chainsync.FindIntersection import _parse_FindIntersection_response
from ogmios.errors import InvalidMethodError, InvalidResponseError, ResponseError
from ogmios.datatypes import Origin, Point, Tip

from test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_FindIntersection_origin(client):
    id_str = "My ID string"
    intersection, tip, id = client.find_intersection.execute([Origin()], id_str)

    assert isinstance(intersection, Origin)
    assert isinstance(tip, Tip)
    assert id == id_str


def test_FindIntersection_last_byron_block(client):
    """This test assumes we are connected to the preprod network"""
    point = Point(slot=84242, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")
    intersection, _, _ = client.find_intersection.execute([point, Origin()])
    assert intersection == point


def test_FindIntersection_tip(client):
    """This test assumes we are connected to the preprod network"""
    # Find origin just to get the tip
    _, tip, _ = client.find_intersection.execute([Origin()])
    point = Point(slot=tip.slot, id=tip.id)

    # Now find intersection with the tip
    intersection, _, _ = client.find_intersection.execute([point, Origin()])
    assert intersection == point


def test_FindIntersection_invalid_block(client):
    point = Point(slot=1, id="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
    with pytest.raises(ResponseError):
        _, _, _ = client.find_intersection.execute([point])


def test_FindIntersection_parser_method_error():
    resp_bad_method = {
        "jsonrpc": "2.0",
        "method": "badMethodName",
        "result": {
            "intersection": {
                "slot": 18446744073709552000,
                "id": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
            },
            "tip": {
                "slot": 18446744073709552000,
                "id": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                "height": 18446744073709552000,
            },
        },
        "id": "1234",
    }
    with pytest.raises(InvalidMethodError):
        _parse_FindIntersection_response(resp_bad_method)


def test_FindIntersection_response_error():
    resp_bad_key = {
        "jsonrpc": "2.0",
        "method": "findIntersection",
        "result": {
            "badKeyName": {
                "slot": 18446744073709552000,
                "id": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
            },
            "tip": {
                "slot": 18446744073709552000,
                "id": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                "height": 18446744073709552000,
            },
        },
        "id": "1234",
    }
    with pytest.raises(InvalidResponseError):
        _parse_FindIntersection_response(resp_bad_key)
