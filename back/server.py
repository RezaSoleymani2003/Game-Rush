import asyncio
import websockets
import json
from XO import XO 

async def handle_connection(websocket, path):
    xo = XO()
    async for message in websocket:
        try:
            data = json.loads(message)  
            index = int(data["index"])  
            player = data["player"]
            
            i = index // 3
            j = index % 3 
            xo.update_board(player.lower(), i, j)
            
            # print(i, j, flush=True)
            print(xo.board, flush=True)

            winner = xo.check_winner()
            print(f"Winner Check: {winner}", flush=True)
            await websocket.send(json.dumps({"winner": winner}))


            # print(f"Received move: Player {player} at index {index}", flush=True)
            # response = {"status": "received", "index": index, "player": player}
            # await websocket.send(json.dumps(response))
        
        except json.JSONDecodeError:
            print("Received invalid JSON")

start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
