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
  startTime,
  endTime,
  onSignOff,
  canSignOff,
}) {
  const formatTime = (t) => (t ? new Date(t).toLocaleString() : "-");
  const duration =
    startTime && endTime
      ? Math.round((new Date(endTime) - new Date(startTime)) / 60000)
      : null;

  const [subTasks, setSubTasks] = useState([]);
  const [editing, setEditing] = useState(false);
  const [newSubTaskName, setNewSubTaskName] = useState("");
  const [initials, setInitials] = useState("");
  const [localEndTime, setLocalEndTime] = useState(null);
  const [comments, setComments] = useState("");

  const isCompleted = execution?.status === "completed";

  const loadSubTasks = async () => {
    if (!execution?.execution_id) return;
    try {
      const res = await apiService.subTasks.getByExecution(
        execution.execution_id,
      );
      setSubTasks(res.data.data);
    } catch (err) {
      console.error("TaskWindow loadSubTasks error:", err);
    }
  };

  useEffect(() => {
    if (!open || !execution?.execution_id) return;
    let cancelled = false;

    async function load() {
      try {
        const res = await apiService.subTasks.getByExecution(
          execution.execution_id,
        );
        if (!cancelled) {
          setSubTasks(res.data.data);
          setInitials("");
          setLocalEndTime(endTime ? dayjs(endTime) : null);
          setComments(execution?.signed_comments || "");
        }
      } catch (err) {
        console.error("TaskWindow load error:", err);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [open, execution?.execution_id, endTime]);

  const handleToggleSubTask = async (st) => {
    if (isCompleted) return;
    const nowCompleted = st.is_completed ? 0 : 1;
    await apiService.subTasks.update(st.sub_task_id, {
      is_completed: nowCompleted,
      completed_by: nowCompleted ? "✓" : null,
      completed_at: nowCompleted ? new Date().toISOString() : null,
    });
    await loadSubTasks();
  };

  const handleAddSubTask = async () => {
    const name = newSubTaskName.trim();
    if (!name || !execution?.execution_id) return;
    await apiService.subTasks.create({
      execution_id: execution.execution_id,
      sub_task_name: name,
      sub_task_order: subTasks.length + 1,
    });
    setNewSubTaskName("");
    await loadSubTasks();
  };

  const handleDeleteSubTask = async (subTaskId) => {
    await apiService.subTasks.delete(subTaskId);
    await loadSubTasks();
  };

  const handleFinalSignOff = async () => {
    const trimmed = (initials || "").trim();
    if (!trimmed || trimmed.length < 2 || trimmed.length > 3) {
      alert("Please enter 2 or 3 character initials.");
      return;
    }
    if (comments.trim() && execution?.execution_id) {
      await apiService.stepExecutions.update(execution.execution_id, {
        signed_comments: comments.trim(),
      });
    }
    const endVal = localEndTime
      ? dayjs.isDayjs(localEndTime)
        ? localEndTime.toDate().toISOString()
        : new Date(localEndTime).toISOString()
      : null;
    onSignOff(step.step_id, trimmed, endVal);
    onClose();
  };

  if (!step) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
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
        {/* Info section */}
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 1,
            mb: 2,
            p: 1.5,
            bgcolor: "background.default",
            borderRadius: 1,
          }}
        >
          <Typography variant="body2">
            <strong>Status:</strong> {execution?.status || "not_started"}
          </Typography>
          <Typography variant="body2">
            <strong>Duration:</strong>{" "}
            {duration != null ? `${duration} min` : "-"}
          </Typography>
          <Typography variant="body2">
            <strong>Start:</strong> {formatTime(startTime)}
          </Typography>
          <Typography variant="body2">
            <strong>End:</strong> {formatTime(endTime)}
          </Typography>
        </Box>

        <Divider sx={{ mb: 2 }} />

        {/* Sub-tasks list */}
        {subTasks.length === 0 && !editing && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            No sub-tasks. Click the edit icon to add some.
          </Typography>
        )}

        {subTasks.map((st) => (
          <Box
            key={st.sub_task_id}
            sx={{ display: "flex", alignItems: "center", py: 0.5 }}
          >
            <Checkbox
              checked={!!st.is_completed}
              onChange={() => handleToggleSubTask(st)}
              disabled={isCompleted || !canSignOff}
              size="small"
            />
            <Typography
              variant="body2"
              sx={{
                flex: 1,
                textDecoration: st.is_completed ? "line-through" : "none",
                color: st.is_completed ? "text.secondary" : "text.primary",
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
        ))}

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
            {execution.signed_comments && (
              <Typography variant="body2" sx={{ mt: 1, fontStyle: "italic" }}>
                "{execution.signed_comments}"
              </Typography>
            )}
          </Box>
        ) : (
          <Box>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Final Sign Off
            </Typography>
            <Box
              sx={{
                display: "flex",
                gap: 2,
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              <DateTimePicker
                label="End Time"
                slotProps={{ textField: { size: "small" } }}
                value={localEndTime}
                onChange={setLocalEndTime}
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
                  htmlInput: {
                    maxLength: 3,
                    style: { width: 50, textAlign: "center" },
                  },
                }}
                disabled={!canSignOff}
              />
              <Button
                variant="contained"
                onClick={handleFinalSignOff}
                disabled={!canSignOff}
              >
                Sign Off
              </Button>
            </Box>
            <TextField
              size="small"
              label="Comments"
              multiline
              minRows={2}
              fullWidth
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              disabled={!canSignOff}
              sx={{ mt: 2 }}
            />
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}
