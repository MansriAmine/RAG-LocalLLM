from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

def prepare_for_tokenization(input_text):
    tokenizer_v3 = MistralTokenizer.v3()

    tokenized = tokenizer_v3.encode_chat_completion(
        ChatCompletionRequest(
            messages=[
                UserMessage(content=input_text)
            ],
            model="test",
        )
    )

    return tokenized.tokens, tokenized.text

# Example usage
example_text = "tell me a joke "
tokens, text = prepare_for_tokenization(example_text)
print("Tokens:", tokens)
print("Text:", text)
print("Total number of tokens:", len(tokens))