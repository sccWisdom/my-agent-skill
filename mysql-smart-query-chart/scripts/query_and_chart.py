#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple

READ_PREFIX = ("select", "with", "show", "describe", "desc", "explain")
BLOCKED_KEYWORDS = (
    "insert", "update", "delete", "drop", "alter", "create", "truncate",
    "replace", "grant", "revoke", "rename", "call", "handler", "load data",
)


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def clean_sql(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"--.*?$", " ", sql, flags=re.M)
    return " ".join(sql.strip().split())


def is_read_only(sql: str) -> Tuple[bool, str]:
    text = clean_sql(sql).lower()
    if not text:
        return False, "SQL 为空"

    statements = [s.strip() for s in text.split(";") if s.strip()]
    if len(statements) > 1:
        return False, "只允许单条查询语句"

    if not text.startswith(READ_PREFIX):
        return False, "只允许读查询（SELECT/WITH/SHOW/DESCRIBE/EXPLAIN）"

    for kw in BLOCKED_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", text):
            return False, f"命中禁用关键词: {kw}"

    return True, "ok"


def ensure_limit(sql: str, limit: int) -> Tuple[str, bool]:
    text = clean_sql(sql).rstrip(";").strip()
    if re.search(r"\blimit\b", text, flags=re.I):
        return text, False
    return f"{text} LIMIT {limit}", True


def sql_for_display(sql: str) -> str:
    s = (sql or "").strip()
    if not s:
        return ""
    return s


def parse_mysql_tsv(stdout: str) -> Tuple[List[str], List[List[Any]]]:
    lines = [line for line in stdout.splitlines() if line.strip() != ""]
    if not lines:
        return [], []
    reader = csv.reader(lines, delimiter="\t")
    rows = list(reader)
    headers = rows[0]
    data_rows = rows[1:]
    return headers, [coerce_row(r) for r in data_rows]


def coerce_value(v: str) -> Any:
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return ""
    if re.fullmatch(r"-?\d+", s):
        try:
            return int(s)
        except Exception:
            return s
    if re.fullmatch(r"-?\d+\.\d+", s):
        try:
            return float(s)
        except Exception:
            return s
    return s


def coerce_row(row: List[str]) -> List[Any]:
    return [coerce_value(v) for v in row]


def run_mysql_cli(sql: str, args: argparse.Namespace) -> Tuple[List[str], List[List[Any]]]:
    mysql_bin = args.mysql_bin
    cmd = [
        mysql_bin,
        "-h", args.host,
        "-P", str(args.port),
        "-u", args.user,
        "--default-character-set=utf8mb4",
        "--batch",
        "--raw",
        "--skip-column-names=false",
    ]
    if args.database:
        cmd.extend(["-D", args.database])
    cmd.extend(["-e", sql])

    env = os.environ.copy()
    if args.password:
        env["MYSQL_PWD"] = args.password

    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "mysql 执行失败")

    return parse_mysql_tsv(proc.stdout)


def load_mock(mock_file: str, case_id: str) -> Tuple[List[str], List[List[Any]]]:
    data = json.loads(Path(mock_file).read_text(encoding="utf-8-sig"))
    for item in data.get("cases", []):
        if item.get("id") == case_id:
            return item.get("columns", []), item.get("rows", [])
    raise ValueError(f"mock case 不存在: {case_id}")


