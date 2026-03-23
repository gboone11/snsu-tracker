import { useState, useEffect } from "react";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { apiService } from "../services/api";

function ProcessStepsConfigPanel() {
  const [steps, setSteps] = useState([]);
  const [newTeam, setNewTeam] = useState("");
  const [newTask, setNewTask] = useState("");

  useEffect(() => {
    apiService.processSteps.getAll()
      .then((res) => setSteps(res.data.data))
      .catch((err) => console.error("Error fetching steps:", err));
  }, []);

  const handleAdd = async () => {
    const team = newTeam.trim();
    const task = newTask.trim();
    if (!team || !task) return;
    try {
      await apiService.processSteps.create({
        step_order: steps.length + 1,
        team_name: team,
        task_name: task,
      });
      const res = await apiService.processSteps.getAll();
      setSteps(res.data.data);
      setNewTeam("");
      setNewTask("");
    } catch (error) {
      alert("Error adding step: " + error.message);
    }
  };

  const handleRemove = async (step) => {
    if (!window.confirm(`Remove step "${step.team_name} — ${step.task_name}"?`)) return;
    try {
      await apiService.processSteps.delete(step.step_id);
      setSteps(steps.filter((s) => s.step_id !== step.step_id));
    } catch (error) {
      alert("Error removing step: " + error.message);
    }
  };

  return (
    <Paper sx={{ p: 2.5, mb: 3, bgcolor: "background.paper" }}>
      <Typography variant="h6" sx={{ mb: 2, color: "primary.main" }}>
        Process Steps
      </Typography>
      <Box sx={{ display: "flex", gap: 1, mb: 2 }}>
        <TextField
          size="small"
          placeholder="Step owner (e.g., Ops)"
          value={newTeam}
          onChange={(e) => setNewTeam(e.target.value)}
          sx={{ width: 200 }}
        />
        <TextField
          size="small"
          placeholder="Step description"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleAdd()}
          sx={{ width: 250 }}
        />
        <Button variant="contained" onClick={handleAdd}>
          + Add Step
        </Button>
      </Box>
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
        {steps.map((step) => (
          <Box
            key={step.step_id}
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
            <Typography variant="body2">{step.team_name} — {step.task_name}</Typography>
            <IconButton
              size="small"
              sx={{ p: 0.25, color: "error.main" }}
              onClick={() => handleRemove(step)}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>
        ))}
        {steps.length === 0 && (
          <Typography variant="body2" sx={{ color: "text.secondary", fontStyle: "italic" }}>
            No process steps configured
          </Typography>
        )}
      </Box>
    </Paper>
  );
}

export default ProcessStepsConfigPanel;
