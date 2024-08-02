from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict
import random
import os

app = FastAPI()

class PlayerInput(BaseModel):
    num_players: int
    num_teams: int
    players: List[str]

# This will store the last teams distribution
last_teams: Dict[str, List[List[str]]] = {}

@app.post("/distribute-teams/")
def distribute_teams(player_input: PlayerInput):
    if player_input.num_players != len(player_input.players):
        raise HTTPException(status_code=400, detail="Number of players does not match the length of the players list.")
    if player_input.num_players % player_input.num_teams != 0:
        raise HTTPException(status_code=400, detail="Players cannot be evenly distributed among teams.")

    players = player_input.players.copy()
    random.shuffle(players)
    team_size = player_input.num_players // player_input.num_teams
    teams = [players[i * team_size:(i + 1) * team_size] for i in range(player_input.num_teams)]

    last_teams["teams"] = teams

    return {"teams": teams}

@app.get("/get-teams/")
def get_teams():
    if not last_teams:
        raise HTTPException(status_code=404, detail="No teams have been distributed yet.")
    return last_teams

@app.get("/", response_class=HTMLResponse)
def get_home():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
