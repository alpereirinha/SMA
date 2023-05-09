from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

class listenStationInfoBehav(CyclicBehaviour):
  
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            # LANDING/TAKEOFF request accepted
            if performative == "confirm_landing" or performative == "confirm_takeoff":
                msg_data = jsonpickle.decode(msg.body)
                runway_id = str(msg_data.getRunwayId())

                # Remove request from queue
                if self.get("multi_mode"):
                    self.agent.multi_queue.pop(0)
                elif performative == "confirm_landing":
                    self.agent.landing_queue.pop(0)
                elif performative == "confirm_takeoff":
                    self.agent.takeoff_queue.pop(0)

                # Redirect info to respective runway, to process the LANDING/TAKEOFF
                runway_msg = Message(to=runway_id)
                runway_msg.body = msg.body
                runway_msg.set_metadata("performative", performative)
                await self.send(runway_msg)