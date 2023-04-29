from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
import jsonpickle

SHIPPING = 0
PASSENGERS = 1

LANDING = 0
TAKEOFF = 1

class handleLandingBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            pass
            # rcv station manager answer (free runway, station, queue)

            # send answer to plane
            #reply_msg = msg.make_reply()
            #reply_msg.set_metadata("performative", "accept/delay/reject")
            #await self.send(reply_msg)
                    
            # handle landing with station manager
        else:
            pass