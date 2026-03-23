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
import Box from "@mui/material/Box";
import { apiService } from "../services/api";

function LinesStatusBoard() {
  const navigate = useNavigate();
  const [lines, setLines] = useState([]);
  const [runs, setRuns] = useState([]);
  const [steps, setSteps] = useState([]);
  const [executions, setExecutions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [linesRes, runsRes, stepsRes] = await Promise.all([
          apiService.lines.getAll(),
          apiService.runs.getAll(),
          apiService.processSteps.getAll(),
        ]);
        const allLines = linesRes.data.data;
        setLines(allLines);

        const stepsData = stepsRes.data.data;
        setSteps(stepsData);

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
        setRuns(allRuns);

        const allExecutions = [];
        for (const run of allRuns) {
          const execRes = await apiService.stepExecutions.getByRun(run.run_id);
          if (execRes.data.data.length === 0 && stepsData.length > 0) {
            const newExec = await apiService.stepExecutions.create({
              run_id: run.run_id,
              step_id: stepsData[0].step_id,
              status: "in_progress",
            });
            allExecutions.push(newExec.data.data);
          } else {
            allExecutions.push(...execRes.data.data);
          }
        }
        setExecutions(allExecutions);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  const getStepStatus = (lineId, stepIndex) => {
    const run = runs.find((r) => r.line_id === lineId);
    if (!run) return { color: "", text: "" };
    const step = steps[stepIndex];
    if (!step) return { color: "", text: "" };
    const execution = executions.find((e) => e.run_id === run.run_id && e.step_id === step.step_id);
    if (!execution) return { color: "", text: "" };
    if (execution.status === "completed")
      return { color: "green", text: execution.signed_by || "✓" };
    if (execution.status === "in_progress") return { color: "yellow", text: "In Progress" };
    return { color: "", text: "" };
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
              {steps.map((step) => (
                <TableCell key={step.step_id}>
                  {step.team_name}
                  <br />
                  <small>{step.task_name}</small>
                </TableCell>
              ))}
              <TableCell sx={{ width: 190 }}>Target Ready Time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {lines.map((line) => {
              const lineRun = runs.find((r) => r.line_id === line.line_id);
              return (
                <TableRow key={line.line_id}>
                  <TableCell
                    sx={{ cursor: "pointer", "&:hover": { bgcolor: "action.hover" } }}
                    onClick={() => navigate(`/line/${line.line_id}`)}                  >
                    {line.line_number}
                  </TableCell>
                  <TableCell>
                    {lineRun?.work_order_end_time
                      ? new Date(lineRun.work_order_end_time).toLocaleString()
                      : "-"}
                  </TableCell>
                  {steps.map((step, i) => {
                    const status = getStepStatus(line.line_id, i);
                    return (
                      <TableCell
                        key={step.step_id}
                        sx={{
                          bgcolor:
                            status.color === "green"
                              ? "#c8e6c9"
                              : status.color === "yellow"
                                ? "#fff9c4"
                                : "transparent",
                        }}
                      ></TableCell>
                    );
                  })}
                  <TableCell>
                    {lineRun?.target_ready_time
                      ? new Date(lineRun.target_ready_time).toLocaleString()
                      : "-"}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default LinesStatusBoard;
