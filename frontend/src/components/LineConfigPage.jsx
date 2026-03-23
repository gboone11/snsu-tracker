import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import LinesConfigPanel from "./LinesConfigPanel";
import ProcessStepsConfigPanel from "./ProcessStepsConfigPanel";

function LineConfigPage() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600, textAlign: "left" }}>
        Configuration
      </Typography>
      <Box sx={{ display: "flex", gap: 3 }}>
        <LinesConfigPanel />
        <ProcessStepsConfigPanel />
      </Box>
    </Box>
  );
}

export default LineConfigPage;
