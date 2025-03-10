const socket = new WebSocket("ws://localhost:8765");
const board = document.getElementById("board");
const popup = document.getElementById("popup");

let playerSymbol = null;
let apponentSymbol = null;
let myTurn = false

socket.onopen = () => {
    console.log("Connected to server");
    socket.send("Hello Server!");
};

socket.onmessage = (event) => {
    console.log("Received:", event.data);
    
    try {
        const data = JSON.parse(event.data);

        if("winner" in data){
            winner = data["winner"]            
            finishGame(winner)
        }
        
        if("index" in data) {  
            const index = data["index"];
            myTurn = true
            updateBoard(index);
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

const updateBoard = (index) => {
    const cell = board.querySelector(`[data-index="${index}"]`);
    cell.textContent = apponentSymbol;
}

const finishGame = (winner) => {
    console.log("Winner:", winner); 

    if (winner == "X" || winner == "O") {
        document.getElementById("popup").style.display = "block"; 
        document.getElementById("popup-text").textContent = `Player ${winner} wins!`; 
    } else {
        document.getElementById("popup").style.display = "none"; 
    }
};


const closePopup = () => {
    popup.style.display = "none";
    location.reload();
}