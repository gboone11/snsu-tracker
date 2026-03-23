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
      await resetAllExecutions(res.data.data[0]?.step_id);
    } catch (error) {
      alert("Error adding step: " + error.message);
    }
  };

  const handleRemove = async (step) => {
    if (!window.confirm(`Remove step "${step.team_name} — ${step.task_name}"?`)) return;
    try {
      await apiService.processSteps.delete(step.step_id);
      const remaining = steps.filter((s) => s.step_id !== step.step_id);
      setSteps(remaining);
      await resetAllExecutions(remaining[0]?.step_id);
    } catch (error) {
      alert("Error removing step: " + error.message);
    }
  };

  const resetAllExecutions = async (firstStepId) => {
    try {
      const runsRes = await apiService.runs.getAll();
      for (const run of runsRes.data.data) {
        const execRes = await apiService.stepExecutions.getByRun(run.run_id);
        for (const exec of execRes.data.data) {
          await apiService.stepExecutions.delete(exec.execution_id);
        }
        if (firstStepId) {
          await apiService.stepExecutions.create({
            run_id: run.run_id,
            step_id: firstStepId,
            status: "in_progress",
          });
        }
      }
    } catch (error) {
      console.error("Error resetting executions:", error);
    }
  };

  const handleMove = async (index, direction) => {
    const swapIndex = index + direction;
    if (swapIndex < 0 || swapIndex >= steps.length) return;
    const reordered = [...steps];
    [reordered[index], reordered[swapIndex]] = [reordered[swapIndex], reordered[index]];
    setSteps(reordered);
    try {
      await apiService.processSteps.reorder(reordered.map((s) => s.step_id));
      await resetAllExecutions(reordered[0]?.step_id);
    } catch (error) {
      console.error("Error reordering steps:", error);
    }
  };

  return (
    <Paper sx={{ flex: 1, p: 2.5, bgcolor: "background.paper" }}>
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
          onKeyDown={(e) => e.key === "Enter" && handleAdd()}
          sx={{ width: 250 }}
        />
        <Button variant="contained" onClick={handleAdd}>
          + Add Step
        </Button>
      </Box>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
        {steps.map((step, i) => (
          <Box
            key={step.step_id}
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
            <IconButton size="small" disabled={i === steps.length - 1} onClick={() => handleMove(i, 1)}>
              <ArrowDownwardIcon fontSize="small" />
            </IconButton>
            <Typography variant="body2" sx={{ flex: 1 }}>{step.team_name} — {step.task_name}</Typography>
            <IconButton size="small" sx={{ p: 0.25, color: "error.main" }} onClick={() => handleRemove(step)}>
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
