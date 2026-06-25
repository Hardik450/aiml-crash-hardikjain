
import json
import csv
from datetime import datetime
import pandas as pd

from llm_clients import call_groq, call_gemini


def compare_providers(prompt: str) -> list[dict]:
    """Send the same prompt to both providers and return their results."""
    print(f"\nPrompt: {prompt!r}")
    print("Sending to Groq...")
    groq_result = call_groq(prompt)

    print("Sending to Gemini...")
    gemini_result = call_gemini(prompt)

    results = []
    for r in (groq_result, gemini_result):
        results.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "prompt": prompt,
            "provider": r["provider"],
            "model": r["model"],
            "response_text": r["text"],
            "response_length_chars": len(r["text"]),
            "response_length_words": len(r["text"].split()),
            "response_time_sec": r["response_time_sec"],
            "prompt_tokens": r["prompt_tokens"],
            "completion_tokens": r["completion_tokens"],
            "total_tokens": r["total_tokens"],
            "error": r["error"],
        })
    return results


def print_comparison_table(results: list[dict]) -> None:
    """Pretty-print a side-by-side comparison table."""
    df = pd.DataFrame(results)
    table = df[["provider", "model", "response_time_sec",
                "response_length_words", "total_tokens"]]
    print("\n" + "=" * 70)
    print("COMPARISON TABLE")
    print("=" * 70)
    print(table.to_string(index=False))
    print("=" * 70)


def save_results(all_results: list[dict], csv_path: str, json_path: str) -> None:
    """Save all results to both CSV and JSON formats."""
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2)

    fieldnames = list(all_results[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nSaved {len(all_results)} records to:")
    print(f"  - {csv_path}")
    print(f"  - {json_path}")


if __name__ == "__main__":
    test_prompts = [
        "Explain the difference between supervised and unsupervised learning in 3 sentences.",
        "Write a one-paragraph summary of why exercise is important for mental health.",
        "What are the top 3 advantages of using cloud computing for a small business?",
    ]

    all_results = []
    for prompt in test_prompts:
        results = compare_providers(prompt)
        print_comparison_table(results)
        all_results.extend(results)

    save_results(all_results,
                 csv_path="outputs/task1_llm_comparison.csv",
                 json_path="outputs/task1_llm_comparison.json")

    print(f"\nReal API calls completed.")
