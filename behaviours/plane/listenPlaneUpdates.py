from spade.behaviour import CyclicBehaviour
from classes.enums import PlaneState

class listenPlaneUpdatesBehav(CyclicBehaviour):

    async def on_start(self):
        self.state = self.get("state")

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "update":
                if self.state == PlaneState.LANDED:
                    self.state = PlaneState.FLYING
                else:
                    self.state = PlaneState.LANDED
                    # TODO - wait 30~ sec before sending new TAKEOFF request