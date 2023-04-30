from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.stationInfo import StationInfo
import jsonpickle

class rcvStationInfoBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "confirm":
                msg_data = jsonpickle.decode(msg.body)
                print(msg_data)
                # TODO wait the time...

            elif performative == "delay":
                print(f'Delay {msg.body}.')
                # TODO or cancel if queue full
            
        else:
            pass