import SendRoundedIcon from "@mui/icons-material/SendRounded";
import { Box, Button, TextField } from "@mui/material";

const ChatInput = () => {
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
                />

                <Button
                    variant="contained"
                    endIcon={<SendRoundedIcon />}
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