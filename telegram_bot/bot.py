from crew_ai.planner import evaluate_token

def handle_message(message: str) -> str:
    """
    Handles incoming Telegram user commands.
    Provides sub-millisecond responses by calling the optimized evaluate_token function.
    """
    print(f"Bot received message: {message}")
    if message.startswith("/evaluate "):
        parts = message.split(" ", 1)
        if len(parts) < 2:
            return "Please provide a token name."
        token = parts[1].strip().upper()
        score = evaluate_token(token)
        return f"Token {token} has a score of {score}/1000."
    return "Unknown command."

if __name__ == "__main__":
    print("Telegram bot simulation initialized.")
    # Run a quick self-test of the handler
    response = handle_message("/evaluate btc")
    print(f"Bot response: {response}")
