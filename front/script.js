const socket = new WebSocket("ws://localhost:8765");
let playerSymbol = null;
let apponentSymbol = null;
const board = document.getElementById("board");
let myTurn = false

socket.onopen = () => {
    console.log("Connected to server");
    socket.send("Hello Server!");
};

socket.onmessage = (event) => {
    console.log("Received:", event.data);
    
    try {
        const data = JSON.parse(event.data);

        if("index" in data) {  
            const index = data["index"];
            myTurn = true
            updateBoard(index);

            winner = data["winner"]

            if(winner != "0"){
                endGame(winner)
            }
        }
        
        if("player init" in data){
            playerSymbol = data["player init"]
            
            if (playerSymbol == "X"){
                apponentSymbol = "O"
            }else{
                apponentSymbol = "X"
            }

            console.log("current player: ", playerSymbol)
            console.log("apponent: ", apponentSymbol)

            if(playerSymbol == "X"){
                myTurn = true
            }
        }


    } catch (error) {
        console.error("Error parsing JSON:", error);
    }
};


socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};

socket.onclose = (event) => {
    console.log("WebSocket closed:", event);
};

board.addEventListener("click", (e) => {
    if (myTurn && e.target.classList.contains("cell") && e.target.textContent === "") {
        e.target.textContent = playerSymbol;
        const index = e.target.dataset.index;  
        const data = JSON.stringify({ index: index, player: playerSymbol });
        socket.send(data);    
        myTurn = false
    }
});

updateBoard = (index) => {
    const cell = board.querySelector(`[data-index="${index}"]`);
    cell.textContent = apponentSymbol;
}

endGame = (winner) => {
    
}