import { Box, Paper, Typography } from "@mui/material";

type Message = {
    id: string;
    role: "user" | "assistant";
    content: string;
};

type ChatWindowProps = {
    messages: Message[];
    loading: boolean;
};

const ChatWindow = ({ messages, loading }: ChatWindowProps) => {
    if (messages.length === 0) {
        return (
            <Box
                sx={{
                    flex: 1,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexDirection: "column",
                    gap: 2,
                    px: 4,
                }}
            >
                <Typography variant="h5">
                    Welcome to AI Auction Intelligence
                </Typography>

                <Typography color="text.secondary">
                    Ask anything about players, teams, auctions and match insights.
                </Typography>
            </Box>
        );
    }

    return (
        <Box
            sx={{
                flex: 1,
                overflowY: "auto",
                p: 3,
                display: "flex",
                flexDirection: "column",
                gap: 2,
            }}
        >
            {messages.map((message) => {
                const isError =
                    message.role === "assistant" &&
                    message.content ===
                    "Something went wrong. Please try again.";

                const isThinking =
                    loading &&
                    message.role === "assistant" &&
                    message.content === "";

                return (
                    <Box
                        key={message.id}
                        sx={{
                            display: "flex",
                            justifyContent:
                                message.role === "user"
                                    ? "flex-end"
                                    : "flex-start",
                        }}
                    >
                        <Paper
                            elevation={0}
                            sx={{
                                px: 2,
                                py: 1.5,
                                maxWidth: "70%",
                                width: "fit-content",
                                borderRadius: 1,
                                border: "1px solid",
                                borderColor: isError
                                    ? "error.main"
                                    : "divider",
                                bgcolor: isError
                                    ? "rgba(244,67,54,0.12)"
                                    : "background.paper",
                            }}
                        >
                            {isThinking ? (
                                <Typography
                                    sx={{
                                        fontSize: "1.5rem",
                                        lineHeight: 1,
                                        letterSpacing: 4,
                                        color: "text.secondary",
                                        animation:
                                            "pulse 1.2s infinite ease-in-out",
                                        "@keyframes pulse": {
                                            "0%": { opacity: 0.3 },
                                            "50%": { opacity: 1 },
                                            "100%": { opacity: 0.3 },
                                        },
                                    }}
                                >
                                    ...
                                </Typography>
                            ) : (
                                <Typography
                                    variant="body1"
                                    color={
                                        isError
                                            ? "error.main"
                                            : "text.primary"
                                    }
                                    whiteSpace="pre-wrap"
                                >
                                    {message.content}
                                </Typography>
                            )}
                        </Paper>


                    </Box>
                );
            })}
        </Box>
    );
};

export default ChatWindow;