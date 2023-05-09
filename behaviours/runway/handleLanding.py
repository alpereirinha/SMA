from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.msgWrapper import MsgWrapper
from messages.stationUpdate import StationUpdate
import jsonpickle
import asyncio

class handleLandingBehav(CyclicBehaviour):

    async def sendToControlTower(self, data):
        msg = Message(to=self.get("controlTower_jid"))
        msg.body = jsonpickle.encode(data)
        msg.set_metadata("performative", "redirect")
        await self.send(msg)

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")
            
            ## Process LANDING
            if performative == "confirm_landing":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId())

                # Confirm landing (notify dashboard)
                new_msg = MsgWrapper(msg.body, "dashboard_jid", "confirm")
                await self.sendToControlTower(new_msg)

                # Occupy runway (notify station manager)
                body = StationUpdate(plane_id, msg_data.getRunwayCoords())
                new_msg = MsgWrapper(jsonpickle.encode(body), "stationManager_jid", "update_runway")
                await self.sendToControlTower(new_msg)

                # Occupy station (notify station manager)
                body = StationUpdate(plane_id, msg_data.getStationCoords())
                new_msg = MsgWrapper(jsonpickle.encode(body), "stationManager_jid", "update_station")
                await self.sendToControlTower(new_msg)

                # Update max_landing_queue (one less free space) (just for control tower)
                new_msg = Message(to=self.get("controlTower_jid"))
                new_msg.set_metadata("performative", "sub_max_queue")
                await self.send(new_msg)

                # Wait out landing (notify dashboard)
                new_msg = MsgWrapper(plane_id, "dashboard_jid", "start_action")
                await self.sendToControlTower(new_msg)
                await asyncio.sleep(10)

                # Wait out moving from runway to station (notify dashboard)
                new_msg = MsgWrapper(plane_id, "dashboard_jid", "next_action")
                await self.sendToControlTower(new_msg)
                await asyncio.sleep(msg_data.getDistance()/2)

                # Free runway (notify station manager)
                body = StationUpdate('', msg_data.getRunwayCoords())
                new_msg = MsgWrapper(jsonpickle.encode(body), "stationManager_jid", "update_runway")
                await self.sendToControlTower(new_msg)

                # Update Plane State (notify plane)
                new_msg = MsgWrapper(str(msg_data.getStationCoords()), plane_id, "update")
                await self.sendToControlTower(new_msg)

                # Landing concluded (notify dashboard)
                new_msg = MsgWrapper(plane_id, "dashboard_jid", "end_action")
                await self.sendToControlTower(new_msg)
