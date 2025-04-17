import urllib.request
import json
import os

class TokenManager:
    def __init__(self, token_file=".github_token"):
        self.token_file = token_file
    
    def save_token(self, token):
        with open(self.token_file, "w") as f:
            f.write(token)
    
    def load_token(self):
        if not os.path.exists(self.token_file):
            return None
        
        try:
            with open(self.token_file, "r") as f:
                return f.read().strip()
        except Exception:
            return None

def main():
    try:
        username = input("Enter a GitHub username: ")
        url = f"https://api.github.com/users/{username}/events"

        token_manager = TokenManager()
        github_token = token_manager.load_token()

        if not github_token:
            github_token = input("Enter your GitHub personal access token: ")
            token_manager.save_token(github_token)

        headers = {
            "Authorization": f"token {github_token}",
            "User-Agent": "github-activity-app"
        }

        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode('utf-8')
        events = json.loads(data)

        print(f"Recent activity for {username}:")
        for event in events:
            event_type = event.get('type', 'Unknown')
            event_type = event_type.replace('Event', '')
            repo_name = event.get('repo', {}).get('name', 'Unknown repository')
            created_at = event.get('created_at', 'Unknown time')
            if event_type == 'Issues':
                event_type = 'Issue'
            print(f"- {event_type} {repo_name} at {created_at}")
    except KeyboardInterrupt:
        exit(0)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User {username} not found")
        else:
            print(f"Error occurred: {e}")
        exit(1)
    except urllib.error.URLError as e:
        print("Please check your internet connection and try again.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()