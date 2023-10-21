from ogmios.errors import InvalidResponseError
import ogmios.model.cardano_model as cm
import ogmios.model.ogmios_model as om
from ogmios.datatypes import Origin, Point, Tip, Block
import ogmios.model.model_map as mm

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def parse_PointOrOrigin(resp: str | dict) -> Point | Origin:
    """Parse a response that contains either a point or an origin.

    :param resp: The response to parse.
    :type resp: str | dict
    :raises InvalidResponseError: If the response is not a valid point or origin.
    :return: The parsed point or origin.
    """
    if isinstance(resp, str):
        assert resp == om.Origin.origin.value
        return Origin()
    else:
        if (slot := resp.get("slot")) and (id := resp.get("id")):
            return Point(slot=slot, id=id)
    raise InvalidResponseError(f"Invalid point: {resp}")


def parse_TipOrOrigin(resp: str | dict) -> Tip | Origin:
    """Parse a response that contains either a tip or an origin.

    :param resp: The response to parse.
    :type resp: str | dict
    :raises InvalidResponseError: If the response is not a valid tip or origin.
    :return: The parsed tip or origin.
    """
    if isinstance(resp, str):
        assert resp == om.Origin.origin.value
        return Origin()
    else:
        if (slot := resp.get("slot")) and (height := resp.get("height")) and (id := resp.get("id")):
            return Tip(slot=slot, height=height, id=id)
    raise InvalidResponseError(f"Invalid tip: {resp}")


def parse_Block(resp: dict) -> cm.BlockEBB | cm.BlockBFT | cm.BlockPraos:
    """Parse a response that contains a block.

    :param resp: The response to parse.
    :type resp: dict
    :raises InvalidResponseError: If the response is not a valid block.
    :return: The parsed block.
    """
    if btype := resp.get("type"):
        if (
            btype == mm.Types.ebb.value
            and (era := resp.get("era")) is not None
            and (id := resp.get("id")) is not None
            and (ancestor := resp.get("ancestor")) is not None
            and (height := resp.get("height")) is not None
        ):
            return Block(blocktype=btype, era=era, id=id, ancestor=ancestor, height=height)
        elif (
            btype == mm.Types.bft.value
            and (era := resp.get("era"))
            and (id := resp.get("id")) is not None
            and (ancestor := resp.get("ancestor")) is not None
            and (height := resp.get("height")) is not None
            and (slot := resp.get("slot")) is not None
            and (size := resp.get("size")) is not None
            and (protocol := resp.get("protocol")) is not None
            and (issuer := resp.get("issuer")) is not None
            and (delegate := resp.get("delegate")) is not None
        ):
            # Optional parameters
            transactions = resp.get("transactions")
            opcert = resp.get("operationalCertificate")

            return Block(
                blocktype=btype,
                era=era,
                id=id,
                ancestor=ancestor,
                height=height,
                slot=slot,
                size=size,
                transactions=transactions,
                operationalCertificates=opcert,
                protocol=protocol,
                issuer=issuer,
                delegate=delegate,
            )
        elif (
            btype == mm.Types.praos.value
            and (era := resp.get("era")) is not None
            and (id := resp.get("id")) is not None
            and (ancestor := resp.get("ancestor")) is not None
            and (height := resp.get("height")) is not None
            and (slot := resp.get("slot")) is not None
            and (size := resp.get("size")) is not None
            and (protocol := resp.get("protocol")) is not None
            and (issuer := resp.get("issuer")) is not None
        ):
            nonce = resp.get("nonce")
            transactions = resp.get("transactions")

            return Block(
                blocktype=btype,
                era=era,
                id=id,
                ancestor=ancestor,
                nonce=nonce,
                height=height,
                size=size,
                slot=slot,
                transactions=transactions,
                protocol=protocol,
                issuer=issuer,
            )
    raise InvalidResponseError(f"Invalid block information: {resp}")
