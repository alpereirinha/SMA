from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

class listenStationResponseBehav(CyclicBehaviour):
  
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            ## LANDING/TAKEOFF request accepted
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

                # Notify Dashboard that request will start being processed
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "start_process")
                await self.send(dashboard_msg)

                # Redirect info to respective runway, to process the LANDING/TAKEOFF
                runway_msg = Message(to=runway_id)
                runway_msg.body = msg.body
                runway_msg.set_metadata("performative", performative)
                await self.send(runway_msg)

            ## LANDING/TAKEOFF request delayed
            #elif performative == "delay":
            #    dashboard_msg = Message(to=self.get("dashboard_jid"))
            #    dashboard_msg.body = msg.body
            #    dashboard_msg.set_metadata("performative", "delay")
            #    await self.send(dashboard_msg)