from spade.agent import Agent

## Server Setup
XMPP_SERVER = '@sara-pc'
PASSWORD = '1234'

## Plane/Station Types
SHIPPING = 0
PASSENGERS = 1

## Runway Types
LANDING = 0
TAKEOFF = 1
MULTI = 2

## Plane States
FLYING = 0
LANDED = 1

## Station/Runway States
FREE = 0
OCCUPIED = 1

class DashboardAgent(Agent):

    async def setup(self):
        print('Starting Dashboard...')