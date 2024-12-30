from mistral_common.protocol.instruct.messages import (
    AssistantMessage,
    UserMessage,
    ToolMessage
)
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.tool_calls import Function, Tool, ToolCall, FunctionCall
from mistral_common.protocol.instruct.request import ChatCompletionRequest

def calculate_and_print_tokens():
    tokenizer_v3 = MistralTokenizer.v3()

    tokenized = tokenizer_v3.encode_chat_completion(
        ChatCompletionRequest(
            tools=[
                Tool(
                    function=Function(
                        name="get_current_weather",
                        description="Get the current weather",
                        parameters={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "format": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                    "description": "The temperature unit to use. Infer this from the users location.",
                                },
                            },
                            "required": ["location", "format"],
                        },
                    )
                )
            ],
            messages=[
                UserMessage(content="What's the weather like today in Paris"),
                AssistantMessage(
                    content=None,
                    tool_calls=[
                        ToolCall(
                            id="VvvODy9mT",
                            function=FunctionCall(
                                name="get_current_weather",
                                arguments='{"location": "Paris, France", "format": "celsius"}',
                            ),
                        )
                    ],
                ),
                ToolMessage(
                    tool_call_id="VvvODy9mT", name="get_current_weather", content="22"
                ),
                AssistantMessage(
                    content="The current temperature in Paris, France is 22 degrees Celsius.",
                ),
                UserMessage(content="What's the weather like today in San Francisco"),
                AssistantMessage(
                    content=None,
                    tool_calls=[
                        ToolCall(
                            id="fAnpW3TEV",
                            function=FunctionCall(
                                name="get_current_weather",
                                arguments='{"location": "San Francisco", "format": "celsius"}',
                            ),
                        )
                    ],
                ),
                ToolMessage(
                    tool_call_id="fAnpW3TEV", name="get_current_weather", content="20"
                ),
            ],
            model="test",
        )
    )

    tokens, text = tokenized.tokens, tokenized.text

    print("Tokens:", tokens)
    print("Text:", text)

# Call the function
calculate_and_print_tokens()
