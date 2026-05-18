import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { apiService } from "../services/api";
import TaskWindow from "./TaskWindow";
import WarehouseTaskWindow from "./WarehouseTaskWindow";

function LineDetailPage() {
  const { lineId } = useParams();
  const navigate = useNavigate();
  const [line, setLine] = useState(null);
  const [run, setRun] = useState(null);
  const [steps, setSteps] = useState([]);
  const [executions, setExecutions] = useState([]);
  const [taskWindowOpen, setTaskWindowOpen] = useState(false);
  const [selectedStep, setSelectedStep] = useState(null);
  const [warehouseWindowOpen, setWarehouseWindowOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const lineRes = await apiService.lines.getById(lineId);
        if (cancelled) return;

        const runsRes = await apiService.runs.getAll();
        let lineRun = runsRes.data.data.find((r) => r.line_id === parseInt(lineId));

        if (!lineRun) {
          const newRunRes = await apiService.runs.create({
            line_id: parseInt(lineId),
            status: "in_progress",
          });
          lineRun = newRunRes.data.data;
        }

        const stepsRes = await apiService.processSteps.getAll();
        const execRes = await apiService.stepExecutions.getByRun(lineRun.run_id);

        let execData = execRes.data.data;
        const firstRegularStep = stepsRes.data.data.find((s) => !s.is_default);
        if (firstRegularStep && execData.length === 0) {
          await apiService.stepExecutions.create({
            run_id: lineRun.run_id,
            step_id: firstRegularStep.step_id,
            status: "in_progress",
          });
          const updatedExecRes = await apiService.stepExecutions.getByRun(lineRun.run_id);
          execData = updatedExecRes.data.data;
        }

        if (!cancelled) {
          setLine(lineRes.data.data);
          setRun(lineRun);
          setSteps(stepsRes.data.data);
          setExecutions(execData);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [lineId]);

  const refreshExecutions = async (runId) => {
    const execRes = await apiService.stepExecutions.getByRun(runId);
    setExecutions(execRes.data.data);
  };

  const defaultStep = steps.find((s) => s.is_default);
  const regularSteps = steps.filter((s) => !s.is_default);

  const getExecution = (stepId) => executions.find((e) => e.step_id === stepId) || {};

  const getStartTime = (stepId) => {
    const idx = regularSteps.findIndex((s) => s.step_id === stepId);
    if (idx <= 0) return run?.work_order_end_time || null;
    const prevExec = getExecution(regularSteps[idx - 1].step_id);
    return prevExec.end_time || null;
  };

  const calculateDuration = (startTime, endTime) => {
    if (!startTime || !endTime) return "-";
    return Math.round((new Date(endTime) - new Date(startTime)) / 60000);
  };

  const handleOpenTask = (step) => {
    if (step.is_default) {
      setSelectedStep(step);
      setWarehouseWindowOpen(true);
    } else {
      setSelectedStep(step);
      setTaskWindowOpen(true);
    }
  };

  const handleSignOff = async (stepId, initials, endTimeIso) => {
    if (!run) return;
    const execution = getExecution(stepId);

    let startTime = getStartTime(stepId);
    let endTime = endTimeIso || execution.end_time;

    let duration = null;
    if (startTime && endTime) {
      duration = Math.round((new Date(endTime) - new Date(startTime)) / 60000);
    }

    if (!duration || duration < 0) {
      alert("End time must be after start time.");
      return;
    }

    try {
      if (!execution.execution_id) {
        await apiService.stepExecutions.create({
          run_id: run.run_id,
          step_id: stepId,
          status: "completed",
        });
        const execRes = await apiService.stepExecutions.getByRun(run.run_id);
        const newExec = execRes.data.data.find((e) => e.step_id === stepId);
        if (newExec) {
          await apiService.stepExecutions.update(newExec.execution_id, {
            status: "completed",
            start_time: startTime,
            end_time: endTime,
            duration_minutes: duration,
            signed_by: initials,
            signed_at: new Date().toISOString(),
          });
        }
      } else {
        await apiService.stepExecutions.update(execution.execution_id, {
          status: "completed",
          start_time: startTime,
          end_time: endTime,
          duration_minutes: duration,
          signed_by: initials,
          signed_at: new Date().toISOString(),
        });
      }

      const currentStepIndex = regularSteps.findIndex((s) => s.step_id === stepId);
      if (currentStepIndex >= 0 && currentStepIndex < regularSteps.length - 1) {
        const nextStep = regularSteps[currentStepIndex + 1];
        const nextExecution = getExecution(nextStep.step_id);
        if (!nextExecution.execution_id) {
          await apiService.stepExecutions.create({
            run_id: run.run_id,
            step_id: nextStep.step_id,
            status: "in_progress",
          });
        } else if (nextExecution.status !== "completed") {
          await apiService.stepExecutions.update(nextExecution.execution_id, {
            status: "in_progress",
            start_time: endTime,
          });
        }
      }

      await refreshExecutions(run.run_id);
    } catch (error) {
      console.error("Error in handleSignOff:", error);
    }
  };

  const handleResetTasks = async () => {
    if (!window.confirm("Reset all tasks? This will clear all progress.")) return;
    try {
      for (const exec of executions) {
        await apiService.stepExecutions.delete(exec.execution_id);
      }
      if (regularSteps.length > 0) {
        await apiService.stepExecutions.create({
          run_id: run.run_id,
          step_id: regularSteps[0].step_id,
          status: "in_progress",
        });
      }
      await refreshExecutions(run.run_id);
    } catch (error) {
      alert("Error resetting tasks: " + error.message);
    }
  };

  if (!line) return <Box sx={{ p: 3 }}>Loading...</Box>;

  const selectedExecution = selectedStep ? getExecution(selectedStep.step_id) : {};
  const selectedIdx = selectedStep
    ? regularSteps.findIndex((s) => s.step_id === selectedStep.step_id)
    : -1;
  const selectedIsCompleted = selectedExecution?.status === "completed";
  const selectedPrevCompleted =
    selectedIdx === 0 ||
    getExecution(regularSteps[selectedIdx - 1]?.step_id)?.status === "completed";
  const selectedCanSignOff = !selectedIsCompleted && selectedPrevCompleted;

  return (
    <Box sx={{ p: 3 }}>
      <Button
        variant="contained"
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate("/")}
        sx={{ mb: 3 }}
      >
        Back
      </Button>
      <Button variant="outlined" color="warning" onClick={handleResetTasks} sx={{ mb: 3, ml: 2 }}>
        Reset Task List
      </Button>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
        Line {line.line_number} - SNSU Process
      </Typography>
      <Paper sx={{ p: 2, mb: 3, display: "flex", gap: 4 }}>
        <Typography>
          <strong>WO Ended:</strong>{" "}
          {run?.work_order_end_time ? new Date(run.work_order_end_time).toLocaleString() : "-"}
        </Typography>
        <Typography>
          <strong>Target Start:</strong>{" "}
          {run?.target_ready_time ? new Date(run.target_ready_time).toLocaleString() : "-"}
        </Typography>
      </Paper>
      {defaultStep &&
        (() => {
          const whExec = getExecution(defaultStep.step_id);
          const whCompleted = whExec?.status === "completed";
          return (
            <Paper
              sx={{
                p: 2,
                mb: 3,
                display: "flex",
                alignItems: "center",
                gap: 2,
                cursor: "pointer",
                "&:hover": { filter: "brightness(0.97)" },
              }}
              onClick={() => handleOpenTask(defaultStep)}
            >
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  borderRadius: "50%",
                  bgcolor: whCompleted ? "#4caf50" : "transparent",
                  border: "2px solid #4caf50",
                }}
              />
              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                {defaultStep.task_name}
              </Typography>
              {whCompleted && (
                <Typography variant="body2" color="text.secondary">
                  ✓ {whExec.signed_by}
                </Typography>
              )}
            </Paper>
          );
        })()}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Step</TableCell>
              <TableCell>Team</TableCell>
              <TableCell>Task</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Duration (min)</TableCell>
              <TableCell>Signed By</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {regularSteps.map((step, idx) => {
              const execution = getExecution(step.step_id);
              const startTime = getStartTime(step.step_id);
              const duration = calculateDuration(startTime, execution.end_time);
              const status = execution.status || (idx === 0 ? "in_progress" : "not_started");
              const rowColor =
                status === "completed"
                  ? "#c8e6c9"
                  : status === "in_progress"
                    ? "#fff9c4"
                    : "inherit";
              return (
                <TableRow
                  key={step.step_id}
                  sx={{
                    backgroundColor: rowColor,
                    cursor: "pointer",
                    "&:hover": { filter: "brightness(0.95)" },
                  }}
                  onClick={() => handleOpenTask(step)}
                >
                  <TableCell>{idx + 1}</TableCell>
                  <TableCell>{step.team_name}</TableCell>
                  <TableCell>{step.task_name}</TableCell>
                  <TableCell>{status}</TableCell>
                  <TableCell>{duration}</TableCell>
                  <TableCell>
                    {execution.signed_by ? (
                      <Typography color="success.main">✓ {execution.signed_by}</Typography>
                    ) : (
                      "-"
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      <TaskWindow
        open={taskWindowOpen}
        onClose={() => {
          setTaskWindowOpen(false);
          if (run) refreshExecutions(run.run_id);
        }}
        step={selectedStep}
        execution={selectedExecution}
        run={run}
        startTime={selectedStep ? getStartTime(selectedStep.step_id) : null}
        endTime={selectedExecution?.end_time || null}
        onSignOff={handleSignOff}
        canSignOff={selectedCanSignOff}
      />

      <WarehouseTaskWindow
        open={warehouseWindowOpen}
        onClose={() => {
          setWarehouseWindowOpen(false);
          if (run) refreshExecutions(run.run_id);
        }}
        step={selectedStep}
        execution={selectedExecution}
        run={run}
        onComplete={() => run && refreshExecutions(run.run_id)}
      />
    </Box>
  );
}

export default LineDetailPage;
