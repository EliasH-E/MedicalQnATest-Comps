
import csv
import textstat
from pathlib import Path

INPUT_FILE = "outputs.csv"
OUTPUT_FILE = "evaluation_results.csv"


def evaluate_readability(original, simplified):
    # Flesch-Kincaid Grade Level
    original_fk = textstat.flesch_kincaid_grade(original)
    simplified_fk = textstat.flesch_kincaid_grade(simplified)

    # Coleman-Liau Index
    original_cli = textstat.coleman_liau_index(original)
    simplified_cli = textstat.coleman_liau_index(simplified)

    return {
        "original_fk": original_fk,
        "simplified_fk": simplified_fk,
        "fk_change": simplified_fk - original_fk,

        "original_cli": original_cli,
        "simplified_cli": simplified_cli,
        "cli_change": simplified_cli - original_cli
    }


def evaluate_dataset():
    results = []

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required = {"original_answer", "simplified_answer"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV must contain original_answer and simplified_answer"
            )

        for row in reader:
            original = row["original_answer"]
            simplified = row["simplified_answer"]

            if not original or not simplified:
                continue

            scores = evaluate_readability(original, simplified)

            results.append({
                **row,
                **scores
            })

            print("\nOriginal:", original)
            print("Simplified:", simplified)
            print("FK Change:", scores["fk_change"])
            print("CLI Change:", scores["cli_change"])

    if not results:
        print("No valid answers found.")
        return

    # saves inidividual scores in a CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nEvaluated {len(results)} answers.")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    if Path(INPUT_FILE).exists():
        evaluate_dataset()
    else:
        original_answer = (
            "Hypertension is a chronic medical condition "
            "characterized by elevated arterial blood pressure."
        )

        simplified_answer = (
            "High blood pressure means the force of blood "
            "in your arteries stays too high."
        )

        scores = evaluate_readability(
            original_answer,
            simplified_answer
        )

        print("Original:", original_answer)
        print("Simplified:", simplified_answer)

        for metric, value in scores.items():
            print(f"{metric}: {value}")