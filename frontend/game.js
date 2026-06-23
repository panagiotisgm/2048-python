
let board = null;  
let score = 0;    

//API calls

// ask the server to create a fresh board and reset the UI
async function startNewGame() {
  const data = await postRequest('/game/new', {});
  board = data.board;
  score = data.score;
  document.getElementById('message').textContent  = '';  // clear win/loss message
  document.getElementById('hint-msg').textContent = '';  // clear hint message
  renderBoard();
}

// send the current board + direction , for new result
async function sendMove(direction) {
  const data = await postRequest('/game/move', { board, direction, score });
  board = data.board;
  score = data.score;
  renderBoard();
  showStatus(data.status);  // check result of game
}

// AIs suggestion for the best move
// API docs: https://docs.anthropic.com/en/api/messages
async function askForHint() {
  document.getElementById('hint-msg').textContent = 'Asking Claude…';  // show loading message
  const data = await postRequest('/game/hint', { board, score });
  document.getElementById('hint-msg').textContent =
    data.move.toUpperCase() + ' — ' + data.reason;
}


//helper sends JSON and returns the response
async function postRequest(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)  
  });
  return response.json(); 
}


function renderBoard() {
  const grid = document.getElementById('grid');
  grid.innerHTML = ''; 

  // loop over every row and column
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const value = board[r][c];
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.textContent = value || '';  // show number or blank if null
      grid.appendChild(cell);
    }
  }

  // update the score display
  document.getElementById('score').textContent = score;
}

//status messages

// show a message when the game is won or lost
function showStatus(status) {
  const msg = document.getElementById('message');
  if      (status === 'won')  msg.textContent = 'You reached 2048. Congrats';
  else if (status === 'lost') msg.textContent = 'No moves left. Fail';
  else                        msg.textContent = ''; 
}

//keyboard controls

// N -> New , H -> hint
document.addEventListener('keydown', function(e) {
  const moves = {
    ArrowLeft: 'left', ArrowRight: 'right',
    ArrowUp: 'up',     ArrowDown: 'down'
  };
  if (moves[e.key]) { e.preventDefault(); sendMove(moves[e.key]); }  // prevent page scrolling
  if (e.key === 'h' || e.key === 'H') askForHint();
  if (e.key === 'n' || e.key === 'N') startNewGame();
});

// start
// kick off a new game as soon as the page loads
startNewGame();