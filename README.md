# 2048 Game

A browser-based 2048 game with an AI hint feature.

---

## Project Structure

```
2048-python/
  main.py          # FastAPI server
  game.py          # game logic (board, moves, merging)
  requirements.txt # dependencies
  openshift/       # helm charts
  frontend/
    index.html     # game UI
    style.css      # styling
    game.js        # browser logic
```

---

## Setup

**1. Clone or download the project**

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up your API key:**

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=key-here
```

---

## Running the Game

```bash
uvicorn main:app --reload
```

Then open your browser at:
```
http://localhost:8000
```

---

## Playing

| Control | Action |
|---|---|
| Arrow keys | move tiles |
| `H` | ask Claude for a hint |
| `N` | start a new game |

---

## Requirements

See `requirements.txt`:
```
fastapi
uvicorn==0.34.0
httpx
pydantic==2.13.4
python-dotenv
```

---

## Notes

- The AI hint uses the Claude Haiku model via the Anthropic API
- If no API key is set the game still works, hints will just show a default message
