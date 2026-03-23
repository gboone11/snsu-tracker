import { useState, useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
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
import TextField from "@mui/material/TextField";
import { apiService } from "../services/api";

function LineDetailPage() {
  const { lineId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const groupId = searchParams.get("group");
  const [line, setLine] = useState(null);
  const [run, setRun] = useState(null);
  const [steps, setSteps] = useState([]);
  const [executions, setExecutions] = useState([]);
  const [timeInputs, setTimeInputs] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const lineRes = await apiService.lines.getById(lineId);
        setLine(lineRes.data.data);

        const runsRes = await apiService.runs.getAll();
        let lineRun = runsRes.data.data.find((r) => r.line_id === parseInt(lineId));

        if (!lineRun) {
          console.log("No run found, creating one...");
          const newRunRes = await apiService.runs.create({
            line_id: parseInt(lineId),
            work_order_end_time: new Date().toISOString(),
            target_ready_time: new Date().toISOString(),
            status: "in_progress",
          });
          lineRun = newRunRes.data.data;
          console.log("Created run:", lineRun);
        }

        setRun(lineRun);
        const stepsRes = await apiService.processSteps.getByGroup(lineRes.data.data.line_group_id);
        setSteps(stepsRes.data.data);

        const execRes = await apiService.stepExecutions.getByRun(lineRun.run_id);
        setExecutions(execRes.data.data);

        // Auto-create execution for first step if not exists
        if (stepsRes.data.data.length > 0 && execRes.data.data.length === 0) {
          await apiService.stepExecutions.create({
            run_id: lineRun.run_id,
            step_id: stepsRes.data.data[0].step_id,
            status: "in_progress",
          });
          const updatedExecRes = await apiService.stepExecutions.getByRun(lineRun.run_id);
          setExecutions(updatedExecRes.data.data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, [lineId]);

  const getExecution = (stepId) => {
    return executions.find((e) => e.step_id === stepId) || {};
  };

  const handleTimeChange = async (stepId, field, value) => {
    if (!value) return;
    if (!run) {
      console.log("No run in handleTimeChange");
      return;
    }
    const date = new Date(value);
    if (isNaN(date.getTime())) {
      alert("Invalid date format. Use MM/DD/YYYY HH:MM AM/PM");
      return;
    }

    const execution = getExecution(stepId);
    const isoValue = date.toISOString();

    if (!execution.execution_id) {
      const newExec = await apiService.stepExecutions.create({
        run_id: run.run_id,
        step_id: stepId,
        status: "in_progress",
      });
      await apiService.stepExecutions.update(newExec.data.data.execution_id, { [field]: isoValue });
    } else {
      await apiService.stepExecutions.update(execution.execution_id, { [field]: isoValue });
    }
    const execRes = await apiService.stepExecutions.getByRun(run.run_id);
    setExecutions(execRes.data.data);
  };

  const handleSignOff = async (stepId) => {
    console.log("=== SIGN OFF START ===", { stepId, run });
    if (!run) {
      console.log("❌ No run found, exiting");
      return;
    }

    const execution = getExecution(stepId);
    console.log("Current execution:", execution);

    const startInput = timeInputs[`${stepId}-start_time`];
    const endInput = timeInputs[`${stepId}-end_time`];
    console.log("Time inputs:", { startInput, endInput });

    let startTime = execution.start_time;
    let endTime = execution.end_time;

    if (startInput) {
      const date = new Date(startInput);
      if (!isNaN(date.getTime())) {
        startTime = date.toISOString();
        console.log("✓ Converted start time:", startTime);
      }
    }
    if (endInput) {
      const date = new Date(endInput);
      if (!isNaN(date.getTime())) {
        endTime = date.toISOString();
        console.log("✓ Converted end time:", endTime);
      }
    }

    let duration = null;
    if (startTime && endTime) {
      duration = Math.round((new Date(endTime) - new Date(startTime)) / 60000);
      console.log("✓ Calculated duration:", duration);
    }

    try {
      if (!execution.execution_id) {
        console.log("Creating new execution...");
        await apiService.stepExecutions.create({
          run_id: run.run_id,
          step_id: stepId,
          status: "completed",
          start_time: startTime,
          end_time: endTime,
          duration_minutes: duration,
          signed_by: "User",
          signed_at: new Date().toISOString(),
        });
        console.log("✓ Created execution");
      } else {
        console.log("Updating existing execution:", execution.execution_id);
        await apiService.stepExecutions.update(execution.execution_id, {
          status: "completed",
          start_time: startTime,
          end_time: endTime,
          duration_minutes: duration,
          signed_by: "User",
          signed_at: new Date().toISOString(),
        });
        console.log("✓ Updated execution");
      }

      const currentStepIndex = steps.findIndex((s) => s.step_id === stepId);
      console.log("Current step index:", currentStepIndex, "Total steps:", steps.length);

      if (currentStepIndex >= 0 && currentStepIndex < steps.length - 1) {
        const nextStep = steps[currentStepIndex + 1];
        console.log("Next step:", nextStep);
        const nextExecution = getExecution(nextStep.step_id);
        console.log("Next execution:", nextExecution);

        if (!nextExecution.execution_id) {
          console.log("Creating next step execution...");
          await apiService.stepExecutions.create({
            run_id: run.run_id,
            step_id: nextStep.step_id,
            status: "in_progress",
            start_time: endTime,
          });
          console.log("✓ Created next step execution");
        } else if (nextExecution.status !== "completed") {
          console.log("Updating next step to in_progress...");
          await apiService.stepExecutions.update(nextExecution.execution_id, {
            status: "in_progress",
            start_time: endTime,
          });
          console.log("✓ Updated next step");
        }
      }

      console.log("Refreshing executions...");
      const execRes = await apiService.stepExecutions.getByRun(run.run_id);
      console.log("New executions:", execRes.data.data);
      setExecutions(execRes.data.data);
      console.log("=== SIGN OFF COMPLETE ===");
    } catch (error) {
      console.error("❌ Error in handleSignOff:", error);
    }
  };

  const calculateDuration = (startTime, endTime) => {
    if (!startTime || !endTime) return "-";
    const start = new Date(startTime);
    const end = new Date(endTime);
    const diff = Math.round((end - start) / 60000);
    return diff;
  };

  const handleResetTasks = async () => {
    if (!window.confirm("Reset all tasks? This will clear all progress.")) return;
    try {
      for (const exec of executions) {
        await apiService.stepExecutions.delete(exec.execution_id);
      }
      if (steps.length > 0) {
        await apiService.stepExecutions.create({
          run_id: run.run_id,
          step_id: steps[0].step_id,
          status: "in_progress",
        });
      }
      const execRes = await apiService.stepExecutions.getByRun(run.run_id);
      setExecutions(execRes.data.data);
      setTimeInputs({});
    } catch (error) {
      alert("Error resetting tasks: " + error.message);
    }
  };

  if (!line) return <Box sx={{ p: 3 }}>Loading...</Box>;

  return (
    <Box sx={{ p: 3 }}>
      <Button
        variant="contained"
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate(groupId ? `/?group=${groupId}` : "/")}
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
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Step</TableCell>
              <TableCell>Team</TableCell>
              <TableCell>Task</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Start Time</TableCell>
              <TableCell>End Time</TableCell>
              <TableCell>Duration (min)</TableCell>
              <TableCell>Sign Off</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {steps.map((step, idx) => {
              const execution = getExecution(step.step_id);
              const duration = calculateDuration(execution.start_time, execution.end_time);
              const status = execution.status || (idx === 0 ? "in_progress" : "not_started");
              const rowColor =
                status === "completed"
                  ? "#c8e6c9"
                  : status === "in_progress"
                    ? "#fff9c4"
                    : "inherit";
              const isCompleted = status === "completed";
              return (
                <TableRow key={step.step_id} sx={{ backgroundColor: rowColor }}>
                  <TableCell>{idx + 1}</TableCell>
                  <TableCell>{step.team_name}</TableCell>
                  <TableCell>{step.task_name}</TableCell>
                  <TableCell>
                    {execution.status || (idx === 0 ? "in_progress" : "not_started")}
                  </TableCell>
                  <TableCell>
                    <TextField
                      size="small"
                      placeholder="MM/DD/YYYY HH:MM AM/PM"
                      value={
                        timeInputs[`${step.step_id}-start_time`] ??
                        (execution.start_time
                          ? new Date(execution.start_time).toLocaleString()
                          : "")
                      }
                      onChange={(e) =>
                        setTimeInputs({
                          ...timeInputs,
                          [`${step.step_id}-start_time`]: e.target.value,
                        })
                      }
                      onBlur={(e) => handleTimeChange(step.step_id, "start_time", e.target.value)}
                      disabled={isCompleted}
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      size="small"
                      placeholder="MM/DD/YYYY HH:MM AM/PM"
                      value={
                        timeInputs[`${step.step_id}-end_time`] ??
                        (execution.end_time ? new Date(execution.end_time).toLocaleString() : "")
                      }
                      onChange={(e) =>
                        setTimeInputs({
                          ...timeInputs,
                          [`${step.step_id}-end_time`]: e.target.value,
                        })
                      }
                      onBlur={(e) => handleTimeChange(step.step_id, "end_time", e.target.value)}
                      disabled={isCompleted}
                    />
                  </TableCell>
                  <TableCell>{duration}</TableCell>
                  <TableCell>
                    {execution.signed_by ? (
                      <Typography color="success.main">✓ {execution.signed_by}</Typography>
                    ) : (
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => handleSignOff(step.step_id)}
                      >
                        Sign Off
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default LineDetailPage;
