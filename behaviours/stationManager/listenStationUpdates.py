from spade.behaviour import CyclicBehaviour
import jsonpickle

class listenStationUpdatesBehav(CyclicBehaviour):

    async def on_start(self):
        self.runways = self.get("runways")
        self.stations = self.get("stations")

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "update_station":
                msg_data = jsonpickle.decode(msg.body)
                coords = msg_data.getCoordinates()
                plane_id = str(msg_data.getPlaneId())

                self.stations[coords].setPlane(plane_id)

            if performative == "update_runway":
                msg_data = jsonpickle.decode(msg.body)
                coords = msg_data.getCoordinates()
                plane_id = str(msg_data.getPlaneId())

                self.runways[coords].setPlane(plane_id)