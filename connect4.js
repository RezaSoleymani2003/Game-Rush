// const socket = new WebSocket("wss://game-rush-production.up.railway.app/");
const socket = new WebSocket("ws://localhost:8765")

const board = document.getElementById("board");
const popup = document.getElementById("popup");
const mode = document.getElementById("mode");
const game = document.getElementById("game");
const difficulty = document.getElementById("difficulty");



let playerSymbol = null;
let apponentSymbol = null;
let myTurn = false


document.addEventListener("DOMContentLoaded", () => {
    for (let i = 0; i < 42; i++) {
        const cell = document.createElement("div");
        cell.classList.add("cell");
        cell.dataset.index = i;
        board.appendChild(cell);
    }
});



socket.onopen = () => {
    console.log("Connected to server");
    // socket.send("Hello Server!");
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
        if (checkDraw()){
            popup.style.display = "block"; 
            document.getElementById("popup-text").textContent = `It's A Draw!`;
            board.classList.add("disabled");
        }
    }
});

const updateBoard = (index) => {
    const cell = board.querySelector(`[data-index="${index}"]`);
    cell.textContent = apponentSymbol;
}

const finishGame = (winner) => {
    console.log("Winner:", winner); 

    if (winner == "X" || winner == "O") {
        popup.style.display = "block"; 
        document.getElementById("popup-text").textContent = `Player ${winner} Wins!`; 
        board.classList.add("disabled");
    }
    else {
        popup.style.display = "none"; 
    }
};

const closePopup = () => {
    popup.style.display = "none";
    location.reload();
}

const AIMode = () => {
    mode.style.display = "none"
    console.log("chose ai")

    const data = JSON.stringify({ mode: "ai mode" });
    socket.send(data);

    difficulty.style.display = "block"
}

const playerMode = () => {
    game.style.display = "block"
    mode.style.display = "none"
    console.log("chose player")
    
    const data = JSON.stringify({ mode: "player mode" });
    socket.send(data);
}

const setDifficulty = (level, event) => {
    event.preventDefault();

    const data = JSON.stringify({ level: level });
    socket.send(data);
    
    console.log(level)
    
    game.style.display = "block"
    difficulty.style.display = "none"
}

const checkDraw = () => {
    const cells = document.querySelectorAll(".cell");
    return !Array.from(cells).some(cell => cell.textContent.trim() === "");
};