import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import theme from './theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static">
          <Toolbar>
            <Box component="img" src="/GALLO-NEW-LOGO-1.PNG" alt="Gallo" sx={{ height: 50, mr: 2 }} />
            <Typography variant="h5" component="h1" sx={{ fontWeight: 600 }}>
              SNSU Tracker
            </Typography>
          </Toolbar>
        </AppBar>
        <Box component="main" sx={{ flex: 1, p: 3, bgcolor: 'background.default' }}>
          {/* Dashboard content will go here */}
        </Box>
      </Box>
    </ThemeProvider>
  )
}

export default App
