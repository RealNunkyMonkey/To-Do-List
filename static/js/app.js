document.addEventListener("DOMContentLoaded", () => {
    let ws;

    function connect() {
        ws = new WebSocket(`ws://${window.location.host}/ws`);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const list = document.getElementById("messages");
            const li = document.createElement("li");
            li.textContent = `${data.number}. ${data.text}`;
            list.appendChild(li);
            li.scrollIntoView({behavior: "smooth"});
        };
    }

    const form = document.getElementById("messageForm");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const input = document.getElementById("messageInput");
            if (input.value && ws?.readyState === WebSocket.OPEN) {
                ws.send(input.value);
                input.value = "";
            }
        });
    } else {
        console.error("Элемент #messageForm не найден!");
    }

    connect();
});