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
                msg_data = jsonpickle.decode(msg.body)
                
                # Notify Plane
                plane_msg = Message(to=msg_data.getPlaneId())
                plane_msg.set_metadata("performative", "delay")
                await self.send(plane_msg)

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", performative)
                await self.send(dashboard_msg)