"""
Spelling Quiz Program
======================
This program reads a word aloud using text-to-speech, then asks you to
type its spelling. It tells you if you're right or wrong, and gives you
a final score report at the end (including a list of words you missed).

SETUP (run once in a terminal):
    pip install pyttsx3

    On Linux you may also need espeak installed:
        sudo apt-get install espeak

RUN:
    python spelling_quiz.py

TIPS while running:
    - Type your spelling and press Enter.
    - Type 'repeat' (no quotes) instead of a word to hear it again.
    - Type 'skip' to skip a word.
    - Press Ctrl+C at any time to quit early (your score so far will still show).
"""

import random
import sys

try:
    import pyttsx3
except ImportError:
    print("The 'pyttsx3' package is required for text-to-speech.")
    print("Install it with:  pip install pyttsx3")
    sys.exit(1)


WORDS = [
    "absorption", "accompaniment", "accomplice", "acquiesce", "acquittal",
    "affiliation", "altercation", "ambassador", "ambiguous", "animosity",
    "apparatus", "approximately", "austerity", "authentic", "authenticate",
    "auxiliary", "benevolent", "blasphemous", "bravado", "camouflage",
    "capricious", "carburetor", "cavalcade", "celestial", "cerebral",
    "chagrin", "chaotic", "chasm", "chastise", "chronic",
    "citadel", "clique", "cocoon", "conceivable", "concurrent",
    "conscientious", "consciousness", "contiguous", "correspondence", "corroborate",
    "curriculum", "defamation", "deprivation", "derelict", "diffidence",
    "disastrous", "dissociate", "distinction", "diurnal", "dominant",
    "dormitory", "drudgery", "elicit", "elimination", "embroidery",
    "equinox", "escapade", "espionage", "etiquette", "exaggeration",
    "exemplary", "expediency", "expedient", "expunge", "facsimile",
    "fallacy", "feasibility", "fictitious", "finesse", "fluorescent",
    "fulfill", "grammatically", "gruesome", "handkerchief", "hideous",
    "hindrance", "homogenize", "hypocrisy", "idiosyncrasy", "impasse",
    "impropriety", "incandescent", "incessant", "inconsolable", "indelible",
    "indispensable", "indisputable", "insufficient", "interrogative", "irreconcilable",
    "irrelevant", "irrevocable", "judicious", "justifiable", "labyrinth",
    "liaison", "lustrous", "magnanimous", "magnificence", "maintenance",
    "malicious", "martyr", "melee", "metamorphosis", "molecular",
    "monotony", "morose", "multiplicity", "nausea", "nonchalance",
    "notoriety", "oblique", "occasionally", "olfactory", "omnipotent",
    "onomatopoeia", "palatable", "pandemonium", "panorama", "partiality",
    "pastime", "patriarch", "pediatrician", "peril", "perjury",
    "philanthropist", "picturesque", "pittance", "playwright", "poignancy",
    "poignant", "potpourri", "prejudice", "premonition", "primitive",
    "proximity", "quibble", "quixotic", "quizzical", "recipient",
    "redundant", "reek", "relevancy", "remembrance", "renegade",
    "renovate", "reservoir", "respite", "retaliate", "retrieve",
    "rococo", "sabotage", "salient", "satisfactorily", "saunter",
    "scavenger", "scourge", "scuttle", "seethe", "significance",
    "soliloquy", "spasmodic", "squalid", "strenuous", "stringent",
    "subsequent", "subsistence", "succinct", "summarize", "supersede",
    "surgeon",
]


def say_word(word):
    # On Windows, reusing one pyttsx3 engine across multiple say/runAndWait
    # calls often breaks after the first word. Creating a fresh engine each
    # time is slower but far more reliable.
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # slow down a bit for clarity
    engine.say(word)
    engine.runAndWait()
    engine.stop()


def ask_shuffle():
    ans = input("Shuffle the word order? (y/n): ").strip().lower()
    return ans.startswith("y")


def run_quiz():
    print("=" * 50)
    print("SPELLING QUIZ")
    print("=" * 50)
    print(f"Total words: {len(WORDS)}")
    print("Type 'repeat' to hear a word again, or 'skip' to skip it.")
    print()

    words = WORDS.copy()
    if ask_shuffle():
        random.shuffle(words)

    input("Press Enter when you're ready to start...")

    correct = 0
    missed = []
    skipped = []

    total = len(words)
    try:
        for i, word in enumerate(words, start=1):
            print(f"\nWord {i} of {total}")
            say_word(word)

            while True:
                answer = input("Type the spelling: ").strip()

                if answer.lower() == "repeat":
                    say_word(word)
                    continue
                elif answer.lower() == "skip":
                    print(f"Skipped. The word was: {word}")
                    skipped.append(word)
                    break
                elif answer.lower() == word.lower():
                    print("Correct!")
                    correct += 1
                    break
                else:
                    print(f"Incorrect. The correct spelling is: {word}")
                    missed.append((word, answer))
                    break

    except KeyboardInterrupt:
        print("\n\nQuiz stopped early by user.")

    # ---- Final report ----
    attempted = correct + len(missed)
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Correct: {correct}")
    print(f"Missed:  {len(missed)}")
    print(f"Skipped: {len(skipped)}")
    if attempted:
        pct = (correct / attempted) * 100
        print(f"Accuracy (excluding skips): {pct:.1f}%")

    if missed:
        print("\nWords to review:")
        for word, your_answer in missed:
            print(f"  - {word}   (you typed: {your_answer})")

    if skipped:
        print("\nSkipped words:")
        for word in skipped:
            print(f"  - {word}")

    print("\nGreat work! Practice the missed words and try again.")


if __name__ == "__main__":
    run_quiz()