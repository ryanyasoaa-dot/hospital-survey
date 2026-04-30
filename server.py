import os
import sys
import json
import csv
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

os.environ.setdefault("SUPABASE_URL", "https://ixfcgvcigwqsafsllbvj.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZmNndmNpZ3dxc2Fmc2xsYnZqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzUzNTcyNSwiZXhwIjoyMDkzMTExNzI1fQ.XpP4z010txpKYnfC0LZFvSPDFxEbRVnsdg09dziIAb0")
os.environ.setdefault("ADMIN_SECRET", "hospital2026")

from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
ADMIN_SECRET = os.environ["ADMIN_SECRET"]

CATEGORIES = {
    "II. Pagtrato at Pangangalaga ng mga Nars": [
        "Maayos at may paggalang ang pakikitungo sa akin ng mga nars.",
        "Ipinakita ng mga nars ang malasakit sa aking kalagayan.",
        "Agad na tinugunan ng mga nars ang aking pangangailangan.",
        "Pinadama sa akin ng mga nars ang pagiging komportable habang ako ay ginagamot at inaalagaan."
    ],
    "III. Pagbibigay ng Impormasyon": [
        "Ipinaliwanag ng mga nars ang mga gagawing pamamaraan bago ito isagawa.",
        "Maliwanag nilang ipinaalam ang tungkol sa aking gamot.",
        "Nasagot nang maayos ng mga nars ang aking mga tanong.",
        "Naipaliwanag nila ang mahahalagang impormasyon tungkol sa aking kalagayan."
    ],
    "IV. Kakayahan ng mga Nars": [
        "Maayos at maingat gumawa ng tungkulin ang mga nars.",
        "Nagpakita sila ng kaalaman sa kanilang trabaho.",
        "Naging maingat sila sa pagbibigay ng pangangalaga sa akin.",
        "Naging handa at mabilis sila sa oras ng pangangailangan."
    ],
    "V. Pangkalahatang Kasiyahan": [
        "Ako ay nasiyahan sa serbisyong ibinigay ng mga nars.",
        "Nakatulong ang mga nars sa aking paggaling.",
        "Maganda ang naging karanasan ko sa pangangalaga ng mga nars.",
        "Irerekomenda ko ang ospital na ito dahil sa mahusay na serbisyo ng mga nars."
    ]
}

class LocalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), 'public'), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == '/api/admin':
            self._handle_admin(params)
        elif path in ('/', ''):
            self.path = '/index.html'
            super().do_GET()
        else:
            super().do_GET()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        token = self.headers.get("Authorization", "")
        if token != f"Bearer {ADMIN_SECRET}":
            self._json(401, {"success": False, "message": "Unauthorized"})
            return
        try:
            response_id = int(params.get("delete", [0])[0])
            if not response_id:
                raise ValueError("Missing response id")
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            supabase.table("responses").delete().eq("id", response_id).execute()
            self._json(200, {"success": True})
        except Exception as e:
            print(f"  [delete error] {e}")
            self._json(400, {"success": False, "message": str(e)})

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if path == '/api/submit':
            self._handle_submit(body)
        elif path == '/api/login':
            self._handle_login(body)
        else:
            self.send_error(404)

    # --- Submit ---
    def _handle_submit(self, body):
        try:
            name     = body.get("name", "").strip()
            age      = int(body.get("age", 0))
            sex      = body.get("sex", "").strip()
            civil    = body.get("civil_status", "").strip()
            duration = body.get("duration_of_hospitalization", "").strip()
            ward     = body.get("ward", "").strip()
            answers  = body.get("answers", {})

            if not all([name, sex, civil, duration, ward]):
                raise ValueError("Missing required fields")
            if len(name) < 2 or age < 1 or age > 120:
                raise ValueError("Invalid name or age")

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            res = supabase.table("responses").insert({
                "name": name, "age": age, "sex": sex,
                "civil_status": civil,
                "duration_of_hospitalization": duration,
                "ward": ward
            }).execute()

            response_id = res.data[0]["id"]

            rows = []
            q_index = 0
            for category, questions in CATEGORIES.items():
                for question in questions:
                    key = f"q_{q_index}"
                    rating = int(answers.get(key, 0))
                    if rating < 1 or rating > 5:
                        raise ValueError(f"Invalid rating for {key}")
                    rows.append({
                        "response_id": response_id,
                        "category": category,
                        "question": question,
                        "rating": rating
                    })
                    q_index += 1

            supabase.table("survey_responses").insert(rows).execute()
            self._json(200, {"success": True, "response_id": response_id})

        except Exception as e:
            print(f"  [submit error] {e}")
            self._json(400, {"success": False, "message": str(e)})

    # --- Login ---
    def _handle_login(self, body):
        try:
            username = body.get("username", "").strip()
            password = body.get("password", "").strip()

            if not username or not password:
                raise ValueError("Missing credentials")

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            result = supabase.table("admin_users").select("*").eq("username", username).eq("password_hash", password).execute()

            if len(result.data) == 1:
                self._json(200, {"success": True, "token": ADMIN_SECRET, "username": username})
            else:
                self._json(401, {"success": False, "message": "Mali ang username o password"})

        except Exception as e:
            print(f"  [login error] {e}")
            self._json(400, {"success": False, "message": str(e)})

    # --- Admin ---
    def _handle_admin(self, params):
        try:
            token = self.headers.get("Authorization", "")
            if token != f"Bearer {ADMIN_SECRET}":
                self._json(401, {"success": False, "message": "Unauthorized"})
                return

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

            if "export" in params:
                responses = supabase.table("responses").select("*, survey_responses(*)").execute()
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["ID","Name","Age","Sex","Civil Status","Duration","Ward","Submitted","Category","Question","Rating"])
                for r in responses.data:
                    for sr in r.get("survey_responses", []):
                        writer.writerow([r["id"], r["name"], r["age"], r["sex"],
                            r["civil_status"], r["duration_of_hospitalization"],
                            r["ward"], r["created_at"], sr["category"], sr["question"], sr["rating"]])
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition", "attachment; filename=survey_responses.csv")
                self._cors()
                self.end_headers()
                self.wfile.write(output.getvalue().encode("utf-8-sig"))
                return

            all_responses = supabase.table("responses").select("id, created_at").execute()
            all_answers   = supabase.table("survey_responses").select("rating, category").execute()

            ratings = [r["rating"] for r in all_answers.data]
            avg = round(sum(ratings) / len(ratings), 2) if ratings else 0
            latest = max((r["created_at"] for r in all_responses.data), default=None)

            cat_map = {}
            for r in all_answers.data:
                cat_map.setdefault(r["category"], []).append(r["rating"])
            categories = sorted([
                {"category": c, "average_rating": round(sum(v)/len(v), 2), "count": len(v)}
                for c, v in cat_map.items()
            ], key=lambda x: x["average_rating"], reverse=True)

            WARDS = [
                "Emergency Room", "Pedia Ward", "OB Ward", "Male Ward",
                "Female Ward", "Isolation Ward (ISO)", "Private",
                "Medicine Ward", "Outpatient Department (OPD)"
            ]
            ward_data = supabase.table("responses").select("id, ward, survey_responses(category, rating)").execute()
            ward_map = {w: {"total": [], "categories": {}, "count": 0} for w in WARDS}
            for r in ward_data.data:
                ward = r["ward"]
                if ward not in ward_map:
                    ward_map[ward] = {"total": [], "categories": {}, "count": 0}
                ward_map[ward]["count"] += 1
                for sr in r.get("survey_responses", []):
                    ward_map[ward]["total"].append(sr["rating"])
                    ward_map[ward]["categories"].setdefault(sr["category"], []).append(sr["rating"])

            ward_performance = []
            for ward in WARDS:
                wdata = ward_map[ward]
                cat_avgs = [
                    {"category": c, "average_rating": round(sum(v)/len(v), 2)}
                    for c, v in wdata["categories"].items()
                ]
                ward_performance.append({
                    "ward": ward,
                    "response_count": wdata["count"],
                    "overall_average": round(sum(wdata["total"])/len(wdata["total"]), 2) if wdata["total"] else 0,
                    "categories": sorted(cat_avgs, key=lambda x: x["category"])
                })

            recent = supabase.table("responses").select("*").order("created_at", desc=True).execute()

            self._json(200, {
                "success": True,
                "stats": {
                    "total_responses": len(all_responses.data),
                    "total_answers": len(ratings),
                    "average_rating": avg,
                    "latest_response": latest
                },
                "categories": categories,
                "ward_performance": ward_performance,
                "responses": recent.data
            })

        except Exception as e:
            print(f"  [admin error] {e}")
            self._json(400, {"success": False, "message": str(e)})

    def _json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def log_message(self, format, *args):
        print(f"  {self.address_string()} - {format % args}")

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('localhost', port), LocalHandler)
    print(f"\n  Server running at http://localhost:{port}")
    print(f"  Survey  → http://localhost:{port}/index.html")
    print(f"  Login   → http://localhost:{port}/login.html")
    print(f"  Admin   → http://localhost:{port}/admin.html")
    print(f"\n  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
