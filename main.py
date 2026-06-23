import os
import json
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import game

load_dotenv()  # load .env file or set variable

app = FastAPI()

# serve static files (html, css, js) from the frontend folder
# at /static/filename e.g. /static/style.css
app.mount("/static", StaticFiles(directory="frontend"), name="static")


class MoveIn(BaseModel):
    board: list       
    direction: str   
    score: int = 0    

class HintIn(BaseModel):
    board: list       
    score: int = 0    

# helper
def status_for(board):
    return game.game_status(board)

# routes 

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.post("/game/new")
def new_game():
    # create a fresh board and return it with score 0
    board = game.reset_board()
    return {"board": board, "score": 0, "status": "still playing"}

@app.post("/game/move")
def move(data: MoveIn):
    try:
        board, points, moved = game.play(data.board, data.direction)
    except ValueError as e:
        # invalid direction sends back a 400 error
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "board": board,
        "score": data.score + points, 
        "moved": moved,                
        "status": status_for(board),
    }

@app.post("/game/hint")
async def hint(data: HintIn):
    # API docs: https://docs.anthropic.com/en/api/messages
    prompt = (
        "You are playing the game 2048. Here is the board (null = empty cell):\n"
        f"{json.dumps(data.board)}\n"
        f"Current score: {data.score}\n\n"
        "Which single move gives the best chance to keep playing and reach 2048?\n"
        'Answer ONLY as JSON: {"move": "left", "reason": "..."}'
    )

    # read the API key from environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # if no key is set, return a default hint instead of crashing
        return {"move": "left", "reason": "No API key set, defaulting to left."}

    try:
        async with httpx.AsyncClient() as client:
            # call the Anthropic Messages API
            # docs: https://docs.anthropic.com/en/api/messages
            # model: claude-haiku
            # anthropic-version: 2023-06-01 — the current stable API version
            r = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "content-type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",  
                },
                json={
                    "model": "claude-haiku-4-5-20251001",  
                    "max_tokens": 100,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=10,
            )

            # extract the text and parse it as JSON
            text = r.json()["content"][0]["text"].strip()
            answer = json.loads(text)
            return {"move": answer["move"], "reason": answer.get("reason", "")}

    except Exception as e:
        # if the AI call fails for any reason, return a default hint
        # so the game keeps working even without AI
        return {"move": "unavailable", "reason": f"AI hint failed ({e})"}