import { Box, Container, Paper, Typography } from "@mui/material";

import ChatInput from "../components/chat/ChatInput";
import ChatWindow from "../components/chat/ChatWindow";

const ChatPage = () => {
    return (
        <Container maxWidth="md">
            <Box sx={{ py: 4 }}>
                <Typography
                    variant="h4"
                    fontWeight={700}
                    textAlign="center"
                    gutterBottom
                >
                    AI Auction Intelligence Platform
                </Typography>

                <Typography
                    variant="body1"
                    color="text.secondary"
                    textAlign="center"
                    mb={4}
                >
                    Ask anything about players, teams, auctions and strategies.
                </Typography>

                <Paper
                    elevation={3}
                    sx={{
                        height: "75vh",
                        display: "flex",
                        flexDirection: "column",
                        borderRadius: 4,
                        overflow: "hidden",
                    }}
                >
                    <ChatWindow />

                    <ChatInput />
                </Paper>
            </Box>
        </Container>
    );
};

export default ChatPage;