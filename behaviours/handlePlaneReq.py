from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
import jsonpickle

SHIPPING = 0
PASSENGERS = 1

LANDING = 0
TAKEOFF = 1

class handlePlaneReqBehav(CyclicBehaviour):
    
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")
            
            ## Received valid landing/takeoff request
            if performative == "request":
                msg_data = jsonpickle.decode(msg.body)
                request_type = msg_data.getRequestType()

                ## Process LANDING request
                if request_type == LANDING:
                    print(f'Received landing request from {msg._sender}.')
                    
                    # send req to station manager + handle landing TODO

                ## Process TAKEOFF request
                elif request_type == TAKEOFF:
                    print(f'Received takeoff request from {msg._sender}.')
                    
                    # send req to station manager + handle takeoff TODO

            ## Cancel LANDING request
            elif performative == "cancel_request":
                print(f'{msg._sender} cancelled their landing request and will head to another airport.')

            ## Received invalid request
            else:
                print(f'Invalid Message.')
        
        ## Timed out
        else:
            print(f'Did not receive any requests after 30 sec.')