import { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Checkbox from "@mui/material/Checkbox";
import IconButton from "@mui/material/IconButton";
import Divider from "@mui/material/Divider";
import CloseIcon from "@mui/icons-material/Close";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import dayjs from "dayjs";
import { apiService } from "../services/api";

export default function TaskWindow({
  open,
  onClose,
  step,
  execution,
  onSignOff,
  canSignOff,
}) {
  const [subTasks, setSubTasks] = useState([]);
  const [subTaskExecs, setSubTaskExecs] = useState([]);
  const [editing, setEditing] = useState(false);
  const [newSubTaskName, setNewSubTaskName] = useState("");
  const [initials, setInitials] = useState("");
  const [endTime, setEndTime] = useState(null);

  const isCompleted = execution?.status === "completed";

  const loadSubTaskData = async () => {
    if (!step) return;
    try {
      const stRes = await apiService.subTasks.getByStep(step.step_id);
      setSubTasks(stRes.data.data);

      if (execution?.execution_id) {
        const steRes = await apiService.subTaskExecutions.getByExecution(
          execution.execution_id,
        );
        const existing = steRes.data.data;

        for (const st of stRes.data.data) {
          if (!existing.find((e) => e.sub_task_id === st.sub_task_id)) {
            await apiService.subTaskExecutions.create({
              execution_id: execution.execution_id,
              sub_task_id: st.sub_task_id,
            });
          }
        }

        const refreshed = await apiService.subTaskExecutions.getByExecution(
          execution.execution_id,
        );
        setSubTaskExecs(refreshed.data.data);
      }
    } catch (err) {
      console.error("TaskWindow loadData error:", err);
    }
  };

  useEffect(() => {
    if (!open || !step) return;
    let cancelled = false;

    async function load() {
      try {
        const stRes = await apiService.subTasks.getByStep(step.step_id);
        if (cancelled) return;

        const subTasksData = stRes.data.data;

        let subTaskExecsData = [];
        if (execution?.execution_id) {
          const steRes = await apiService.subTaskExecutions.getByExecution(
            execution.execution_id,
          );
          const existing = steRes.data.data;

          for (const st of subTasksData) {
            if (!existing.find((e) => e.sub_task_id === st.sub_task_id)) {
              await apiService.subTaskExecutions.create({
                execution_id: execution.execution_id,
                sub_task_id: st.sub_task_id,
              });
            }
          }

          const refreshed = await apiService.subTaskExecutions.getByExecution(
            execution.execution_id,
          );
          subTaskExecsData = refreshed.data.data;
        }

        if (!cancelled) {
          setSubTasks(subTasksData);
          setSubTaskExecs(subTaskExecsData);
          setInitials("");
          setEndTime(execution?.end_time ? dayjs(execution.end_time) : null);
        }
      } catch (err) {
        console.error("TaskWindow load error:", err);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [open, step, execution?.execution_id, execution?.end_time]);

  const handleToggleSubTask = async (ste) => {
    if (isCompleted) return;
    const nowCompleted = ste.is_completed ? 0 : 1;
    await apiService.subTaskExecutions.update(ste.sub_task_execution_id, {
      is_completed: nowCompleted,
      completed_by: nowCompleted ? "✓" : null,
      completed_at: nowCompleted ? new Date().toISOString() : null,
    });
    const refreshed = await apiService.subTaskExecutions.getByExecution(
      execution.execution_id,
    );
    setSubTaskExecs(refreshed.data.data);
  };

  const handleAddSubTask = async () => {
    const name = newSubTaskName.trim();
    if (!name) return;
    await apiService.subTasks.create({
      step_id: step.step_id,
      sub_task_name: name,
      sub_task_order: subTasks.length + 1,
    });
    setNewSubTaskName("");
    await loadSubTaskData();
  };

  const handleDeleteSubTask = async (subTaskId) => {
    await apiService.subTasks.delete(subTaskId);
    await loadSubTaskData();
  };

  const allSubTasksDone =
    subTasks.length === 0 ||
    (subTaskExecs.length >= subTasks.length &&
      subTasks.every((st) => {
        const ste = subTaskExecs.find((e) => e.sub_task_id === st.sub_task_id);
        return ste?.is_completed;
      }));

  const handleFinalSignOff = () => {
    const trimmed = (initials || "").trim();
    if (!trimmed || trimmed.length < 2 || trimmed.length > 3) {
      alert("Please enter 2 or 3 character initials.");
      return;
    }
    const endVal = endTime
      ? dayjs.isDayjs(endTime)
        ? endTime.toDate().toISOString()
        : new Date(endTime).toISOString()
      : null;
    onSignOff(step.step_id, trimmed, endVal);
    onClose();
  };

  if (!step) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Box>
          <Typography variant="h6">{step.task_name}</Typography>
          <Typography variant="body2" color="text.secondary">
            {step.team_name}
          </Typography>
        </Box>
        <Box>
          {!isCompleted && (
            <IconButton size="small" onClick={() => setEditing(!editing)}>
              <EditIcon fontSize="small" />
            </IconButton>
          )}
          <IconButton size="small" onClick={onClose}>
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        {/* Sub-tasks list */}
        {subTasks.length === 0 && !editing && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            No sub-tasks configured. Click the edit icon to add some.
          </Typography>
        )}

        {subTasks.map((st) => {
          const ste = subTaskExecs.find((e) => e.sub_task_id === st.sub_task_id);
          return (
            <Box
              key={st.sub_task_id}
              sx={{ display: "flex", alignItems: "center", py: 0.5 }}
            >
              <Checkbox
                checked={!!ste?.is_completed}
                onChange={() => ste && handleToggleSubTask(ste)}
                disabled={isCompleted || !canSignOff}
                size="small"
              />
              <Typography
                variant="body2"
                sx={{
                  flex: 1,
                  textDecoration: ste?.is_completed ? "line-through" : "none",
                  color: ste?.is_completed ? "text.secondary" : "text.primary",
                }}
              >
                {st.sub_task_name}
              </Typography>
              {editing && (
                <IconButton
                  size="small"
                  color="error"
                  onClick={() => handleDeleteSubTask(st.sub_task_id)}
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
              )}
            </Box>
          );
        })}

        {/* Add sub-task (edit mode) */}
        {editing && (
          <Box sx={{ display: "flex", gap: 1, mt: 1, mb: 1 }}>
            <TextField
              size="small"
              placeholder="New sub-task name"
              value={newSubTaskName}
              onChange={(e) => setNewSubTaskName(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAddSubTask()}
              sx={{ flex: 1 }}
            />
            <Button variant="outlined" size="small" onClick={handleAddSubTask}>
              Add
            </Button>
          </Box>
        )}

        {/* Sign-off section */}
        <Divider sx={{ my: 2 }} />

        {isCompleted ? (
          <Box sx={{ textAlign: "center" }}>
            <Typography color="success.main" variant="h6">
              ✓ Signed off by {execution.signed_by}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {execution.signed_at
                ? new Date(execution.signed_at).toLocaleString()
                : ""}
            </Typography>
          </Box>
        ) : (
          <Box>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Final Sign Off
            </Typography>
            <Box sx={{ display: "flex", gap: 2, alignItems: "center", flexWrap: "wrap" }}>
              <DateTimePicker
                label="End Time"
                slotProps={{ textField: { size: "small" } }}
                value={endTime}
                onChange={setEndTime}
                disabled={!canSignOff}
              />
              <TextField
                size="small"
                label="Initials"
                value={initials}
                onChange={(e) =>
                  setInitials(e.target.value.slice(0, 3).toUpperCase())
                }
                slotProps={{
                  htmlInput: { maxLength: 3, style: { width: 50, textAlign: "center" } },
                }}
                disabled={!canSignOff}
              />
              <Button
                variant="contained"
                onClick={handleFinalSignOff}
                disabled={!canSignOff || !allSubTasksDone}
              >
                Sign Off
              </Button>
            </Box>
            {!allSubTasksDone && subTasks.length > 0 && (
              <Typography variant="caption" color="error" sx={{ mt: 1, display: "block" }}>
                Complete all sub-tasks before signing off.
              </Typography>
            )}
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}
