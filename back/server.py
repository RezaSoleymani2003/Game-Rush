import asyncio
import websockets
import json
from XO import XO 

async def handle_xo(player1_ws, player2_ws):
    xo = XO()
    players = {player1_ws: "X", player2_ws: "O"}
    
    async def relay_moves(player_ws, opponent_ws):
        async for message in player_ws:
            try:
                data = json.loads(message)  
                index = int(data["index"])  
                player = data["player"]
                
                i = index // 3
                j = index % 3 
                xo.update_board(player.lower(), i, j)
                
                print(xo.board, flush=True)

                winner = xo.check_winner()
                print(f"Winner Check: {winner}", flush=True)

                await opponent_ws.send(json.dumps({"index": index, "player": player, "winner": winner}))

            except json.JSONDecodeError:
                print("Received invalid JSON")

    await asyncio.gather(
        relay_moves(player1_ws, player2_ws),
        relay_moves(player2_ws, player1_ws)
    )

waiting_player = None

async def handle_connection(websocket, path):
    global waiting_player

    if waiting_player is None:
        waiting_player = websocket
        await websocket.send(json.dumps({"status": "waiting"}))
    else:
        player1_ws = waiting_player
        player2_ws = websocket
        waiting_player = None
        
        await player1_ws.send(json.dumps({"type": "start", "player": "X"}))
        await player2_ws.send(json.dumps({"type": "start", "player": "O"}))

        await handle_xo(player1_ws, player2_ws)  # Await this function properly

start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
