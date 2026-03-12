# nlp.py — Fuzzy command matcher for flexible voice control

from fuzzywuzzy import fuzz

known_commands = {
    "open notepad": ["open notepad", "launch notepad", "start notepad"],
    "open calculator": ["open calculator", "launch calculator"],
    "open cmd": ["open command prompt", "start terminal", "launch cmd"],
    "open downloads": ["open downloads", "show downloads folder"],
    "move mouse": ["move mouse to top left", "mouse to corner"],
    "click": ["click", "press mouse", "left click"],
    "type": ["type"],
    "exit": ["exit", "shutdown astra", "quit assistant"]
}

def match_command(text):
    best_match = None
    highest_score = 0

    for key, phrases in known_commands.items():
        for phrase in phrases:
            score = fuzz.partial_ratio(text.lower(), phrase.lower())
            if score > highest_score:
                highest_score = score
                best_match = key

    return best_match if highest_score > 70 else None
