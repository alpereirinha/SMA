from spade.behaviour import CyclicBehaviour
from spade.message import Message
from classes.enums import *
import jsonpickle

class listenDashboardBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "request":
                pass

        else:
            pass