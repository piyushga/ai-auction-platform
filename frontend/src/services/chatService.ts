import { API_BASE_URL } from "../config/api";

export const streamChat = async (
    message: string,
    onChunk: (chunk: string) => void
): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message,
        }),
    });

    if (!response.body) {
        throw new Error("No response stream received.");
    }

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();

        if (done) {
            break;
        }

        onChunk(decoder.decode(value));
    }
};