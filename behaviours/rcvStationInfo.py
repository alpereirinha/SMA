from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.stationInfo import StationInfo
from classes.enums import *
import jsonpickle

class rcvStationInfoBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "confirm":
                msg_data = jsonpickle.decode(msg.body)
                print(msg_data)
                req_action = msg_data.getRequestAction()

                # Handle LANDING
                if req_action == Action.LANDING:

                    # Confirm landing (notify plane)
                    plane_msg = Message(to=msg_data.getPlaneId())
                    plane_msg.set_metadata("performative", "confirm")
                    await self.send(plane_msg)

                    # Occupy runway (notify station manager)
                    # Wait out landing
                    # Wait out parking in station
                    # Occupy station + free runway (notify station manager)
                    # Update Plane State (notify plane)

                # Handle TAKEOFF
                else:
                    pass
                    # Wait out move to runway
                    # Free station + occupy runway (notify station manager)
                    # Wait out takeoff
                    # Free runway (notify station manager)
                    # Update Plane State (notify plane)

            elif performative == "delay":
                msg_data = jsonpickle.decode(msg.body)
                print(msg_data)

                # TODO - queue handling, notify plane, cancel if queue is full
            
        else:
            pass