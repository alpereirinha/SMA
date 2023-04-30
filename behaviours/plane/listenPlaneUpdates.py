from spade.behaviour import CyclicBehaviour
from spade.message import Message
from classes.enums import *
import jsonpickle

class listenPlaneUpdatesBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "update":
                pass
                # After change from FLYING to LANDED, wait 30~ sec before sending new TAKEOFF request

        else:
            pass