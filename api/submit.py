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
        "The questions in the Digital Nursing Care Satisfaction Survey Form that I answered are clear and easy to understand.",
        "The statements used in the survey form are not confusing.",
        "The instructions are clear and easy to follow while answering the form.",
        "Each question is well-constructed for accurate responses.",
        "I easily understand the purpose of each question in the survey form."
    ],
    "VII. Ease of Use": [
        "The Digital Nursing Care Satisfaction Survey Form is easy to use.",
        "I was able to easily navigate from one question to the next.",
        "The process of answering the digital survey form is convenient."
    ],
    "VIII. Completeness of Responses": [
        "I was able to provide complete answers to each question.",
        "The choices provided are sufficient for me to express my responses properly.",
        "The survey form helped me express my overall experience."
    ],
    "IX. Efficiency": [
        "I was able to save time in answering the digital survey form.",
        "It is faster to answer compared to traditional paper-based surveys.",
        "The process of answering the form is smooth and continuous.",
        "The digital survey form helped me provide feedback quickly.",
        "The digital survey form is effective in collecting my responses."
    ],
    "X. User Satisfaction": [
        "I am satisfied with my experience using the Digital Nursing Care Satisfaction Survey Form.",
        "I feel comfortable using the digital survey form.",
        "I would use this type of survey form again if given the chance.",
        "I would recommend the use of digital survey forms to other patients or respondents."
    ],
    "XI. Accuracy": [
        "I did not notice any incorrect recording of my responses.",
        "My answers were saved accurately and consistently."
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