def detect_datetime_col(headers: List[str], rows: List[List[Any]]) -> int:
    if not headers or not rows:
        return -1
    score = []
    for i, h in enumerate(headers):
        name = h.lower()
        s = 0
        if any(k in name for k in ["date", "time", "day", "month", "week", "year", "日期", "时间"]):
            s += 2
        parsed = 0
        for r in rows[:20]:
            try:
                dt.datetime.fromisoformat(str(r[i]).replace("Z", ""))
                parsed += 1
            except Exception:
                pass
        if parsed >= max(1, min(20, len(rows)) // 2):
            s += 2
        score.append((s, i))
    score.sort(reverse=True)
    return score[0][1] if score and score[0][0] > 0 else -1


def numeric_cols(headers: List[str], rows: List[List[Any]]) -> List[int]:
    idxs = []
    for i, _ in enumerate(headers):
        values = [r[i] for r in rows[:50] if i < len(r)]
        if not values:
            continue
        ok = sum(1 for v in values if isinstance(v, (int, float)))
        if ok >= max(1, int(len(values) * 0.7)):
            idxs.append(i)
    return idxs


def decide_chart(question: str, headers: List[str], rows: List[List[Any]]) -> Dict[str, Any]:
    if not rows or not headers:
        return {"type": "none", "reason": "无数据，跳过图表"}

    q = (question or "").lower()
    dt_col = detect_datetime_col(headers, rows)
    nums = numeric_cols(headers, rows)
    cats = [i for i in range(len(headers)) if i not in nums]

    if dt_col >= 0 and nums:
        y = nums[0] if nums[0] != dt_col else (nums[1] if len(nums) > 1 else -1)
        if y >= 0:
            return {
                "type": "line",
                "x": dt_col,
                "y": y,
                "reason": "按时间变化的数据更适合看趋势，使用折线图。",
            }

    if any(k in q for k in ["占比", "比例", "构成", "percentage", "share"]) and cats and nums:
        return {
            "type": "pie",
            "x": cats[0],
            "y": nums[0],
            "reason": "问题关注结构占比，使用饼图更直观。",
        }

    if any(k in q for k in ["排行", "排名", "top", "rank"]) and cats and nums:
        return {
            "type": "barh",
            "x": cats[0],
            "y": nums[0],
            "reason": "问题关注排名，使用横向条形图便于比较名次。",
        }

    if cats and nums:
        return {
            "type": "bar",
            "x": cats[0],
            "y": nums[0],
            "reason": "类别之间做数值对比，使用柱状图。",
        }

    if nums:
        return {
            "type": "line",
            "x": 0,
            "y": nums[0],
            "reason": "数据以数值序列为主，使用折线图展示变化。",
        }

    return {"type": "none", "reason": "当前结果不适合自动成图"}


def to_float(v: Any) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", ""))
    except Exception:
        return 0.0


def is_port_listening(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def start_static_server(root_dir: Path, host: str, port: int) -> bool:
    cmd = [
        sys.executable,
        "-m",
        "http.server",
        str(port),
        "--bind",
        host,
        "--directory",
        str(root_dir),
    ]

    kwargs: Dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }

    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    subprocess.Popen(cmd, **kwargs)
    for _ in range(8):
        if is_port_listening(host, port):
            return True
        time.sleep(0.15)
    return False


def url_reachable(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=0.6) as resp:
            return 200 <= int(getattr(resp, "status", 200)) < 400
    except Exception:
        return False


def ensure_static_server(root_dir: Path, host: str, preferred_port: int, probe_path: str = "") -> int:
    probe_path = probe_path.lstrip("/")

    def can_reuse(port: int) -> bool:
        if not probe_path:
            return True
        return url_reachable(f"http://{host}:{port}/{probe_path}")

    if is_port_listening(host, preferred_port) and can_reuse(preferred_port):
        return preferred_port

    max_scan = 30
    for offset in range(max_scan):
        port = preferred_port + offset
        if is_port_listening(host, port):
            if can_reuse(port):
                return port
            continue

        if start_static_server(root_dir, host, port) and can_reuse(port):
            return port

    raise RuntimeError("failed to start local chart server")


def summarize(question: str, headers: List[str], rows: List[List[Any]], chart: Dict[str, Any]) -> Tuple[str, List[str]]:
    if not rows:
        return (
            "当前筛选条件下没有查到数据。",
            [
                "建议放宽时间范围后再试一次。",
                "建议检查过滤条件是否过严。",
                "若口径不确定，先明确指标定义再查询。",
            ],
        )

    summary = f"已完成查询：{question}，共返回 {len(rows)} 条记录。"
    findings: List[str] = []

    y_idx = chart.get("y", -1)
    x_idx = chart.get("x", -1)
    ctype = chart.get("type")

    if y_idx >= 0 and y_idx < len(headers):
        vals = [to_float(r[y_idx]) for r in rows]
        if vals:
            findings.append(f"{headers[y_idx]} 总量为 {sum(vals):,.2f}。")
            max_i = max(range(len(vals)), key=lambda i: vals[i])
            if x_idx >= 0 and x_idx < len(headers):
                findings.append(f"峰值出现在 {rows[max_i][x_idx]}，数值为 {vals[max_i]:,.2f}。")

            if ctype == "line" and len(vals) >= 2:
                trend = "上升" if vals[-1] > vals[0] else ("下降" if vals[-1] < vals[0] else "基本持平")
                findings.append(f"整体趋势呈{trend}。")

    if not findings:
        findings.append("已返回明细结果，可按维度继续下钻分析。")

    return summary, findings[:3]


def make_chart_html(
    out_file: Path,
    headers: List[str],
    rows: List[List[Any]],
    chart: Dict[str, Any],
) -> None:
    labels = []
    values = []

    ctype = chart.get("type")
    x_idx = chart.get("x", -1)
    y_idx = chart.get("y", -1)

    if ctype != "none" and rows and x_idx >= 0 and y_idx >= 0:
        labels = [str(r[x_idx]) for r in rows]
        values = [to_float(r[y_idx]) for r in rows]

    chart_type_map = {"line": "line", "bar": "bar", "barh": "bar", "pie": "pie"}
    chart_type = chart_type_map.get(ctype, "bar")
    index_axis = "'y'" if ctype == "barh" else "'x'"

    html = f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>chart</title>
  <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
  <style>
    body {{ margin: 0; padding: 16px; background: #ffffff; }}
    .wrap {{ width: min(1200px, 100%); margin: 0 auto; }}
    canvas {{ width: 100%; height: 560px !important; }}
    .empty {{ font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; color: #4b5563; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <canvas id=\"chart\"></canvas>
  </div>
  <script>
    const labels = {json.dumps(labels, ensure_ascii=False)};
    const values = {json.dumps(values, ensure_ascii=False)};
    const chartType = {json.dumps(chart_type)};
    const hasData = labels.length > 0 && values.length > 0;
    if (hasData) {{
      new Chart(document.getElementById('chart'), {{
        type: chartType,
        data: {{
          labels,
          datasets: [{{
            label: 'value',
            data: values,
            backgroundColor: ['#7cb9e8','#88d498','#f4b183','#c3aed6','#f7e28b','#9fd3c7'],
            borderColor: '#3b82f6',
            borderWidth: 2,
            fill: false,
            tension: 0.25
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: {index_axis},
          plugins: {{ legend: {{ display: true }} }},
          scales: chartType === 'pie' ? {{}} : {{ y: {{ beginAtZero: true }} }}
        }}
      }});
    }} else {{
      const msg = document.createElement('p');
      msg.className = 'empty';
      msg.innerText = 'No chart generated for current result.';
      document.getElementById('chart').replaceWith(msg);
    }}
  </script>
</body>
</html>
"""
    out_file.write_text(html, encoding="utf-8-sig")


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="执行 MySQL 查询并输出问数结论与 HTML 图表")
    parser.add_argument("--question", required=True, help="自然语言问题")
    parser.add_argument("--sql", required=True, help="待执行 SQL")
    parser.add_argument("--output-dir", default="outputs", help="输出目录")
    parser.add_argument("--max-limit", type=int, default=500, help="默认最大 LIMIT")

    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    parser.add_argument("--database", default=os.getenv("MYSQL_DATABASE", ""))
    parser.add_argument("--mysql-bin", default="mysql", help="mysql 客户端命令")

    parser.add_argument("--mock-file", default="", help="mock 数据文件")
    parser.add_argument("--mock-case", default="", help="mock case id")
    parser.add_argument("--chart-host", default="127.0.0.1", help="chart host")
    parser.add_argument("--chart-port", type=int, default=8765, help="chart port")

    args = parser.parse_args()

    base_output_dir = Path(args.output_dir).resolve()

    safe, msg = is_read_only(args.sql)
    if not safe:
        result = {
            "query_summary": "查询被拦截：仅支持只读查询。",
            "key_findings": [msg, "请改为 SELECT/WITH/SHOW/DESCRIBE/EXPLAIN 查询。"],
            "table": {"columns": [], "rows": []},
            "chart_url": "",
            "chart_reason": "",
            "query_status": "blocked",
            "sql_query": sql_for_display(args.sql),
            "sql_executed": clean_sql(args.sql),
            "limited": False,
        }
        out_dir = base_output_dir / now_stamp()
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8-sig")
        print(str(out_dir / "result.json"))
        return 2

    sql_exec, limited = ensure_limit(args.sql, args.max_limit)

    out_dir = base_output_dir / now_stamp()
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.mock_file and args.mock_case:
            headers, rows = load_mock(args.mock_file, args.mock_case)
        else:
            headers, rows = run_mysql_cli(sql_exec, args)
    except Exception as e:
        result = {
            "query_summary": "查询执行失败。",
            "key_findings": [str(e), "请检查连接信息、库名或 SQL 字段是否正确。"],
            "table": {"columns": [], "rows": []},
            "chart_url": "",
            "chart_reason": "",
            "query_status": "error",
            "sql_query": sql_for_display(args.sql),
            "sql_executed": sql_exec,
            "limited": limited,
        }
        (out_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8-sig")
        print(str(out_dir / "result.json"))
        return 1

    chart = decide_chart(args.question, headers, rows)
    summary, findings = summarize(args.question, headers, rows, chart)

    chart_url = ""
    if chart.get("type") != "none":
        chart_file = out_dir / "chart.html"
        make_chart_html(chart_file, headers, rows, chart)
        rel_chart_path = chart_file.relative_to(base_output_dir).as_posix()
        port = ensure_static_server(base_output_dir, args.chart_host, args.chart_port, rel_chart_path)
        chart_url = f"http://{args.chart_host}:{port}/{rel_chart_path}"

    result = {
        "query_summary": summary,
        "key_findings": findings,
        "table": {"columns": headers, "rows": rows},
        "chart_url": chart_url,
        "chart_reason": chart.get("reason", ""),
        "query_status": "success",
        "sql_query": sql_for_display(args.sql),
        "sql_executed": sql_exec,
        "limited": limited,
    }

    (out_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8-sig")
    print(str(out_dir / "result.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

