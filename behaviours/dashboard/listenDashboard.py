from spade.behaviour import CyclicBehaviour
from classes.enums import Action
from datetime import datetime
import jsonpickle

class listenDashboardBehav(CyclicBehaviour):
    
    async def on_start(self):
        self.actions = {}

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            ## Control Tower received landing/takeoff request
            if performative == "request":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId()).split("@", 1)[0]
                print(f'{timestamp()} > {msg_data.getRequestAction().name} request received: [ {plane_id} | {msg_data.getPlaneType().name} | {msg_data.getOrigin()} - {msg_data.getDestination()} | {msg_data.getCompany()} ]')

            ## Plane cancelled landing request
            elif performative == "cancel_request":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId()).split("@", 1)[0]
                print(f'{timestamp()} > LANDING *cancelled* for {plane_id}. Plane will head to another airport. ({msg_data.getIssue()})')

            ## Control Tower approved request to queue
            elif performative == "confirm":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId()).split("@", 1)[0]
                print(f'{timestamp()} > {msg_data.getRequestAction().name} *approved* for {plane_id}. Plane is on queue.')

            ## Control Tower refused plane landing
            elif performative == "refuse":
                plane_id = msg.body.split("@", 1)[0]
                print(f'{timestamp()} > LANDING *refused* for {plane_id}. Plane will head to another airport. (Queue Full)')

            ## Control Tower delayed landing/takeoff
            #elif performative == "delay":
            #    msg_data = jsonpickle.decode(msg.body)
            #    plane_id = str(msg_data.getPlaneId()).split("@", 1)[0]
            #    print(f'{timestamp()} > {msg_data.getRequestAction().name} *delayed* for {plane_id}. ({msg_data.getIssue()})')

            ## Runway started processing landing/takeoff
            elif performative == "start_process":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId()).split("@", 1)[0]
                print(f'{timestamp()} > {msg_data.getRequestAction().name} *process started* for {plane_id}.')
                self.actions[plane_id] = msg_data
            
            ## LANDING: Plane started landing / TAKEOFF: Plane is moving to runway
            elif performative == "start_action":
                plane_id = msg.body.split("@", 1)[0]
                data = self.actions[plane_id]
                runway_id = data.getRunwayId().split("@", 1)[0]

                # Plane started landing
                if data.getRequestAction() == Action.LANDING:
                    print(f'{timestamp()} > {plane_id} started landing on the {runway_id}...')

                # Plane is moving to runway
                else:
                    print(f'{timestamp()} > {plane_id} is moving from its station to the {runway_id}... (Estimated Time: {data.getDistance()/2} secs)')

            ## LANDING: Plane is moving to station / TAKEOFF: Plane is taking off
            elif performative == "next_action":                
                plane_id = msg.body.split("@", 1)[0]
                data = self.actions[plane_id]
                runway_id = data.getRunwayId().split("@", 1)[0]

                # Plane is moving to station
                if data.getRequestAction() == Action.LANDING:
                    print(f'{timestamp()} > {plane_id} is moving from the {runway_id} to a station... (Estimated Time: {data.getDistance()/2} secs)')

                # Plane is taking off
                else:
                    print(f'{timestamp()} > {plane_id} started taking off from the {runway_id}...')

            ## LANDING/TAKEOFF concluded
            elif performative == "end_action":
                plane_id = msg.body.split("@", 1)[0]
                print(f'{timestamp()} > {self.actions[plane_id].getRequestAction().name} *concluded* for {plane_id}.')
                self.actions.pop(plane_id)

def timestamp():
    return datetime.now().strftime("[%H:%M:%S]")