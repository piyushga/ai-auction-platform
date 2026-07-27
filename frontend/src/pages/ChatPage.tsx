import { Box, Container, Paper, Typography } from "@mui/material";

import ChatInput from "../components/chat/ChatInput";
import ChatWindow from "../components/chat/ChatWindow";

const ChatPage = () => {
    return (
        <Box
            sx={{
                minHeight: "100vh",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background:
                    "radial-gradient(circle at top, #2C3E50 0%, #1B263B 40%, #0F172A 100%)",
                px: 3,
                py: 4,
            }}
        >
            <Container maxWidth="lg">
                <Paper
                    elevation={0}
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

                        <Typography
                            variant="body2"
                            color="text.secondary"
                            sx={{ mt: 1 }}
                        >
                            AI-powered player analysis, auction strategy and team recommendations.
                        </Typography>
                    </Box>

                    <ChatWindow />

                    <ChatInput />
                </Paper>
            </Container>
        </Box>
    );
};

export default ChatPage;