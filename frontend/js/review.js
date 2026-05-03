function updateStatus(message, className) {
    const statusEl = document.getElementById('status-indicator');
    statusEl.innerText = message;
    statusEl.className = `status ${className}`;
}

function showScore(score) {
    const scoreContainer = document.getElementById('score-container');
    const scoreClass = score >= 80 ? 'score-good' : (score >= 60 ? 'score-ok' : 'score-bad');
    scoreContainer.innerHTML = `<span class="score-badge ${scoreClass}">Score: ${score}</span>`;
}

function submitReview() {
    const code = document.getElementById('code-input').value;
    const language = document.getElementById('language-select').value;
    const btn = document.getElementById('submit-btn');
    const output = document.getElementById('review-output');
    
    if (!code.trim()) {
        alert("Please enter some code to review.");
        return;
    }
    
    btn.disabled = true;
    updateStatus("Connecting...", "connecting");
    output.innerText = "";
    output.classList.add("cursor-blink");
    document.getElementById('score-container').innerHTML = "";
    
    const ws = new WebSocket('ws://localhost:8000/ws/review');
    
    ws.onopen = () => {
        ws.send(JSON.stringify({
            code: code,
            language: language,
            token: getToken()
        }));
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === "started") {
            updateStatus("Streaming...", "streaming");
        } 
        else if (data.type === "chunk") {
            output.innerText += data.content;
            output.scrollTop = output.scrollHeight;
        }
        else if (data.type === "done") {
            output.classList.remove("cursor-blink");
            updateStatus("Complete ✓", "complete");
            showScore(data.score);
            setTimeout(() => { btn.disabled = false; }, 1000);
            ws.close();
        }
        else if (data.type === "error") {
            output.classList.remove("cursor-blink");
            updateStatus("Error", "error");
            alert("Error: " + data.message);
            btn.disabled = false;
        }
    };
    
    ws.onerror = (error) => {
        output.classList.remove("cursor-blink");
        updateStatus("Connection failed", "error");
        btn.disabled = false;
    };
    
    ws.onclose = (event) => {
        output.classList.remove("cursor-blink");
        if (btn.disabled) {
            btn.disabled = false;
            const statusEl = document.getElementById('status-indicator');
            if (statusEl.className.includes('streaming') || statusEl.className.includes('connecting')) {
                updateStatus("Disconnected", "error");
            }
        }
    };
}
