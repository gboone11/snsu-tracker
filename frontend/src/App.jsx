import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import SettingsIcon from "@mui/icons-material/Settings";
import theme from "./theme";
import LinesStatusBoard from "./components/LinesStatusBoard";
import LineConfigPage from "./components/LineConfigPage";
import LineDetailPage from "./components/LineDetailPage";

function AppContent() {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <AppBar position="static">
        <Toolbar>
          <Box
            component="img"
            src="/GALLO-NEW-LOGO-1.PNG"
            alt="Gallo"
            sx={{ height: 50, mr: 2 }}
          />
          <Button
            color="inherit"
            onClick={() => navigate("/")}
            sx={{ flexGrow: 1, justifyContent: "flex-start" }}
          >
            <Typography variant="h5" component="h1" sx={{ fontWeight: 600 }}>
              SNSU Tracker
            </Typography>
          </Button>
          <IconButton color="inherit" onClick={() => navigate("/config")}>
            <SettingsIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box
        component="main"
        sx={{ flex: 1, p: 3, bgcolor: "background.default" }}
      >
        <Routes>
          <Route path="/" element={<LinesStatusBoard />} />
          <Route path="/config" element={<LineConfigPage />} />
          <Route path="/line/:lineId" element={<LineDetailPage />} />
        </Routes>
      </Box>
    </Box>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <BrowserRouter>
          <AppContent />
        </BrowserRouter>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;
