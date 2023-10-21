"""This file contains user-friendly datatypes for Ogmios objects.

    Behind the scenes, ogmios-python uses objects derived from the cardano.json and ogmios.json schema files.
    These types are useful for validating that data passed to and from the Ogmios server is properly formatted.
    However, the schema types are not easy to work with. For example, to access the parameters of a schema Tip object:
        slot = tip.slot.__root__
        id = tip.id.__root__
        height = tip.height.__root__

    Other schema types are even more tedious to work with. Therefore, we use intermediate datatypes for user-facing
    functions of this library.
"""
from ogmios.errors import InvalidBlockParameter
import ogmios.model.cardano_model as cm
import ogmios.model.ogmios_model as om
import ogmios.model.model_map as mm

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


class Origin:
    """A class representing the origin of the blockchain.

    The origin is the first block in the blockchain. It is the only block that does not have a parent block.
    """

    def __init__(self):
        self._schematype = om.Origin.origin

    def __eq__(self, other):
        return True if isinstance(other, Origin) else False

    def __str__(self):
        return "Origin()"


class Point:
    """A class representing a point in the blockchain.

    :param slot: The slot number of the point.
    :type slot: int
    :param id: The block hash of the point.
    :type id: str
    """

    def __init__(self, slot: int, id: str):
        self.slot = slot
        self.id = id
        self._schematype = om.PointOrOriginItem(slot=self.slot, id=self.id)

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.slot == other.slot and self.id == other.id:
                return True
        return False

    def __str__(self):
        return f"Point(Slot={self.slot:,}, ID={self.id})"


class Tip:
    """A class representing the tip of the blockchain.

    :param slot: The slot number of the tip.
    :type slot: int
    :param id: The block hash of the tip.
    :type id: str
    :param height: The block height of the tip.
    :type height: int
    """

    def __init__(self, slot: int, id: str, height: int):
        self.slot = slot
        self.id = id
        self.height = height
        self._schematype = om.Tip(slot=self.slot, id=self.id, height=self.height)

    def __eq__(self, other):
        if isinstance(other, Tip):
            if self.slot == other.slot and self.id == other.id and self.height == other.height:
                return True
        return False

    def __str__(self):
        return f"Tip(Slot={self.slot:,}, Height={self.height:,}, ID={self.id})"

    def to_point(self) -> Point:
        """Returns a Point representation of the Tip"""
        return Point(self.slot, self.id)


class Block:
    """
    Represents a block in the blockchain.

    :param blocktype: The type of the block (EBB, BFT, or Praos)
    :type blocktype: ogmios.model.model_map.Types
    :param kwargs: Additional arguments depending on the block type.
    :raises InvalidBlockParameter: If an unsupported block type is provided.
    """

    def __init__(self, blocktype: mm.Types, **kwargs):
        self.blocktype = blocktype
        if blocktype == mm.Types.ebb.value:
            self.era = kwargs.get("era")
            self.id = kwargs.get("id")
            self.ancestor = kwargs.get("ancestor")
            self.height = kwargs.get("height")
            self._schematype = cm.BlockEBB(
                type=self.blocktype,
                era=self.era,
                id=self.id,
                ancestor=self.ancestor,
                height=self.height,
            )
        elif blocktype == mm.Types.bft.value:
            self.era = kwargs.get("era")
            self.id = kwargs.get("id")
            self.ancestor = kwargs.get("ancestor")
            self.height = kwargs.get("height")
            self.slot = kwargs.get("slot")
            self.size = kwargs.get("size")
            self.transactions = kwargs.get("transactions")
            self.protocol = kwargs.get("protocol")
            self.issuer = kwargs.get("issuer")
            self.delegate = kwargs.get("delegate")
            self._schematype = cm.BlockBFT(
                type=self.blocktype,
                era=self.era,
                id=self.id,
                ancestor=self.ancestor,
                height=self.height,
                slot=self.slot,
                size=self.size,
                transactions=self.transactions,
                protocol=self.protocol,
                issuer=self.issuer,
                delegate=self.delegate,
            )
        elif blocktype == mm.Types.praos.value:
            self.era = kwargs.get("era")
            self.id = kwargs.get("id")
            self.ancestor = kwargs.get("ancestor")
            self.nonce = kwargs.get("nonce")
            self.height = kwargs.get("height")
            self.slot = kwargs.get("slot")
            self.size = kwargs.get("size")
            self.transactions = kwargs.get("transactions")
            self.protocol = kwargs.get("protocol")
            self.issuer = kwargs.get("issuer")
            self._schematype = cm.BlockPraos(
                type=self.blocktype,
                era=self.era,
                id=self.id,
                ancestor=self.ancestor,
                height=self.height,
                slot=self.slot,
                size=self.size,
                protocol=self.protocol,
                issuer=self.issuer,
            )
        else:
            raise InvalidBlockParameter(f"Unsupported block type: {blocktype}")

    def __str__(self):
        """
        Returns a string representation of the block.

        :return: A string representation of the block.
        :rtype: str
        """
        if self.blocktype == mm.Types.ebb.value:
            return f"Block(Type=EBB, Era={self.era}, ID={self.id}, Ancestor={self.ancestor}, Height={self.height:,})"
        elif self.blocktype == mm.Types.bft.value:
            return f"Block(Type=BFT, Era={self.era}, ID={self.id}, Ancestor={self.ancestor}, Height={self.height:,}, Slot={self.slot:,}, Size={self.size.get('bytes'):,}, TXs={len(self.transactions)})"
        elif self.blocktype == mm.Types.praos.value:
            return f"Block(Type=Praos, Era={self.era}, ID={self.id}, Ancestor={self.ancestor}, Height={self.height:,}, Slot={self.slot:,}, Size={self.size.get('bytes'):,}, TXs={len(self.transactions)})"
