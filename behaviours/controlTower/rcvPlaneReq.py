from spade.behaviour import CyclicBehaviour
from spade.message import Message
from classes.enums import Action
import jsonpickle

class rcvPlaneReqBehav(CyclicBehaviour):
    
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            # Received valid LANDING/TAKEOFF request
            if performative == "request":
                msg_data = jsonpickle.decode(msg.body)

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "plane_request")
                await self.send(dashboard_msg)

                # If LANDING request, confirm it was received
                if msg_data.getRequestAction() == Action.LANDING:
                    plane_msg = Message(to=str(msg_data.getPlaneId()))
                    plane_msg.set_metadata("performative", "ok")
                    await self.send(plane_msg)

                # Convert PlaneRequestFull into PlaneRequest (ignore company, origin and destination)
                req = msg_data.toPlaneRequest()

                # Add to request queue
                self.get("queue").append(req)
                
                # TODO - if req is landing and queue.length > free_stations, send refused instead

            # Received cancellation of LANDING request
            elif performative == "cancel_request":

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "cancel_plane_request")
                await self.send(dashboard_msg)

                # Remove request from queue
                self.set("queue", list(filter(lambda req: str(req.getPlaneId()) != msg.body, self.get("queue"))))
                