from __future__ import annotations

from typing import Any, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ogmios.client import Client

from ogmios.errors import InvalidMethodError, InvalidResponseError, ResponseError
from ogmios.logger import logger
from ogmios.datatypes import Origin, Point, Tip
import ogmios.response_handler as rh
import ogmios.model.ogmios_model as om
import ogmios.model.model_map as mm

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


class FindIntersection:
    """Ogmios method to find a point on the blockchain. The first point that is found in the provided list will be returned.

    NOTE: This class is not intended to be used directly. Instead, use the Client.find_intersection method.

    :param client: The client to use for the request.
    :type client: Client
    """

    def __init__(self, client: Client):
        self.client = client
        self.method = mm.Method.findIntersection.value

    def execute(
        self, points: list[Point | Origin], id: Optional[Any] = None
    ) -> (Point | Origin, Tip | Origin, Optional[Any]):
        """Send and receive the request.

        :param points: The list of points to find.
        :type points: list[Point | Origin]
        :param id: The ID of the request.
        :type id: Any
        :return: The intersection, tip, and ID of the response.
        :rtype: (Point | Origin, Tip | Origin, Optional[Any])
        """
        self.send(points, id)
        return self.receive()

    def send(self, points: list[Point | Origin], id: Optional[Any] = None) -> None:
        """Send the request.

        :param points: The list of points to find.
        :type points: list[Point | Origin]
        :param id: The ID of the request.
        :type id: Any
        """
        params = om.Params(points=[point._schematype for point in points])
        pld = om.FindIntersection(
            jsonrpc=self.client.rpc_version,
            method=self.method,
            params=params,
            id=id,
        )
        self.client.send(pld.json())

    def receive(self) -> (Point | Origin, Tip | Origin, Optional[Any]):
        """Receive the response.

        :return: The intersection, tip, and ID of the response.
        :rtype: (Point | Origin, Tip | Origin, Optional[Any])
        """
        response = self.client.receive()
        return _parse_FindIntersection_response(response)


def _parse_FindIntersection_response(response) -> (Point | Origin, Tip | Origin, Optional[Any]):
    if response.get("method") != mm.Method.findIntersection.value:
        raise InvalidMethodError(f"Incorrect method for FindIntersection response: {response}")

    if response.get("error"):
        raise ResponseError(f"Ogmios responded with error: {response}")

    # Successful response will contain intersection, tip, and id
    if result := response.get("result"):
        if (intersection_resp := result.get("intersection")) and (tip_resp := result.get("tip")):
            intersection: Point | Origin = rh.parse_PointOrOrigin(intersection_resp)
            tip: Tip | Origin = rh.parse_TipOrOrigin(tip_resp)
            id: Optional[Any] = response.get("id")
            logger.info(
                f"""Parsed FindIntersection response:
    Point = {intersection}
    Tip = {tip}
    ID = {id}"""
            )
            return intersection, tip, id

    raise InvalidResponseError(f"Failed to parse FindIntersection response: {response}")
