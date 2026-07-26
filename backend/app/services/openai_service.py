from openai import OpenAI

from app.core.config import OPENAI_API_KEY
from app.prompts.auction_prompt import SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)


def stream_chat(message: str):
    openai_response_stream = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=message,
        stream=True,
    )

    # Read each event sent by OpenAI
    for event in openai_response_stream:

        # Process only text events
        # Example: event.type = "response.output_text.delta"
        if event.type == "response.output_text.delta":

            # event.delta contains only the newly generated text
            # Example: "How", " are", " you?"
            yield event.delta