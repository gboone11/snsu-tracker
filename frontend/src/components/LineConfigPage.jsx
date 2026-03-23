import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import LinesConfigPanel from "./LinesConfigPanel";
import ProcessStepsConfigPanel from "./ProcessStepsConfigPanel";

function LineConfigPage() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 600, textAlign: "center" }}>
        Line Configuration
      </Typography>
      <LinesConfigPanel />
      <ProcessStepsConfigPanel />
    </Box>
  );
}

export default LineConfigPage;
