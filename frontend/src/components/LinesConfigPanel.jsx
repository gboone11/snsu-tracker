import { useState, useEffect } from "react";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { apiService } from "../services/api";

function LinesConfigPanel() {
  const [lines, setLines] = useState([]);
  const [newLine, setNewLine] = useState("");

  useEffect(() => {
    apiService.lines.getAll()
      .then((res) => setLines(res.data.data))
      .catch((err) => console.error("Error fetching lines:", err));
  }, []);

  const handleAdd = async () => {
    const lineNum = newLine.trim();
    if (!lineNum) return;
    if (lines.some((l) => l.line_number === lineNum)) {
      alert("Line already exists");
      return;
    }
    try {
      await apiService.lines.create({ line_number: lineNum });
      const res = await apiService.lines.getAll();
      setLines(res.data.data);
      setNewLine("");
    } catch (error) {
      alert("Error adding line: " + error.message);
    }
  };

  const handleRemove = async (line) => {
    if (!window.confirm(`Remove Line ${line.line_number}?`)) return;
    try {
      await apiService.lines.delete(line.line_id);
      setLines(lines.filter((l) => l.line_id !== line.line_id));
    } catch (error) {
      alert("Error removing line: " + error.message);
    }
  };

  return (
    <Paper sx={{ p: 2.5, mb: 3, bgcolor: "background.paper" }}>
      <Typography variant="h6" sx={{ mb: 2, color: "primary.main" }}>
        Lines
      </Typography>
      <Box sx={{ display: "flex", gap: 1, mb: 2 }}>
        <TextField
          size="small"
          placeholder="Line number (e.g., 101)"
          value={newLine}
          onChange={(e) => setNewLine(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleAdd()}
          sx={{ width: 250 }}
        />
        <Button variant="contained" onClick={handleAdd}>
          + Add Line
        </Button>
      </Box>
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
        {lines.map((line) => (
          <Box
            key={line.line_id}
            sx={{
              bgcolor: "background.default",
              px: 1.5,
              py: 0.75,
              borderRadius: 1,
              display: "flex",
              alignItems: "center",
              gap: 1,
            }}
          >
            <Typography variant="body2">Line {line.line_number}</Typography>
            <IconButton
              size="small"
              sx={{ p: 0.25, color: "error.main" }}
              onClick={() => handleRemove(line)}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>
        ))}
        {lines.length === 0 && (
          <Typography variant="body2" sx={{ color: "text.secondary", fontStyle: "italic" }}>
            No lines configured
          </Typography>
        )}
      </Box>
    </Paper>
  );
}

export default LinesConfigPanel;
