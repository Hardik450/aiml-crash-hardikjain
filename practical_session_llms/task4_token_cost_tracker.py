import csv
import os
from datetime import datetime
import pandas as pd
import json
from llm_clients import call_groq, call_gemini, estimate_cost

LOG_PATH = "logs/usage_log.csv"
LOG_FIELDS = [
    "timestamp", "provider", "model", "prompt_text", "response_text",
    "prompt_tokens", "completion_tokens", "total_tokens", "estimated_cost_usd",
]


class TokenCostTracker:
    """Logs every LLM call to a CSV file and can generate a usage report."""

    def __init__(self, log_path: str = LOG_PATH):
        self.log_path = log_path
        self._ensure_log_file()

    def _ensure_log_file(self) -> None:
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
                writer.writeheader()
            return

        # Repair a log file created without headers.
        with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
            first_line = f.readline().strip()
        if first_line != ",".join(LOG_FIELDS):
            with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
                rows = f.read().splitlines()
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
                writer.writeheader()
                for row in rows:
                    if not row.strip():
                        continue
                    f.write(row + "\n")

    def _log_call(self, result: dict, prompt: str) -> dict:
        cost = estimate_cost(result["provider"], result["prompt_tokens"],
                              result["completion_tokens"])
        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "provider": result["provider"],
            "model": result["model"],
            "prompt_text": prompt,
            "response_text": result["text"],
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "total_tokens": result["total_tokens"],
            "estimated_cost_usd": cost,
        }
        with open(self.log_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
            writer.writerow(record)
        return record

    def track_groq_call(self, prompt: str, **kwargs) -> dict:
        """Call Groq, log the result, and return the log record."""
        result = call_groq(prompt, **kwargs)
        return self._log_call(result, prompt)

    def track_gemini_call(self, prompt: str, **kwargs) -> dict:
        """Call Gemini, log the result, and return the log record."""
        result = call_gemini(prompt, **kwargs)
        return self._log_call(result, prompt)

    def generate_report(self) -> dict:
        """Read the full log and compute summary statistics."""
        df = pd.read_csv(self.log_path, encoding="utf-8", encoding_errors = "replace")
        if df.empty:
            return {"total_requests": 0, "total_tokens": 0, "total_cost_usd": 0.0}

        report = {
            "total_requests": len(df),
            "total_prompt_tokens": int(df["prompt_tokens"].sum()),
            "total_completion_tokens": int(df["completion_tokens"].sum()),
            "total_tokens": int(df["total_tokens"].sum()),
            "total_cost_usd": round(df["estimated_cost_usd"].sum(), 6),
            "by_provider": df.groupby("provider").agg(
                requests=("provider", "count"),
                tokens=("total_tokens", "sum"),
                cost_usd=("estimated_cost_usd", "sum"),
            ).round(6).to_dict(orient="index"),
        }
        return report

    def print_report(self) -> None:
        report = self.generate_report()
        print("\n" + "=" * 60)
        print("TOKEN USAGE & COST REPORT")
        print("=" * 60)
        print(f"Total requests          : {report['total_requests']}")
        print(f"Total prompt tokens     : {report.get('total_prompt_tokens', 0):,}")
        print(f"Total completion tokens : {report.get('total_completion_tokens', 0):,}")
        print(f"Total tokens            : {report.get('total_tokens', 0):,}")
        print(f"Estimated total cost    : ${report.get('total_cost_usd', 0):.6f}")
        print("\nBreakdown by provider:")
        for provider, stats in report.get("by_provider", {}).items():
            print(f"  {provider}: {stats['requests']} requests, "
                  f"{stats['tokens']:,} tokens, ${stats['cost_usd']:.6f}")
        print("=" * 60)


if __name__ == "__main__":
    tracker = TokenCostTracker()

    sample_prompts = [
        ("groq", "Summarize the benefits of regular exercise in 2 sentences."),
        ("gemini", "List 3 tips for writing clean Python code."),
        ("groq", "What is the difference between a list and a tuple in Python?"),
        ("gemini", "Explain what an API is to a complete beginner."),
    ]

    print(f"Making real API calls and logging usage...\n")

    for provider, prompt in sample_prompts:
        if provider == "groq":
            record = tracker.track_groq_call(prompt)
        else:
            record = tracker.track_gemini_call(prompt)
        print(f"[{record['provider']}] {record['total_tokens']} tokens, "
              f"${record['estimated_cost_usd']:.6f} -> logged to {LOG_PATH}")

    tracker.print_report()
    with open("outputs/task4_usage_report.json", "w") as f:
        json.dump(tracker.generate_report(), f, indent=2, default=str)
    print(f"\nFull report saved to outputs/task4_usage_report.json")
