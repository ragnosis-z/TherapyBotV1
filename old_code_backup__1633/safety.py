def safety_check(user_input: str) -> str:
    risky_phrases = ["i want to die", "no one else matters"]

    for phrase in risky_phrases:
        if phrase in user_input.lower():
            return (
                "That sounds really overwhelming. "
                "You don’t have to face it alone, and "
                "it might help to reach out to someone you trust."
            )

    return None
