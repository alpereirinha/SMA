from spade.behaviour import OneShotBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
import jsonpickle

class sendPlaneReqBehav(OneShotBehaviour):

    async def on_start(self):
        self.type = self.get("type")
        self.state = self.get("state")
    
    async def run(self):
        msg = Message(to=self.get("controlTower_jid"))
        req = PlaneRequest(self.agent.jid, self.type, 1-self.state) # request opposite of current state
        msg.body = jsonpickle.encode(req)
        msg.set_metadata("performative", "request")
        await self.send(msg)