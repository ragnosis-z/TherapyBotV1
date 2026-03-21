"""Safety checks and crisis detection"""

import logging

logger = logging.getLogger(__name__)


def detect_crisis_keywords(message: str) -> bool:
    """
    Detect if message contains crisis keywords

    Args:
        message: User message

    Returns:
        True if crisis detected, False otherwise
    """
    crisis_phrases = [
        "i want to die",
        "no one else matters",
        "kill myself",
        "end it",
        "hurt myself",
        "self harm",
    ]

    message_lower = message.lower()
    for phrase in crisis_phrases:
        if phrase in message_lower:
            logger.warning(f"Crisis keyword detected: {phrase}")
            return True

    return False


def get_crisis_response(crisis_type: str) -> str:
    """
    Get appropriate crisis response

    Args:
        crisis_type: Type of crisis (suicide, self_harm, etc.)

    Returns:
        Crisis response message
    """
    responses = {
        "suicide": (
            "That sounds really overwhelming. "
            "You don't have to face it alone. "
            "Please reach out to someone you trust or contact the 988 Suicide & Crisis Lifeline: "
            "Call or text 988 (US)"
        ),
        "self_harm": (
            "I'm concerned about what you're sharing. "
            "Hurting yourself is a sign you're in real pain. "
            "You deserve support from someone trained to help. "
            "Please reach out: 988 Suicide & Crisis Lifeline or Crisis Text Line (Text HOME to 741741)"
        ),
        "severe_distress": (
            "This sounds incredibly difficult. "
            "What you're feeling is real and valid. "
            "Please consider reaching out for professional support. "
            "Crisis resources are available 24/7: 988 (call or text) or Crisis Text Line"
        ),
    }

    return responses.get(
        crisis_type,
        (
            "I'm concerned about your wellbeing. "
            "Please reach out for professional support. "
            "988 Suicide & Crisis Lifeline is available 24/7."
        ),
    )


def is_safety_violation(message: str) -> bool:
    """
    Check if message contains safety violations

    Args:
        message: User message

    Returns:
        True if violation detected
    """
    # Implement additional safety checks
    return detect_crisis_keywords(message)
