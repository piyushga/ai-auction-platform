import { Box, Button, TextField } from "@mui/material";

const ChatInput = () => {
    return (
        <Box
            sx={{
                display: "flex",
                gap: 2,
                p: 2,
                borderTop: "1px solid #e0e0e0",
            }}
        >
            <TextField
                fullWidth
                placeholder="Ask about players, teams or auctions..."
                variant="outlined"
            />

            <Button variant="contained">
                Send
            </Button>
        </Box>
    );
};

export default ChatInput;