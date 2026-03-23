import { useState, useEffect } from "react";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
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
    const lineNum = parseInt(newLine.trim(), 10);
    if (!lineNum || lineNum <= 0) {
      alert("Please enter a valid positive number");
      return;
    }
    try {
      await apiService.lines.create({ line_number: lineNum });
      const res = await apiService.lines.getAll();
      setLines(res.data.data);
      setNewLine("");
    } catch (error) {
      if (error.response?.status === 409) {
        alert(error.response.data.detail);
      } else {
        alert("Error adding line: " + error.message);
      }
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

  const handleMove = async (index, direction) => {
    const swapIndex = index + direction;
    if (swapIndex < 0 || swapIndex >= lines.length) return;
    const reordered = [...lines];
    [reordered[index], reordered[swapIndex]] = [reordered[swapIndex], reordered[index]];
    setLines(reordered);
    try {
      await apiService.lines.reorder(reordered.map((l) => l.line_id));
    } catch (error) {
      console.error("Error reordering lines:", error);
    }
  };

  return (
    <Paper sx={{ flex: 1, p: 2.5, bgcolor: "background.paper" }}>
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
      <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
        {lines.map((line, i) => (
          <Box
            key={line.line_id}
            sx={{
              bgcolor: "background.default",
              px: 1.5,
              py: 0.5,
              borderRadius: 1,
              display: "flex",
              alignItems: "center",
              gap: 0.5,
            }}
          >
            <IconButton size="small" disabled={i === 0} onClick={() => handleMove(i, -1)}>
              <ArrowUpwardIcon fontSize="small" />
            </IconButton>
            <IconButton size="small" disabled={i === lines.length - 1} onClick={() => handleMove(i, 1)}>
              <ArrowDownwardIcon fontSize="small" />
            </IconButton>
            <Typography variant="body2" sx={{ flex: 1 }}>Line {line.line_number}</Typography>
            <IconButton size="small" sx={{ p: 0.25, color: "error.main" }} onClick={() => handleRemove(line)}>
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
