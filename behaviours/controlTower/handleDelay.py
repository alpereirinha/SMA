from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

class handleDelayBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")
            
            ## Process Delay
            if performative == "delay":
                
                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", performative)
                await self.send(dashboard_msg)

                # TODO - queue handling, notify plane, cancel if queue is full