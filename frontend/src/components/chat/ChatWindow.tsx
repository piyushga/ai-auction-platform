import { Box, Typography } from "@mui/material";

const ChatWindow = () => {
    return (
        <Box
            sx={{
                flex: 1,
                overflowY: "auto",
                p: 3,
                backgroundColor: "#fafafa",
            }}
        >
            <Typography color="text.secondary">
                Start a conversation with the AI Auction Assistant...
            </Typography>
        </Box>
    );
};

export default ChatWindow;