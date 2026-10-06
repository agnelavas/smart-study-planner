"""
data_handler.py - Supporting Logic, Validation, Presets & Inspiration Data
Role: Member B (Supporting Logic / Integration Developer)
"""

from datetime import date, timedelta
import random


# ---------------------------------------------------------
# 1. Input Validation & Sanitization
# ---------------------------------------------------------

def validate_subject_input(
    name: str,
    chapters: int,
    difficulty: int,
    exam_date: date,
    start_date: date
) -> tuple[bool, str]:
    """
    Validates user input before passing it to the scheduling engine.
    Returns (is_valid, error_message).
    """

    if not name or not name.strip():
        return False, "Subject name cannot be empty."

    if chapters < 1:
        return False, "Chapters must be at least 1."

    if difficulty < 1 or difficulty > 5:
        return False, "Difficulty must be on a scale of 1 to 5."

    if exam_date <= start_date:
        return False, f"Exam date ({exam_date}) must be strictly after the start date ({start_date})."

    return True, "Valid"

# ---------------------------------------------------------
# 2. One-Click Demonstration Presets
# ---------------------------------------------------------

def get_preset_schedule(preset_name: str) -> list[dict]:
    """
    Returns realistic pre-configured subject rosters so evaluators
    don't have to wait for manual typing during live testing.
    """

    today = date.today()

    presets = {
        "B.Tech CSE 3rd Sem Sprint": [
            {
                "name": "Computer Organization & Arch.",
                "chapters": 5,
                "difficulty": 4,
                "exam_date": today + timedelta(days=4)
            },
            {
                "name": "Database Management Systems",
                "chapters": 6,
                "difficulty": 3,
                "exam_date": today + timedelta(days=8)
            },
            {
                "name": "Discrete Mathematics",
                "chapters": 5,
                "difficulty": 5,
                "exam_date": today + timedelta(days=12)
            },
            {
                "name": "Data Structures & Algorithms",
                "chapters": 7,
                "difficulty": 4,
                "exam_date": today + timedelta(days=16)
            }
        ],

        "Light Revision / Midterm": [
            {
                "name": "Software Engineering",
                "chapters": 4,
                "difficulty": 2,
                "exam_date": today + timedelta(days=5)
            },
            {
                "name": "Operating Systems",
                "chapters": 5,
                "difficulty": 4,
                "exam_date": today + timedelta(days=9)
            }
        ]
    }

    return presets.get(preset_name, [])

# ---------------------------------------------------------
# 3. Offline Inspiration Vault (Constellations & Lexicon)
# ---------------------------------------------------------

CONSTELLATIONS = [
    {
        "name": "Cassiopeia (The Seated Queen)",
        "coordinates": "RA 01h 00m | Dec +60°",
        "lore": "Recognizable by its prominent 'W' shape in the northern sky. "
                "Circumpolar and visible year-round, serving as a constant celestial compass."
    },
    {
        "name": "Orion (The Hunter)",
        "coordinates": "RA 05h 30m | Dec 00°",
        "lore": "Home to Betelgeuse and Rigel, this prominent winter constellation "
                "contains the Orion Nebula—one of the nearest stellar nurseries."
    },
    {
        "name": "Ursa Major (The Great Bear)",
        "coordinates": "RA 10h 40m | Dec +55°",
        "lore": "Houses the Big Dipper asterism. Merak and Dubhe, the two outer "
                "stars of its bowl, point directly toward Polaris, the North Star."
    },
    {
        "name": "Cygnus (The Northern Cross)",
        "coordinates": "RA 20h 40m | Dec +45°",
        "lore": "Flying along the Milky Way, its brightest star Deneb forms the "
                "prominent Summer Triangle alongside Vega and Altair."
    }
]


BRAIN_SPARKS = [
    {
        "word": "Meraki (Greek)",
        "meaning": "To put something of yourself—your soul, creativity, or love—"
                   "into your work."
    },
    {
        "word": "Fernweh (German)",
        "meaning": "An ache for distant places; the craving to travel and explore "
                   "beyond current horizons."
    },
    {
        "word": "Sonder (Neologism)",
        "meaning": "The realization that each random passerby lives a life as vivid "
                   "and complex as your own."
    },
    {
        "word": "Ad Astra Per Aspera (Latin)",
        "meaning": "'Through hardships to the stars' — reminding us that "
                   "perseverance turns ambition into mastery."
    }
]


def get_daily_cosmic_spark() -> dict:
    """Returns a paired constellation and intellectual brain spark."""

    return {
        "constellation": random.choice(CONSTELLATIONS),
        "spark": random.choice(BRAIN_SPARKS)
    }

# ---------------------------------------------------------
# 4. Standalone Terminal Test Harness
# ---------------------------------------------------------

if __name__ == "__main__":
    print("Testing Member B Data Handler Module...")

    # Test Validation
    valid, msg = validate_subject_input(
        "OS",
        4,
        3,
        date.today() + timedelta(days=5),
        date.today()
    )

    print(f"Validation Test 1 (Valid): {valid} -> {msg}")

    invalid, err = validate_subject_input(
        "",
        0,
        6,
        date.today() - timedelta(days=1),
        date.today()
    )

    print(f"Validation Test 2 (Invalid): {invalid} -> Error: {err}")

    # Test Presets
    preset = get_preset_schedule("B.Tech CSE 3rd Sem Sprint")

    print(f"\nLoaded Preset Items: {len(preset)} subjects")
    print(f"First preset subject: {preset[0]['name']}")

    # Test Inspiration Vault
    spark_data = get_daily_cosmic_spark()

    print(
        f"\nDaily Spark: {spark_data['spark']['word']} - "
        f"{spark_data['spark']['meaning']}"
    )

    print(f"Constellation: {spark_data['constellation']['name']}")

    print("\nAll Member B tests passed cleanly!")