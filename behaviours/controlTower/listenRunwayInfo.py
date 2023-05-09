from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

class listenRunwayInfoBehav(CyclicBehaviour):
  
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            # Redirect Message
            if performative == "redirect":
                data = jsonpickle.decode(msg.body)
                dest = data.getDest()
                
                if '_jid' in dest:
                    new_msg = Message(to=self.get(dest))
                else:
                    new_msg = Message(to=dest)
                    
                new_msg.body = data.getBody()
                new_msg.set_metadata("performative", data.getPerformative())
                await self.send(new_msg)

            # Add to Max Queue
            elif performative == "add_max_queue":
                self.set("max_landing_queue", self.get("max_landing_queue") + 1)

            # Subtract from Max Queue
            elif performative == "sub_max_queue":
                self.set("max_landing_queue", self.get("max_landing_queue") - 1)