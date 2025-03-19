import asyncio
import websockets
import json
import time
from games.XO import XO , XO_bot

async def handle_xo_ai_mode(player_ws):
    mapper = {"easy": "random", "medium": "rule based", "hard": "minimax"}
    xo = XO()
    bot = None
    await player_ws.send(json.dumps({"player init": "X"}))
    
    try:
        async for message in player_ws:
            try:
                data = json.loads(message)

                if "level" in data:
                    level = data["level"]
                    bot = XO_bot(mapper[level], xo, "O")
                    print(f"Bot initialized with difficulty: {level}", flush=True)

                elif "index" in data:
                    if bot is None:
                        print("Error: Bot not initialized before receiving moves", flush=True)
                        continue  

                    index = int(data["index"])
                    player = data["player"]

                    i = index // 3
                    j = index % 3
                    xo.update_board(player, i, j)

                    print("Player Move:", xo.board, flush=True)

                    winner = XO.check_winner(xo.board)
                    
                    if winner != '0':
                        await player_ws.send(json.dumps({"winner": winner}))

                    else:
                        bot_move = bot.make_move()
                        xo.update_board("O", bot_move[0], bot_move[1])

                        print("Bot Move:", xo.board, flush=True)
                        time.sleep(0.1) 
                        winner = XO.check_winner(xo.board)
                    
                        if winner != '0':
                            await player_ws.send(json.dumps({"winner": winner}))
                            await player_ws.send(json.dumps({"index": bot_move[0] * 3 + bot_move[1], "player": "O"}))

                        else:
                            if player_ws.open:
                                await player_ws.send(json.dumps({"index": bot_move[0] * 3 + bot_move[1], "player": "O"}))
                            else:
                                print("Client disconnected, stopping AI mode", flush=True)
                                break  

            except json.JSONDecodeError:
                print("Received invalid JSON", flush=True)
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e.code} ({e.reason})", flush=True)
                break  

    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)

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
                waiting_player = None
                await asyncio.Future()  
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

PORT = int(os.getenv("PORT", 443))

start_server = websockets.serve(handle_connection, "0.0.0.0", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()