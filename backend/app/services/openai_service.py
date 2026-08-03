from openai import OpenAI
from app.core.config import settings
from app.prompts.auction_prompt import RAG_SYSTEM_PROMPT

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def stream_chat(message: str):
    openai_response_stream = client.responses.create(
        model="gpt-4.1-mini",
        instructions=RAG_SYSTEM_PROMPT,
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
