import json
from kivy.network.urlrequest import UrlRequest
from urllib.parse import quote

class OnlineLeaderboard:
    def __init__(self):
        # Your specific Firebase URL
        self.url = "https://andazebi-798bd-default-rtdb.europe-west1.firebasedatabase.app/leaderboard"

    def sync_score(self, name, score, time, on_success):
        """Pure logic: Sends score to Firebase and runs a function on success."""
        safe_name = quote(str(name))
        target_url = f"{self.url}/{safe_name}.json"
        
        data = json.dumps({
            "name": name,
            "score": int(score),
            "time": time
        })

        # PUT overwrites or creates the entry for that specific name
        UrlRequest(
            target_url, 
            req_body=data, 
            method='PUT', 
            on_success=lambda req, res: on_success(name)
        )

    def fetch_scores(self, on_data_received):
        """Pure logic: Downloads scores and passes the raw dictionary to a handler."""
        UrlRequest(
            f"{self.url}.json", 
            on_success=lambda req, res: on_data_received(res)
        )