import re

phrases = (
    (re.compile(r".*(ඞ|sus).*", re.IGNORECASE), "thats pretty sus if you ask me"),
    (re.compile(r"bad recursion", re.IGNORECASE), "bad recursion"),
    (re.compile(r".*get good.*", re.IGNORECASE), "play more"),
    # if you mention a vtuber it will reply "touch grass"
    (re.compile(r".*(gawr|gura|kizuna|mori|hololive|inugami|\
                shirakami|houshou|nyanners|peko|hime|nekomata|\
                watson|sakura|minato|snuffy|colon).*", re.IGNORECASE), "touch grass"),
)


def check_phrase(msg):
    for key, value in phrases:
        if key.match(msg):
            return value