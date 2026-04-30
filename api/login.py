import os
import json
from http.server import BaseHTTPRequestHandler
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ixfcgvcigwqsafsllbvj.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZmNndmNpZ3dxc2Fmc2xsYnZqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzUzNTcyNSwiZXhwIjoyMDkzMTExNzI1fQ.XpP4z010txpKYnfC0LZFvSPDFxEbRVnsdg09dziIAb0")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            username = body.get("username", "").strip()
            password = body.get("password", "").strip()

            if not username or not password:
                raise ValueError("Missing credentials")

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            result = supabase.table("admin_users").select("*").eq("username", username).eq("password_hash", password).execute()

            if len(result.data) == 1:
                token = os.environ.get("ADMIN_SECRET")
                self._respond(200, {"success": True, "token": token, "username": username})
            else:
                self._respond(401, {"success": False, "message": "Mali ang username o password"})

        except Exception as e:
            self._respond(400, {"success": False, "message": str(e)})

    def do_OPTIONS(self):
        self._respond(200, {})

    def _respond(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
