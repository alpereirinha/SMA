from spade.behaviour import CyclicBehaviour
from spade.message import Message
from classes.enums import *
import jsonpickle

class listenDashboardBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            ## Control Tower received landing/takeoff request
            if performative == "plane_request":
                msg_data = jsonpickle.decode(msg.body)
                print('> Received', msg_data)

            ## Plane cancelled landing request
            elif performative == "cancel_plane_request":
                print(f'> {msg.body} cancelled their landing request and will head to another airport.')

            ## Control Tower replied to plane request
            elif performative == "plane_request_reply":
                msg_data = jsonpickle.decode(msg.body)
                print('>', msg_data)

            # elif TODO ...

        else:
            pass