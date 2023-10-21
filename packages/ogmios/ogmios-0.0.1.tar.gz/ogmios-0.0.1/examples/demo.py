from __future__ import annotations

import time
import ogmios

"""
This example shows how to use the ogmios-python library to view new blocks as they are added to the 
blockchain.
"""


def live_block_viewer():
    with ogmios.Client() as client:
        # Set chain pointer to origin
        _, tip, _ = client.find_intersection.execute([ogmios.Origin()])

        # Now set chain pointer to tip
        _, _, _ = client.find_intersection.execute([tip.to_point()])

        # # Tail blockchain as new blocks come in beyond the current tip
        while True:
            client.next_block.execute()
            time.sleep(1)


if __name__ == "__main__":
    live_block_viewer()
