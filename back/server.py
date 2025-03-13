import asyncio
import websockets
import json
from games.XO import XO , XO_bot

async def handle_xo_ai_mode(player_ws):
    pass

async def handle_xo_player_mode(player1_ws, player2_ws):
    xo = XO()
    
    async def send_winner():
        winner = XO.check_winner(xo.board)
        if winner != '0':
            await player1_ws.send(json.dumps({"winner": winner}))
            await player2_ws.send(json.dumps({"winner": winner}))

    async def relay_moves(player_ws, opponent_ws):
        async for message in player_ws:
            try:
                data = json.loads(message)  
                index = int(data["index"])  
                player = data["player"]
                
                i = index // 3
                j = index % 3 
                xo.update_board(player, i, j)
                
                print(xo.board, flush=True)


                await opponent_ws.send(json.dumps({"index": index}))
                await send_winner()

            except json.JSONDecodeError:
                print("Received invalid JSON", flush=True)

    await asyncio.gather(
        relay_moves(player1_ws, player2_ws),
        relay_moves(player2_ws, player1_ws)
    )

waiting_player = None


async def handle_connection(websocket, path):
    global waiting_player

    try:
        message = await websocket.recv()  
        print(f"Received: {message}", flush=True)

        data = json.loads(message)
        mode = data.get("mode")  

        if waiting_player is None:
            print("First player connected, waiting for opponent...", flush=True)
            waiting_player = websocket
            await websocket.send(json.dumps({"status": "waiting"}))

            if mode == "ai mode":
                print("AI Mode selected, starting AI game...", flush=True)
                await handle_xo_ai_mode(waiting_player) 
            else:
                await asyncio.Future()  

        else:
            if mode == "ai mode":
                await handle_xo_ai_mode(waiting_player) 
                await asyncio.Future()  

            else:
                print("Second player connected, starting game...", flush=True)
                player1_ws = waiting_player  
                player2_ws = websocket      
                waiting_player = None  

                await player1_ws.send(json.dumps({"player init": "X"}))
                await player2_ws.send(json.dumps({"player init": "O"}))

                await handle_xo_player_mode(player1_ws, player2_ws)

    except Exception as e:
        print(f"Connection handler failed: {e}", flush=True)

start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()