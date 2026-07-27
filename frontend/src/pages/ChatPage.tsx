import { useState } from "react";

import { Box, Container, Paper, Typography } from "@mui/material";

import ChatInput from "../components/chat/ChatInput";
import ChatWindow from "../components/chat/ChatWindow";
import { streamChat } from "../services/chatService";

export type Message = {
    id: string;
    role: "user" | "assistant";
    content: string;
};

const ChatPage = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async (message: string): Promise<void> => {
        if (!message.trim()) {
            return;
        }

        setLoading(true);

        const userMessage: Message = {
            id: crypto.randomUUID(),
            role: "user",
            content: message,
        };

        const assistantMessage: Message = {
            id: crypto.randomUUID(),
            role: "assistant",
            content: "",
        };

        setMessages((previousMessages) => [
            ...previousMessages,
            userMessage,
            assistantMessage,
        ]);

        try {
            await streamChat(message, (chunk) => {
                setMessages((previousMessages) =>
                    previousMessages.map((currentMessage) =>
                        currentMessage.id === assistantMessage.id
                            ? {
                                ...currentMessage,
                                content: currentMessage.content + chunk,
                            }
                            : currentMessage
                    )
                );
            });
        } catch (error) {
            console.error(error);

            setMessages((previousMessages) =>
                previousMessages.map((currentMessage) =>
                    currentMessage.id === assistantMessage.id
                        ? {
                            ...currentMessage,
                            content:
                                "Something went wrong. Please try again.",
                        }
                        : currentMessage
                )
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            sx={{
                minHeight: "100vh",
                display: "flex",
                alignItems: "center",
                background:
                    "radial-gradient(circle at top, #243447 0%, #111827 45%, #09090B 100%)",
            }}
        >
            <Container maxWidth="lg">
                <Paper
                    sx={{
                        height: "90vh",
                        display: "flex",
                        flexDirection: "column",
                        overflow: "hidden",
                    }}
                >
                    <Box
                        sx={{
                            px: 4,
                            py: 3,
                            borderBottom: 1,
                            borderColor: "divider",
                        }}
                    >
                        <Typography variant="h4">
                            AI Auction Intelligence Platform
                        </Typography>

                        <Typography color="text.secondary">
                            AI-powered player analysis, auction insights and
                            cricket intelligence.
                        </Typography>
                    </Box>

                    <ChatWindow
                        messages={messages}
                        loading={loading}
                    />

                    <ChatInput onSend={handleSend} />
                </Paper>
            </Container>
        </Box>
    );
};

export default ChatPage;