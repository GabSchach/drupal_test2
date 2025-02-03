import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DrupalJSONAPIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False
        self.csrf_token = None
        self.login()
        self.get_csrf_token()

    def login(self):
        """Login to Drupal and get session cookie"""
        login_url = f"{self.base_url}/user/login"
        
        # First get the form build ID and token
        response = self.session.get(login_url)
        
        # Now post the login form
        login_data = {
            'name': self.username,
            'pass': self.password,
            'form_id': 'user_login_form',
            'op': 'Log in'
        }
        
        response = self.session.post(login_url, data=login_data)
        print(f"Login response status: {response.status_code}")
        if response.status_code == 200:
            print("Login successful")
        else:
            print("Login failed")

    def get_csrf_token(self):
        """Get CSRF token from Drupal"""
        token_url = f"{self.base_url}/session/token"
        response = self.session.get(token_url)
        if response.status_code == 200:
            self.csrf_token = response.text
            print(f"Got CSRF token: {self.csrf_token}")
        else:
            print(f"Failed to get CSRF token. Status: {response.status_code}")
        return self.csrf_token

    def create_project(self, project_data):
        url = f"{self.base_url}/jsonapi/node/projects"
        
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'X-CSRF-Token': self.csrf_token
        }

        # Format the data according to JSON:API specification
        payload = {
            "data": {
                "type": "node--projects",
                "attributes": {
                    "title": project_data.get("project_name", ""),
                    "field_adresse": project_data.get("adresse", ""),
                    "field_description": project_data.get("description", ""),
                    "field_federal_state": project_data.get("federal_state", ""),
                    "field_geo_data": project_data.get("geo_data", ""),
                    "field_hospital": project_data.get("hospital", ""),
                    "field_latitude": project_data.get("latitude", 0),
                    "field_longitude": project_data.get("longitude", 0),
                    "field_project_name": project_data.get("project_name", ""),
                    "field_status": project_data.get("status", "")
                }
            }
        }

        print(f"Making request to: {url}")
        print(f"With headers: {headers}")
        print(f"With payload: {json.dumps(payload, indent=2)}")
        print(f"Session cookies: {self.session.cookies.get_dict()}")
        
        response = self.session.post(url, headers=headers, json=payload)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        try:
            print(f"Response body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Raw response text: {response.text}")
                
        return response

# Example usage
if __name__ == "__main__":
    # Configuration
    DRUPAL_URL = "https://crispy-enigma-jj77r9v6xp453qjx4-80.app.github.dev"
    USERNAME = "admin"
    PASSWORD = "admin"

    # Create client instance
    client = DrupalJSONAPIClient(DRUPAL_URL, USERNAME, PASSWORD)
    
    # Example project data
    project_data = {
        "project_name": "Test Hospital Project",
        "adresse": "123 Medical Street",
        "description": "New hospital wing construction",
        "federal_state": "Bavaria",
        "geo_data": "POINT(13.404954 52.520008)",
        "hospital": "Central Hospital",
        "latitude": 52.520008,
        "longitude": 13.404954,
        "status": "In Progress"
    }

    # Create the project
    response = client.create_project(project_data)
    
    if response.status_code == 201:
        print("Project created successfully!")
    else:
        print(f"Error creating project: {response.status_code}")