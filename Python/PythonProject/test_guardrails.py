from guardrails import Guard, OnFailAction
from guardrails.hub import ToxicLanguage

guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION)
)

guard.validate(
    """An apple a day keeps a doctor away.
    This is good advice for keeping your health."""
)  # Both the guardrails pass

try:
    guard.validate(
        """Shut the hell up! Apple just released a new iPhone."""
    )  # Both the guardrails fail
except Exception as e:
    print(e)