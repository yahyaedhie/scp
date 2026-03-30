import tiktoken

class TokenCounter:
    def __init__(self):
        self.encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text."""
        return len(self.encoding.encode(text))

    def measure_compression_efficiency(self, original_text: str, compressed_text: str) -> float:
        """Calculate the compression efficiency of the given texts."""
        original_tokens = self.count_tokens(original_text)
        compressed_tokens = self.count_tokens(compressed_text)
        return (original_tokens - compressed_tokens) / original_tokens if original_tokens > 0 else 0.0

    def track_conversation_metrics(self, conversation: list) -> dict:
        """Track conversation metrics such as total tokens used."""
        total_tokens = 0
        for message in conversation:
            total_tokens += self.count_tokens(message)
        return {'total_tokens': total_tokens}

# Example usage
token_counter = TokenCounter()
text = "[WAR] affects markets significantly."
text2 = ("The Semantic Compression Protocol solves meaning drift in long AI conversations by using anchors "
         "to define concepts once and reference them efficiently throughout the session.")
text3 = ("def check_drift(text: str, domain: str = \"market\") -> list[DriftEvent]: "
         "events: list[DriftEvent] = [] "
         "codes = await extract_codes(text) "
         "for code in codes: "
         "anchor = await resolve_code(code, domain) "
         "if not anchor: "
         "    events.append(DriftEvent(...))")

text4 = ("[SCP] prevents drift by storing anchors once and referencing them.")

print(f'Tokens in text: {token_counter.count_tokens(text)}')
print(f'Tokens in text2: {token_counter.count_tokens(text2)}')
print(text3)
print(f'Tokens in text3: {token_counter.count_tokens(text3)}')
print(f'Tokens in text4: {token_counter.count_tokens(text4)}')

