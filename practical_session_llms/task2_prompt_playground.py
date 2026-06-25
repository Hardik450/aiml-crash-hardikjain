import json
from datetime import datetime
import pandas as pd

from llm_clients import call_groq

df = pd.read_csv("BBCNews.csv")

PROMPT_VARIANTS = {
    "1_naive": (
        "Summarize this article: {article}"
    ),
    "2_role_based": (
        "You are an expert news editor with 20 years of experience writing concise, "
        "accurate summaries for busy readers. Summarize the following article in a "
        "way that captures the most newsworthy points:\n\n{article}"
    ),
    "3_structured_format": (
        "Summarize the following article in exactly 3 bullet points, each under "
        "15 words, covering: (1) what happened, (2) why it matters, (3) what happens "
        "next.\n\nArticle:\n{article}"
    ),
    "4_few_shot": (
        "Here is an example of a good news summary:\n"
        "Example article: 'The city approved a new park budget of $2M, to be spent "
        "on playgrounds and trails, after years of resident requests.'\n"
        "Example summary: 'City approved a $2M park budget for playgrounds and "
        "trails after sustained resident demand.'\n\n"
        "Now summarize this article in the same style (one sentence, neutral tone):\n\n"
        "{article}"
    ),
    "5_chain_of_thought": (
        "First, identify the 3 most important facts in this article. Then, using "
        "only those facts, write a single concise summary paragraph (max 40 words). "
        "Show your reasoning step by step, then give the final summary clearly "
        "labeled 'FINAL SUMMARY:'.\n\nArticle:\n{article}"
    ),
}


def score_summary(text: str) -> dict:
    """
    Simple, transparent scoring heuristic (no LLM-as-judge needed):
      - length_score: rewards summaries that are concise but not too short
      - structure_score: rewards presence of clear structure (bullets/labels)
      - word_count: raw word count for reference
    This keeps evaluation objective and reproducible.
    """
    word_count = len(text.split())
    # Ideal summary range: 15-60 words
    if 15 <= word_count <= 60:
        length_score = 10
    elif word_count < 15:
        length_score = 5
    else:
        length_score = max(0, 10 - (word_count - 60) // 10)

    structure_score = 0
    if any(marker in text for marker in ["•", "-", "1.", "2.", "FINAL SUMMARY"]):
        structure_score += 5
    if text.strip().endswith((".", "!", "?")):
        structure_score += 2

    total_score = length_score + structure_score
    return {"word_count": word_count, "length_score": length_score,
            "structure_score": structure_score, "total_score": total_score}


def run_playground() -> list[dict]:
    results = []
    n = 10
    for idx, row in df.head(n).iterrows():
        article = str(row['descr']).strip()
        for name, template in PROMPT_VARIANTS.items():
            prompt = template.format(article=article[:1000])
            print(f"\nTesting prompt variant: {name}")
            result = call_groq(prompt, system_prompt="You are a helpful summarization assistant.")
            scores = score_summary(result["text"])

            record = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "prompt_variant": name,
                "prompt_text": prompt,
                "response_text": result["text"],
                "response_time_sec": result["response_time_sec"],
                "total_tokens": result["total_tokens"],
                **scores,
            }
            results.append(record)
            print(f"  -> {scores['word_count']} words | score: {scores['total_score']}/17")
    return results


def save_and_report(results: list[dict]) -> None:
    with open("outputs/task2_prompt_playground.json", "w") as f:
        json.dump(results, f, indent=2)

    df = pd.DataFrame(results)
    df.to_csv("outputs/task2_prompt_playground.csv", index=False)

    print("\n" + "=" * 70)
    print("PROMPT COMPARISON SUMMARY")
    print("=" * 70)
    summary_table = df[["prompt_variant", "word_count", "total_score", "response_time_sec"]]
    summary_table = summary_table.sort_values("total_score", ascending=False)
    print(summary_table.to_string(index=False))

    best = df.loc[df["total_score"].idxmax()]
    print("\n" + "=" * 70)
    print(f"BEST PROMPT: {best['prompt_variant']}  (score: {best['total_score']}/17)")
    print("=" * 70)
    print(f"Response:\n{best['response_text']}")

    print(f"\nSaved outputs/task2_prompt_playground.csv and .json")
    print(f"Real API calls completed.")


if __name__ == "__main__":
    results = run_playground()
    save_and_report(results)
