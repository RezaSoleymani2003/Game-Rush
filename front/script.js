const socket = new WebSocket("ws://localhost:8765");
let playerSymbol = null;
let apponentSymbol = null;
const board = document.getElementById("board");
let myTurn = false
const popup = document.getElementById("popup");
// popup.style.display = "none"

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
            endGame(winner)
            console.log(popup);

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

const endGame = (winner) => {
    
    const endGame = (winner) => {
        console.log("Winner:", winner); 
    
        if (winner === "X" || winner === "O") {
            popup.style.display = "block"; // Show popup
        } else {
            popup.style.display = "none"; // Hide popup
        }
    };

}

const closePopup = () => {
    popup.style.display = "none";
    location.reload();
}