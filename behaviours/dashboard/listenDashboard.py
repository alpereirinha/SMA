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
                print(f'> Received request for {msg_data.getRequestAction().name}: {msg_data.getPlaneId()}, Type {msg_data.getPlaneType().name}.')

            ## Plane cancelled landing request
            elif performative == "cancel_plane_request":
                print(f'> {msg.body} cancelled their landing request and will head to another airport.')

            ## Control Tower confirmed landing
            elif performative == "confirm_landing":
                msg_data = jsonpickle.decode(msg.body)
                print(f'> LANDING Approved: {msg_data.getPlaneId()} to station at {msg_data.getStationCoords()}.')

            ## Control Tower confirmed takeoff
            elif performative == "confirm_takeoff":
                msg_data = jsonpickle.decode(msg.body)
                print(f'> TAKEOFF Approved: {msg_data.getPlaneId()} to runway at {msg_data.getRunwayCoords()}.')

            ## Control Tower delayed landing
            elif performative == "delay":
                msg_data = jsonpickle.decode(msg.body)
                print(f'> Delayed {msg_data.getRequestAction().name} of {msg_data.getPlaneId()}. Issue: {msg_data.getIssue()}')

            # elif TODO ...