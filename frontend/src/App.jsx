import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import theme from './theme';
import LinesStatusBoard from './components/LinesStatusBoard';
import LineConfigPage from './components/LineConfigPage';

function App() {
  const [currentPage, setCurrentPage] = useState('status');

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static">
          <Toolbar>
            <Box component="img" src="/GALLO-NEW-LOGO-1.PNG" alt="Gallo" sx={{ height: 50, mr: 2 }} />
            <Typography variant="h5" component="h1" sx={{ fontWeight: 600, flexGrow: 1 }}>
              SNSU Tracker
            </Typography>
            <Button 
              color="inherit" 
              onClick={() => setCurrentPage('status')}
              sx={{ fontWeight: currentPage === 'status' ? 700 : 400 }}
            >
              📊 Lines Status
            </Button>
            <Button 
              color="inherit" 
              onClick={() => setCurrentPage('config')}
              sx={{ fontWeight: currentPage === 'config' ? 700 : 400 }}
            >
              🔧 Line Config
            </Button>
          </Toolbar>
        </AppBar>
        <Box component="main" sx={{ flex: 1, p: 3, bgcolor: 'background.default' }}>
          {currentPage === 'status' ? <LinesStatusBoard /> : <LineConfigPage />}
        </Box>
      </Box>
    </ThemeProvider>
  )
}

export default App
