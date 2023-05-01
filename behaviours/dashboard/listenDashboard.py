from spade.behaviour import CyclicBehaviour
from classes.enums import Action
import jsonpickle

class listenDashboardBehav(CyclicBehaviour):
    
    async def on_start(self):
        self.actions = {}

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            ## Control Tower received landing/takeoff request
            if performative == "plane_request":
                msg_data = jsonpickle.decode(msg.body)
                print(f'> {msg_data.getRequestAction().name} request received: {msg_data.getPlaneId()}, type {msg_data.getPlaneType().name}.')

            ## Plane cancelled landing request
            elif performative == "cancel_plane_request":
                print(f'> {msg.body} cancelled their landing request and will head to another airport.')

            ## Control Tower confirmed landing/takeoff
            elif performative == "confirm":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId())

                print(f'> {msg_data.getRequestAction().name} approved for {plane_id}.')

                self.actions[plane_id] = msg_data

            ## Control Tower delayed landing
            elif performative == "delay":
                msg_data = jsonpickle.decode(msg.body)
                print(f'> {msg_data.getRequestAction().name} delayed for {msg_data.getPlaneId()}. Issue: {msg_data.getIssue()}')

            ## LANDING: Plane started landing / TAKEOFF: Plane is moving to runway
            elif performative == "start_action":
                plane_id = msg.body
                data = self.actions[plane_id]

                # Plane started landing
                if data.getRequestAction() == Action.LANDING:
                    print(f'> {plane_id} started landing on the runway at {data.getRunwayCoords()}...')

                # Plane is moving to runway
                else:
                    print(f'> {plane_id} is moving from the station at {data.getStationCoords()} to the runway at {data.getRunwayCoords()}...')

            ## LANDING: Plane is moving to station / TAKEOFF: Plane is taking off
            elif performative == "next_action":                
                plane_id = msg.body
                data = self.actions[plane_id]

                # Plane is moving to station
                if data.getRequestAction() == Action.LANDING:
                    print(f'> {plane_id} is moving from the runway at {data.getRunwayCoords()} to the station at {data.getStationCoords()}...')

                # Plane is taking off
                else:
                    print(f'> {plane_id} started taking off from the runway at {data.getRunwayCoords()}...')

            ## LANDING/TAKEOFF concluded
            elif performative == "end_action":
                plane_id = msg.body

                print(f'> {self.actions[plane_id].getRequestAction().name} of {plane_id} concluded.')

                self.actions.pop(plane_id)

                