import { Box, Typography } from "@mui/material";

const ChatWindow = () => {
    return (
        <Box
            sx={{
                flex: 1,
                overflowY: "auto",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                px: 4,
            }}
        >
            <Box
                sx={{
                    textAlign: "center",
                    maxWidth: 550,
                }}
            >
                <Typography variant="h5" gutterBottom>
                    AI Auction Assistant
                </Typography>

                <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{
                        lineHeight: 1.8,
                        mt: 2,
                    }}
                >
                    Ask questions about players, compare teams, simulate auctions,
                    discover hidden talents and build smarter auction strategies using AI.
                </Typography>
            </Box>
        </Box>
    );
};

export default ChatWindow;