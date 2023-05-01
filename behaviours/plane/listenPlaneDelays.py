from spade.behaviour import CyclicBehaviour

class listenPlaneDelaysBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "delay":
                pass
                # TODO - retry after 60~ seconds