const socket = new WebSocket("ws://localhost:8765");

socket.onopen = () => {
    console.log("Connected to server");
    socket.send("Hello Server!");
};

socket.onmessage = (event) => {
    console.log("Received:", event.data);
};

socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};

socket.onclose = (event) => {
    console.log("WebSocket closed:", event);
};


const board = document.getElementById("board");
let currentPlayer = "X";

board.addEventListener("click", (e) => {
    if (e.target.classList.contains("cell") && e.target.textContent === "") {
        e.target.textContent = currentPlayer;
        
        const index = e.target.dataset.index;  
        const data = JSON.stringify({ index: index, player: currentPlayer });

        socket.send(data); 
        
        currentPlayer = currentPlayer === "X" ? "O" : "X";  
    }
});