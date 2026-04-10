import { useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { apiService } from "../services/api";

export default function WarehouseTaskWindow({ open, onClose, step, execution, run, onComplete }) {
  const [initials, setInitials] = useState("");
  const [prevOpen, setPrevOpen] = useState(false);
  const isCompleted = execution?.status === "completed";

  if (open && !prevOpen) {
    setInitials("");
  }
  if (open !== prevOpen) {
    setPrevOpen(open);
  }

  const handleComplete = async () => {
    const trimmed = (initials || "").trim();
    if (!trimmed || trimmed.length < 2 || trimmed.length > 3) {
      alert("Please enter 2 or 3 character initials.");
      return;
    }

    try {
      const now = new Date().toISOString();
      if (!execution?.execution_id) {
        const res = await apiService.stepExecutions.create({
          run_id: run.run_id,
          step_id: step.step_id,
          status: "completed",
        });
        await apiService.stepExecutions.update(res.data.data.execution_id, {
          status: "completed",
          signed_by: trimmed,
          signed_at: now,
        });
      } else {
        await apiService.stepExecutions.update(execution.execution_id, {
          status: "completed",
          signed_by: trimmed,
          signed_at: now,
        });
      }
      onComplete();
      onClose();
    } catch (err) {
      console.error("WarehouseTaskWindow error:", err);
    }
  };

  const handleUncomplete = async () => {
    if (!execution?.execution_id) return;
    try {
      await apiService.stepExecutions.update(execution.execution_id, {
        status: "in_progress",
      });
      onComplete();
      onClose();
    } catch (err) {
      console.error("WarehouseTaskWindow uncomplete error:", err);
    }
  };

  if (!step) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="h6">{step.task_name}</Typography>
        <IconButton size="small" onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        {isCompleted ? (
          <Box sx={{ textAlign: "center", py: 2 }}>
            <Typography color="success.main" variant="h6">
              ✓ Delivered — signed by {execution.signed_by}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {execution.signed_at ? new Date(execution.signed_at).toLocaleString() : ""}
            </Typography>
            <Button
              variant="outlined"
              color="warning"
              size="small"
              sx={{ mt: 2 }}
              onClick={handleUncomplete}
            >
              Undo
            </Button>
          </Box>
        ) : (
          <Box sx={{ display: "flex", gap: 2, alignItems: "center", py: 2 }}>
            <TextField
              size="small"
              label="Initials"
              value={initials}
              onChange={(e) => setInitials(e.target.value.slice(0, 3).toUpperCase())}
              slotProps={{
                htmlInput: {
                  maxLength: 3,
                  style: { width: 50, textAlign: "center" },
                },
              }}
            />
            <Button variant="contained" color="success" onClick={handleComplete}>
              Mark Delivered
            </Button>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}
