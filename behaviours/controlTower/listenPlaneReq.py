from spade.behaviour import CyclicBehaviour
from spade.message import Message
from classes.enums import Action
import jsonpickle

class listenPlaneReqBehav(CyclicBehaviour):

    async def on_start(self):
        self.multi = self.get("multi_mode")

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            # Received valid LANDING/TAKEOFF request
            if performative == "request":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId())

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "request")
                await self.send(dashboard_msg)

                # Convert PlaneRequestFull into PlaneRequest (ignore company, origin and destination)
                req = msg_data.toPlaneRequest()

                # If LANDING request
                if msg_data.getRequestAction() == Action.LANDING:

                    # Get number of landing planes on queue
                    n_landing = len(self.agent.landing_queue)
                    if self.multi:
                        n_landing = len(list(filter(lambda req: req.getRequestAction() == Action.LANDING, self.agent.multi_queue)))

                    # If queue not full
                    if n_landing < self.get("max_landing_queue"):
                        
                        # Confirm LANDING with Plane
                        plane_msg = Message(to=plane_id)
                        plane_msg.set_metadata("performative", "ok")
                        await self.send(plane_msg)

                        # Add request to queue
                        if self.multi:
                            self.agent.multi_queue.append(req)
                        else:
                            self.agent.landing_queue.append(req)
                    
                    # If queue full
                    else:
                        # Refuse Plane LANDING
                        plane_msg = Message(to=plane_id)
                        plane_msg.set_metadata("performative", "refuse")
                        await self.send(plane_msg)

                        # Notify Dashboard
                        dashboard_msg = Message(to=self.get("dashboard_jid"))
                        dashboard_msg.body = plane_id
                        dashboard_msg.set_metadata("performative", "refuse")
                        await self.send(dashboard_msg)

                # If TAKEOFF request
                else:
                    # Add request to queue
                    if self.multi:
                        self.agent.multi_queue.append(req)
                    else:
                        self.agent.takeoff_queue.append(req)

            # Received cancellation of LANDING request
            elif performative == "cancel_request":

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "cancel_request")
                await self.send(dashboard_msg)

                # Remove request from queue
                if self.multi:
                    self.agent.multi_queue = [req for req in self.agent.multi_queue if str(req.getPlaneId()) != msg.body]
                else:
                    self.agent.landing_queue = [req for req in self.agent.landing_queue if str(req.getPlaneId()) != msg.body]
                