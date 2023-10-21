import pytest
from pydantic.error_wrappers import ValidationError

from ogmios.chainsync.FindIntersection import FindIntersection
from ogmios.datatypes import Origin, Point, Tip, Block
from ogmios.model.model_map import Types
import ogmios.model.ogmios_model as om

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_Origin():
    # Valid origin
    origin = Origin()
    assert origin._schematype == om.Origin.origin


def test_Point():
    # Valid Point
    Point(slot=10, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")

    # Invalid slot
    with pytest.raises(ValidationError):
        Point(slot=-10, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")

    # Invalid id
    with pytest.raises(ValidationError):
        Point(slot=10, id="bad_id")


def test_Tip():
    # Valid Tip
    Tip(slot=10, height=1000, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")

    # Invalid slot
    with pytest.raises(ValidationError):
        Tip(
            slot=-10,
            height=1000,
            id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        )

    # Invalid height
    with pytest.raises(ValidationError):
        Tip(
            slot=10,
            height=-1000,
            id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        )

    # Invalid id
    with pytest.raises(ValidationError):
        Tip(slot=10, height=1000, id="bad_id")


def test_Tip_to_point():
    tip = Tip(
        slot=10, height=1000, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
    )
    point = Point(slot=10, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")
    assert tip.to_point() == point


def test_Block_EBB():
    # Valid EBB block
    kwargs = {
        "era": "byron",
        "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "height": 100,
    }
    Block(Types.ebb.value, **kwargs)

    # Wrong era
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "shelley",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
        }
        Block(Types.ebb.value, **kwargs)

    # Invalid height
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": -100,
        }
        Block(Types.ebb.value, **kwargs)

    # Missing required parameter
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
        }
        Block(Types.ebb.value, **kwargs)


def test_Block_BFT():
    # Valid block
    kwargs = {
        "era": "byron",
        "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "height": 100,
        "slot": 1000,
        "size": {"bytes": 1},
        "transactions": [],  # TODO: Add this type
        "protocol": {
            "id": 123456,
            "version": {"major": 0, "minor": 1, "patch": 2},
            "software": {"appName": "test", "number": 1234},
        },
        "issuer": {
            "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
        },
        "delegate": {
            "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
        },
    }
    Block(Types.bft.value, **kwargs)

    # Wrong era
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "shelley",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "id": 123456,
                "version": {"major": 0, "minor": 1, "patch": 2},
                "software": {"appName": "test", "number": 1234},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
            "delegate": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
        }
        Block(Types.bft.value, **kwargs)

    # Invalid height
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": -100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "id": 123456,
                "version": {"major": 0, "minor": 1, "patch": 2},
                "software": {"appName": "test", "number": 1234},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
            "delegate": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
        }
        Block(Types.bft.value, **kwargs)

    # Missing required parameter
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "id": 123456,
                "version": {"major": 0, "minor": 1, "patch": 2},
                "software": {"appName": "test", "number": 1234},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
            "delegate": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
        }
        Block(Types.bft.value, **kwargs)


def test_Block_Praos():
    # Valid block
    kwargs = {
        "era": "alonzo",
        "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "nonce": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "height": 100,
        "slot": 1000,
        "size": {"bytes": 1},
        "transactions": [],  # TODO: Add this type
        "protocol": {
            "version": {"major": 0, "minor": 1, "patch": 2},
        },
        "issuer": {
            "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "operationalCertificate": {
                "count": 123,
                "kes": {
                    "period": 12,
                    "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                },
            },
            "leaderValue": {},
        },
    }
    Block(Types.praos.value, **kwargs)

    # Wrong era
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "nonce": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "version": {"major": 0, "minor": 1, "patch": 2},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "operationalCertificate": {
                    "count": 123,
                    "kes": {
                        "period": 12,
                        "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                    },
                },
                "leaderValue": {},
            },
        }
        Block(Types.praos.value, **kwargs)

    # Invalid height
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "babbage",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "nonce": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": -100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "version": {"major": 0, "minor": 1, "patch": 2},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "operationalCertificate": {
                    "count": 123,
                    "kes": {
                        "period": 12,
                        "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                    },
                },
                "leaderValue": {},
            },
        }
        Block(Types.praos.value, **kwargs)

    # Missing required parameter
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "shelley",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "version": {"major": 0, "minor": 1, "patch": 2},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "operationalCertificate": {
                    "count": 123,
                    "kes": {
                        "period": 12,
                        "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                    },
                },
                "leaderValue": {},
            },
        }
        Block(Types.praos.value, **kwargs)
