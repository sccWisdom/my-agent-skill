import json
import subprocess
import tempfile
import unittest
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "query_and_chart.py"


class QueryAndChartOutputTests(unittest.TestCase):
    def fetch_url_text(self, url: str) -> str:
        with urllib.request.urlopen(url, timeout=2) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    def run_script(self, question: str, sql: str, rows: list[list], columns: list[str] | None = None):
        columns = columns or ["day", "value"]
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            mock_file = td_path / "mock.json"
            output_dir = td_path / "outputs"
            mock_payload = {
                "cases": [
                    {
                        "id": "case1",
                        "columns": columns,
                        "rows": rows,
                    }
                ]
            }
            mock_file.write_text(json.dumps(mock_payload, ensure_ascii=False), encoding="utf-8")

            cmd = [
                "python",
                str(SCRIPT),
                "--question",
                question,
                "--sql",
                sql,
                "--mock-file",
                str(mock_file),
                "--mock-case",
                "case1",
                "--output-dir",
                str(output_dir),
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(proc.stdout.strip(), "", msg=proc.stderr)

            result_path = Path(proc.stdout.strip().splitlines()[-1])
            result = json.loads(result_path.read_text(encoding="utf-8-sig"))
            chart_html = ""
            chart_url_html = ""
            if result.get("chart_url"):
                chart_html = result_path.parent.joinpath("chart.html").read_text(encoding="utf-8-sig")
                chart_url_html = self.fetch_url_text(result["chart_url"])

            return proc.returncode, result, chart_html, chart_url_html

    def test_success_result_keeps_full_sql_and_uses_only_chart_url(self):
        sql = "SELECT DATE(created_at) AS day, COUNT(*) AS new_users FROM users GROUP BY DATE(created_at) ORDER BY day"
        rows = [["2026-03-01", 10], ["2026-03-02", 20], ["2026-03-03", 15]]

        code, result, _, url_html = self.run_script("new user trend", sql, rows)

        self.assertEqual(code, 0)
        self.assertEqual(result["sql_executed"], f"{sql} LIMIT 500")
        self.assertIn("chart_url", result)
        self.assertNotIn("chart_html_path", result)
        self.assertTrue(str(result["chart_url"]).startswith("http://127.0.0.1:"))
        self.assertTrue(str(result["chart_url"]).endswith("/chart.html"))
        self.assertIn("<canvas id=\"chart\"></canvas>", url_html)

    def test_html_page_is_chart_only(self):
        sql = "SELECT category, amount FROM sales ORDER BY amount DESC"
        rows = [["A", 100], ["B", 80], ["C", 60]]

        code, result, chart_html, _ = self.run_script("channel compare", sql, rows, columns=["channel", "gmv"])

        self.assertEqual(code, 0)
        self.assertTrue(result.get("chart_url"))
        self.assertIn("<canvas id=\"chart\"></canvas>", chart_html)
        self.assertNotIn("query_summary", chart_html)
        self.assertNotIn("key_findings", chart_html)
        self.assertNotIn("<table", chart_html)

    def test_blocked_shape_uses_chart_url_and_sql_executed(self):
        blocked_code, blocked_result, _, _ = self.run_script(
            "delete records",
            "DELETE FROM users",
            rows=[["x", 1]],
            columns=["k", "v"],
        )
        self.assertNotEqual(blocked_code, 0)
        self.assertEqual(blocked_result["query_status"], "blocked")
        self.assertIn("chart_url", blocked_result)
        self.assertNotIn("chart_html_path", blocked_result)
        self.assertIn("sql_executed", blocked_result)

    def test_four_chart_scenarios_generate_direct_urls(self):
        cases = [
            (
                "new user trend",
                "SELECT day, new_users FROM t ORDER BY day",
                ["day", "new_users"],
                [["2026-03-01", 10], ["2026-03-02", 15]],
                'const chartType = "line";',
                "indexAxis: 'x'",
            ),
            (
                "channel compare",
                "SELECT channel, gmv FROM t",
                ["channel", "gmv"],
                [["A", 100], ["B", 80]],
                'const chartType = "bar";',
                "indexAxis: 'x'",
            ),
            (
                "sales share",
                "SELECT product, sales FROM t",
                ["product", "sales"],
                [["P1", 60], ["P2", 40]],
                'const chartType = "pie";',
                "indexAxis: 'x'",
            ),
            (
                "top rank channels",
                "SELECT channel, amount FROM t",
                ["channel", "amount"],
                [["A", 120], ["B", 90]],
                'const chartType = "bar";',
                "indexAxis: 'y'",
            ),
        ]

        for question, sql, columns, rows, chart_type_marker, axis_marker in cases:
            code, result, _, url_html = self.run_script(question, sql, rows, columns=columns)
            self.assertEqual(code, 0)
            self.assertTrue(result.get("chart_url"))
            self.assertIn(chart_type_marker, url_html)
            self.assertIn(axis_marker, url_html)

    def test_empty_result_keeps_shape_without_chart(self):
        sql = "SELECT day, value FROM t ORDER BY day"
        code, result, chart_html, url_html = self.run_script(
            "last 7 day trend",
            sql,
            rows=[],
            columns=["day", "value"],
        )

        self.assertEqual(code, 0)
        self.assertEqual(result.get("query_status"), "success")
        self.assertEqual(result.get("chart_url"), "")
        self.assertEqual(result.get("sql_executed"), f"{sql} LIMIT 500")
        self.assertEqual(chart_html, "")
        self.assertEqual(url_html, "")


if __name__ == "__main__":
    unittest.main()
