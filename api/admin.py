import os
import json
import csv
import io
from http.server import BaseHTTPRequestHandler
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ixfcgvcigwqsafsllbvj.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZmNndmNpZ3dxc2Fmc2xsYnZqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzUzNTcyNSwiZXhwIjoyMDkzMTExNzI1fQ.XpP4z010txpKYnfC0LZFvSPDFxEbRVnsdg09dziIAb0")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            token = self.headers.get("Authorization", "")
            if token != f"Bearer {os.environ.get('ADMIN_SECRET')}":
                self._respond(401, {"success": False, "message": "Unauthorized"})
                return

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

            # CSV export
            if "export" in self.path:
                responses = supabase.table("responses").select("*, survey_responses(*)").execute()
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["ID","Name","Age","Sex","Civil Status","Duration","Ward","Submitted","Category","Question","Rating"])
                for r in responses.data:
                    for sr in r.get("survey_responses", []):
                        writer.writerow([
                            r["id"], r["name"], r["age"], r["sex"],
                            r["civil_status"], r["duration_of_hospitalization"],
                            r["ward"], r["created_at"],
                            sr["category"], sr["question"], sr["rating"]
                        ])
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition", "attachment; filename=survey_responses.csv")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(output.getvalue().encode("utf-8-sig"))
                return

            # Stats
            all_responses = supabase.table("responses").select("id, created_at").execute()
            all_answers   = supabase.table("survey_responses").select("rating, category").execute()

            total_responses = len(all_responses.data)
            ratings = [r["rating"] for r in all_answers.data]
            avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0
            latest = max((r["created_at"] for r in all_responses.data), default=None)

            # Category averages
            cat_map = {}
            for r in all_answers.data:
                c = r["category"]
                cat_map.setdefault(c, []).append(r["rating"])
            categories = [
                {"category": c, "average_rating": round(sum(v)/len(v), 2), "count": len(v)}
                for c, v in cat_map.items()
            ]
            categories.sort(key=lambda x: x["average_rating"], reverse=True)

            # Ward category performance
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

            # Recent responses - fetch all, no limit issues
            recent = supabase.table("responses").select("*").order("created_at", desc=True).execute()

            self._respond(200, {
                "success": True,
                "stats": {
                    "total_responses": total_responses,
                    "total_answers": len(ratings),
                    "average_rating": avg_rating,
                    "latest_response": latest
                },
                "categories": categories,
                "ward_performance": ward_performance,
                "responses": recent.data
            })

        except Exception as e:
            self._respond(400, {"success": False, "message": str(e)})

    def do_DELETE(self):
        try:
            token = self.headers.get("Authorization", "")
            if token != f"Bearer {os.environ.get('ADMIN_SECRET')}":
                self._respond(401, {"success": False, "message": "Unauthorized"})
                return

            from urllib.parse import urlparse, parse_qs
            params = parse_qs(urlparse(self.path).query)
            response_id = int(params.get("delete", [0])[0])
            if not response_id:
                raise ValueError("Missing response id")

            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            supabase.table("responses").delete().eq("id", response_id).execute()
            self._respond(200, {"success": True})

        except Exception as e:
            self._respond(400, {"success": False, "message": str(e)})

    def do_OPTIONS(self):
        self._respond(200, {})

    def _respond(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
