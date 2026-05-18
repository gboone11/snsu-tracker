import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Paper from "@mui/material/Paper";
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

function LinesStatusBoard() {
  const navigate = useNavigate();
  const [lines, setLines] = useState([]);
  const [runs, setRuns] = useState([]);
  const [steps, setSteps] = useState([]);
  const [executions, setExecutions] = useState([]);
  const [taskWindowOpen, setTaskWindowOpen] = useState(false);
  const [selectedStep, setSelectedStep] = useState(null);
  const [selectedRun, setSelectedRun] = useState(null);
  const [warehouseWindowOpen, setWarehouseWindowOpen] = useState(false);
  const [warehouseStep, setWarehouseStep] = useState(null);
  const [warehouseRun, setWarehouseRun] = useState(null);
  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [linesRes, runsRes, stepsRes] = await Promise.all([
          apiService.lines.getAll(),
          apiService.runs.getAll(),
          apiService.processSteps.getAll(),
        ]);
        if (cancelled) return;

        const allLines = linesRes.data.data;
        const stepsData = stepsRes.data.data;

        const allRuns = [...runsRes.data.data];
        for (const line of allLines) {
          if (!allRuns.find((r) => r.line_id === line.line_id)) {
            const newRunRes = await apiService.runs.create({
              line_id: line.line_id,
              status: "in_progress",
            });
            allRuns.push(newRunRes.data.data);
          }
        }

        const firstRegularStep = stepsData.find((s) => !s.is_default);
        const allExecutions = [];
        for (const run of allRuns) {
          const execRes = await apiService.stepExecutions.getByRun(run.run_id);
          if (execRes.data.data.length === 0 && firstRegularStep) {
            await apiService.stepExecutions.create({
              run_id: run.run_id,
              step_id: firstRegularStep.step_id,
              status: "in_progress",
            });
            const refetch = await apiService.stepExecutions.getByRun(run.run_id);
            allExecutions.push(...refetch.data.data);
          } else {
            allExecutions.push(...execRes.data.data);
          }
        }

        if (!cancelled) {
          setLines(allLines);
          setSteps(stepsData);
          setRuns(allRuns);
          setExecutions(allExecutions);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const refreshData = async () => {
    try {
      const [linesRes, runsRes, stepsRes] = await Promise.all([
        apiService.lines.getAll(),
        apiService.runs.getAll(),
        apiService.processSteps.getAll(),
      ]);
      const allRuns = runsRes.data.data;
      const allExecutions = [];
      for (const run of allRuns) {
        const execRes = await apiService.stepExecutions.getByRun(run.run_id);
        allExecutions.push(...execRes.data.data);
      }
      setLines(linesRes.data.data);
      setSteps(stepsRes.data.data);
      setRuns(allRuns);
      setExecutions(allExecutions);
    } catch (error) {
      console.error("Error refreshing data:", error);
    }
  };

  const getExecution = (lineId, stepId) => {
    const run = runs.find((r) => r.line_id === lineId);
    if (!run) return {};
    return executions.find((e) => e.run_id === run.run_id && e.step_id === stepId) || {};
  };

  const getStepStatus = (lineId, stepId) => {
    const execution = getExecution(lineId, stepId);
    if (execution.status === "completed") return { color: "#c8e6c9", text: "" };
    if (execution.status === "in_progress") return { color: "#fff9c4", text: "" };
    return { color: "transparent", text: "" };
  };

  const handleCellClick = (lineId, step, e) => {
    e.stopPropagation();
    const run = runs.find((r) => r.line_id === lineId);
    if (!run) return;
    if (step.is_default) {
      setWarehouseStep(step);
      setWarehouseRun(run);
      setWarehouseWindowOpen(true);
    } else {
      setSelectedStep(step);
      setSelectedRun(run);
      setTaskWindowOpen(true);
    }
  };

  const defaultStep = steps.find((s) => s.is_default);
  const regularSteps = steps.filter((s) => !s.is_default);

  const getStartTime = (run, stepId) => {
    const idx = regularSteps.findIndex((s) => s.step_id === stepId);
    if (idx <= 0) return run?.work_order_end_time || null;
    const prevExec = executions.find(
      (e) => e.run_id === run.run_id && e.step_id === regularSteps[idx - 1].step_id,
    );
    return prevExec?.end_time || null;
  };

  const handleSignOff = async (stepId, initials, endTimeIso) => {
    if (!selectedRun) return;
    const execution = getExecution(selectedRun.line_id, stepId);
    const startTime = getStartTime(selectedRun, stepId);
    const endTime = endTimeIso || execution.end_time;

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
        const newExec = await apiService.stepExecutions.create({
          run_id: selectedRun.run_id,
          step_id: stepId,
          status: "completed",
        });
        await apiService.stepExecutions.update(newExec.data.data.execution_id, {
          status: "completed",
          start_time: startTime,
          end_time: endTime,
          duration_minutes: duration,
          signed_by: initials,
          signed_at: new Date().toISOString(),
        });
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
        const nextExec = executions.find(
          (e) => e.run_id === selectedRun.run_id && e.step_id === nextStep.step_id,
        );
        if (!nextExec) {
          await apiService.stepExecutions.create({
            run_id: selectedRun.run_id,
            step_id: nextStep.step_id,
            status: "in_progress",
          });
        }
      }

      await refreshData();
    } catch (error) {
      console.error("Error in handleSignOff:", error);
    }
  };

  const getCanSignOff = () => {
    if (!selectedStep || !selectedRun) return false;
    const exec = getExecution(selectedRun.line_id, selectedStep.step_id);
    if (exec.status === "completed") return false;
    const idx = regularSteps.findIndex((s) => s.step_id === selectedStep.step_id);
    if (idx === 0) return true;
    const prevExec = getExecution(selectedRun.line_id, regularSteps[idx - 1].step_id);
    return prevExec.status === "completed";
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
        Lines Status Board
      </Typography>
      <TableContainer>
        <Table size="small" sx={{ tableLayout: "fixed" }}>
          <TableHead>
            <TableRow>
              <TableCell sx={{ width: 60 }}>Line</TableCell>
              <TableCell sx={{ width: 190 }}>Work Order Ended</TableCell>
              {regularSteps.map((step) => (
                <TableCell key={step.step_id}>
                  {step.team_name}
                  <br />
                  <small>{step.task_name}</small>
                </TableCell>
              ))}
              <TableCell sx={{ width: 190 }}>Target Ready Time</TableCell>
              {defaultStep && (
                <TableCell sx={{ width: 80, textAlign: "center", px: 0.5 }}>
                  {"Materials?"}
                </TableCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {[...lines]
              .sort((a, b) => {
                const runA = runs.find((r) => r.line_id === a.line_id);
                const runB = runs.find((r) => r.line_id === b.line_id);
                const timeA = runA?.target_ready_time
                  ? new Date(runA.target_ready_time).getTime()
                  : Infinity;
                const timeB = runB?.target_ready_time
                  ? new Date(runB.target_ready_time).getTime()
                  : Infinity;
                return timeA - timeB;
              })
              .map((line) => {
                const lineRun = runs.find((r) => r.line_id === line.line_id);
                return (
                  <TableRow key={line.line_id}>
                    <TableCell
                      sx={{
                        cursor: "pointer",
                        "&:hover": { bgcolor: "action.hover" },
                      }}
                      onClick={() => navigate(`/line/${line.line_id}`)}
                    >
                      {line.line_number}
                    </TableCell>
                    <TableCell>
                      {lineRun?.work_order_end_time
                        ? new Date(lineRun.work_order_end_time).toLocaleString()
                        : "-"}
                    </TableCell>
                    {regularSteps.map((step) => {
                      const status = getStepStatus(line.line_id, step.step_id);
                      return (
                        <TableCell
                          key={step.step_id}
                          sx={{
                            bgcolor: status.color,
                            cursor: "pointer",
                            "&:hover": { filter: "brightness(0.9)" },
                          }}
                          onClick={(e) => handleCellClick(line.line_id, step, e)}
                        >
                          {status.text}
                        </TableCell>
                      );
                    })}
                    <TableCell>
                      {lineRun?.target_ready_time
                        ? new Date(lineRun.target_ready_time).toLocaleString()
                        : "-"}
                    </TableCell>
                     {defaultStep &&
                      (() => {
                        const whStatus = getStepStatus(line.line_id, defaultStep.step_id);
                        return (
                          <TableCell
                            sx={{
                              bgcolor: whStatus.color,
                              cursor: "pointer",
                              px: 0.5,
                              "&:hover": { filter: "brightness(0.9)" },
                            }}
                            onClick={(e) => handleCellClick(line.line_id, defaultStep, e)}
                          />
                        );
                      })()}
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
          refreshData();
        }}
        step={selectedStep}
        execution={
          selectedStep && selectedRun ? getExecution(selectedRun.line_id, selectedStep.step_id) : {}
        }
        run={selectedRun}
        startTime={
          selectedStep && selectedRun ? getStartTime(selectedRun, selectedStep.step_id) : null
        }
        endTime={
          selectedStep && selectedRun
            ? getExecution(selectedRun.line_id, selectedStep.step_id)?.end_time || null
            : null
        }
        onSignOff={handleSignOff}
        canSignOff={getCanSignOff()}
      />

      <WarehouseTaskWindow
        open={warehouseWindowOpen}
        onClose={() => {
          setWarehouseWindowOpen(false);
          refreshData();
        }}
        step={warehouseStep}
        execution={
          warehouseStep && warehouseRun
            ? getExecution(warehouseRun.line_id, warehouseStep.step_id)
            : {}
        }
        run={warehouseRun}
        onComplete={refreshData}
      />
    </Paper>
  );
}

export default LinesStatusBoard;
