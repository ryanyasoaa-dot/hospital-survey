import os
import json
from http.server import BaseHTTPRequestHandler
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ixfcgvcigwqsafsllbvj.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZmNndmNpZ3dxc2Fmc2xsYnZqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzUzNTcyNSwiZXhwIjoyMDkzMTExNzI1fQ.XpP4z010txpKYnfC0LZFvSPDFxEbRVnsdg09dziIAb0")

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
    ],
    "VI. Clarity of Statements": [
        "Malinaw at madaling maunawaan ang mga tanong sa Digital Nursing Care Satisfaction Survey Form na aking sinagutan.",
        "Hindi nakakalito ang mga pahayag na ginamit sa survey form.",
        "Ang mga instruksyon ay malinaw at madaling sundin habang sinasagutan ang form.",
        "Ang bawat tanong ay maayos ang pagkakabuo para sa tamang pagsagot.",
        "Natintindihan ko agad ang layunin ng bawat tanong sa survey form."
    ],
    "VII. Ease of Use": [
        "Madaling gamitin ang Digital Nursing Care Satisfaction Survey Form.",
        "Madali akong nakapag-navigate mula sa isang tanong patungo sa susunod.",
        "Maginhawa ang proseso ng pagsagot sa digital survey form."
    ],
    "VIII. Completeness of Responses": [
        "Nagawa kong makapagbigay ng kumpletong sagot sa bawat tanong.",
        "Sapat ang mga pagpipilian upang maipahayag ko nang maayos ang aking sagot.",
        "Ang survey form ay nakatulong upang maipahayag ko ang aking kabuuang karanasan."
    ],
    "IX. Efficiency": [
        "Nakapagtipid ako ng oras sa pagsagot sa digital survey form.",
        "Mas mabilis itong sagutan kumpara sa tradisyunal na papel na survey.",
        "Maayos at tuloy-tuloy ang proseso ng pagsagot sa form.",
        "Nakatulong ang digital survey form sa mabilis na pagbibigay ko ng feedback.",
        "Epektibo ang digital survey form sa pangangalap ng aking mga sagot."
    ],
    "X. User Satisfaction": [
        "Nasiyahan ako sa aking karanasan sa paggamit ng Digital Nursing Care Satisfaction Survey Form.",
        "Komportable akong gumamit ng digital survey form.",
        "Gagamitin ko muli ang ganitong uri ng survey form kung muling ipagagamit.",
        "Irerekomenda ko ang paggamit ng digital survey forms sa ibang pasyente o respondents."
    ],
    "XI. Accuracy": [
        "Wala akong napansing maling pag-record ng aking responses.",
        "Tama at consistent ang pag-save ng aking mga sagot."
    ]
}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            name     = body.get("name", "").strip()
            age      = int(body.get("age", 0))
            sex      = body.get("sex", "").strip()
            civil    = body.get("civil_status", "").strip()
            duration = body.get("duration_of_hospitalization", "").strip()
            ward     = body.get("ward", "").strip()
            answers  = body.get("answers", {})

            if not all([name, age, sex, civil, duration, ward]):
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

            self._respond(200, {"success": True, "response_id": response_id})

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
