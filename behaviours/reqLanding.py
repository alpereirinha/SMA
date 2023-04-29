from spade.behaviour import OneShotBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
import jsonpickle

class reqLandingBehav(OneShotBehaviour):
    
    async def run(self):
        msg = Message(to=self.get("controlTower_jid"))
        #req = PlaneRequest(self.agent.id, self.agent.type, 0)
        #msg.body = jsonpickle.encode(req)
        msg.body = "landing req test"
        msg.set_metadata("performative", "request")
