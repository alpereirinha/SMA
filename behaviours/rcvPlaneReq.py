from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
import jsonpickle

class rcvPlaneReqBehav(CyclicBehaviour):
    
    async def run(self):
        msg = await self.receive(timeout=20)

        if msg:
            performative = msg.get_metadata("performative")
            if performative == "request":
                msg_data = jsonpickle.decode(msg.body)
                print(f'Received {msg_data.getRequestType()} from {msg_data.getPlaneJid()}')
                #reply_msg = msg.make_reply()
            else:
                print(f'Agent {self.agent.jid}: Message not understood')
        else:
            print(f'Agent {self.agent.jid}: Did not receive any messages after 20 sec.')