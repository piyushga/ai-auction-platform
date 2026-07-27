import { useState } from "react";

import SendRoundedIcon from "@mui/icons-material/SendRounded";
import { Box, Button, TextField } from "@mui/material";

type ChatInputProps = {
    onSend: (message: string) => void;
};

const ChatInput = ({ onSend }: ChatInputProps) => {
    const [message, setMessage] = useState("");

    const handleSend = () => {
        if (!message.trim()) {
            return;
        }

        onSend(message);

        setMessage("");
    };

    return (
        <Box
            sx={{
                p: 3,
                borderTop: 1,
                borderColor: "divider",
            }}
        >
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 2,
                }}
            >
                <TextField
                    fullWidth
                    placeholder="Ask anything about players, teams or auctions..."
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                    onKeyDown={(event) => {
                        if (event.key === "Enter") {
                            handleSend();
                        }
                    }}
                />

                <Button
                    variant="contained"
                    endIcon={<SendRoundedIcon />}
                    onClick={handleSend}
                    sx={{
                        minWidth: 120,
                        height: 56,
                    }}
                >
                    Send
                </Button>
            </Box>
        </Box>
    );
};

export default ChatInput;