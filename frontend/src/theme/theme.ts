import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        mode: "dark",

        primary: {
            main: "#4F8CFF",
        },

        background: {
            default: "#09090B",
            paper: "#1A202C",
        },

        text: {
            primary: "#F8FAFC",
            secondary: "#AAB4C5",
        },

        divider: "rgba(255,255,255,0.08)",
    },

    shape: {
        borderRadius: 20,
    },

    typography: {
        fontFamily: [
            "Inter",
            "Segoe UI",
            "Roboto",
            "Helvetica",
            "Arial",
            "sans-serif",
        ].join(","),

        h4: {
            fontWeight: 700,
            letterSpacing: "-0.5px",
        },

        h5: {
            fontWeight: 600,
        },

        body1: {
            fontSize: "1rem",
            lineHeight: 1.7,
        },

        body2: {
            fontSize: "0.92rem",
            lineHeight: 1.6,
        },
    },

    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundImage: "none",
                    backgroundColor: "#1A202C",
                    border: "1px solid rgba(255,255,255,0.08)",
                    boxShadow: "0 24px 80px rgba(0,0,0,0.45)",
                },
            },
        },

        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 14,
                    textTransform: "none",
                    fontWeight: 600,
                    paddingInline: 18,
                    transition: "all 0.2s ease",
                },

                contained: {
                    backgroundColor: "#4F8CFF",

                    "&:hover": {
                        backgroundColor: "#2563EB",
                        transform: "translateY(-2px)",
                        boxShadow: "0 8px 24px rgba(37,99,235,0.35)",
                    },
                },
            },
        },

        MuiTextField: {
            styleOverrides: {
                root: {
                    "& .MuiOutlinedInput-root": {
                        borderRadius: 14,

                        backgroundColor: "#252B36",

                        "& fieldset": {
                            borderColor: "#394150",
                        },

                        "&:hover fieldset": {
                            borderColor: "#4F8CFF",
                        },

                        "&.Mui-focused fieldset": {
                            borderColor: "#4F8CFF",
                        },
                    },
                },
            },
        },
    },
});

export default theme;