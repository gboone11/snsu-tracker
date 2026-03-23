import { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Box from "@mui/material/Box";
import { apiService } from "../services/api";

function LinesStatusBoard() {
  const navigate = useNavigate();
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState("");
  const [lines, setLines] = useState([]);
  const [runs, setRuns] = useState([]);
  const [steps, setSteps] = useState([]);
  const [executions, setExecutions] = useState([]);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await apiService.lineGroups.getAll();
        setGroups(response.data.data);
        const params = new URLSearchParams(window.location.search);
        const groupParam = params.get("group");
        if (groupParam) {
          setSelectedGroup(parseInt(groupParam));
        } else if (response.data.data.length > 0) {
          setSelectedGroup(response.data.data[0].group_id);
        }
      } catch (error) {
        console.error("Error fetching groups:", error);
      }
    };
    fetchGroups();
  }, []);

  useEffect(() => {
    if (!selectedGroup) return;
    const fetchData = async () => {
      try {
        const [linesRes, runsRes, stepsRes] = await Promise.all([
          apiService.lines.getAll(),
          apiService.runs.getAll(),
          apiService.processSteps.getByGroup(selectedGroup),
        ]);
        const groupLines = linesRes.data.data.filter((l) => l.line_group_id === selectedGroup);
        setLines(groupLines);
        setSteps(stepsRes.data.data);

        const allRuns = [...runsRes.data.data];
        for (const line of groupLines) {
          if (!allRuns.find((r) => r.line_id === line.line_id)) {
            const newRunRes = await apiService.runs.create({
              line_id: line.line_id,
              work_order_end_time: new Date().toISOString(),
              target_ready_time: new Date().toISOString(),
              status: "in_progress",
            });
            allRuns.push(newRunRes.data.data);
          }
        }
        setRuns(allRuns);

        const allExecutions = [];
        for (const run of allRuns) {
          const execRes = await apiService.stepExecutions.getByRun(run.run_id);

          // Create first step execution if none exist
          if (execRes.data.data.length === 0 && stepsRes.data.data.length > 0) {
            const newExec = await apiService.stepExecutions.create({
              run_id: run.run_id,
              step_id: stepsRes.data.data[0].step_id,
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
  }, [selectedGroup]);

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

  const randomEndTimes = useMemo(() => {
    const today = new Date();
    const daysSinceFriday = (today.getDay() + 2) % 7;
    return Object.fromEntries(
      lines.map((line) => {
        const friday = new Date(today);
        friday.setDate(today.getDate() - daysSinceFriday);
        /* eslint-disable */
        friday.setHours(
          Math.floor(Math.random() * 9) + 15,
          Math.floor(Math.random() * 60),
          Math.floor(Math.random() * 60),
          0,
        ); 
        /* eslint-enable */
        return [line.line_id, friday.toLocaleString()];
      }),
    );
  }, [lines]);

  const randomStartTimes = useMemo(() => {
    const today = new Date();
    const daysSinceMonday = (today.getDay() + 6) % 7;
    return Object.fromEntries(
      lines.map((line) => {
        const monday = new Date(today);
        monday.setDate(today.getDate() - daysSinceMonday);
        /* eslint-disable */
        monday.setHours(
          Math.floor(Math.random() * 5) + 7,
          Math.floor(Math.random() * 60),
          Math.floor(Math.random() * 60),
          0,
        ); 
        /* eslint-enable */
        return [line.line_id, monday.toLocaleString()];
      }),
    );
  }, [lines]);

  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Lines Status Board
        </Typography>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Group</InputLabel>
          <Select
            value={selectedGroup}
            label="Group"
            onChange={(e) => setSelectedGroup(e.target.value)}
          >
            {groups.map((group) => (
              <MenuItem key={group.group_id} value={group.group_id}>
                {group.group_name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Line</TableCell>
              <TableCell>Work Order Ended</TableCell>
              {steps.map((step) => (
                <TableCell key={step.step_id}>
                  {step.team_name}
                  <br />
                  <small>{step.task_name}</small>
                </TableCell>
              ))}
              <TableCell>Work Order Starts</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {lines.map((line) => {
              return (
                <TableRow key={line.line_id}>
                  <TableCell
                    sx={{ cursor: "pointer", "&:hover": { bgcolor: "action.hover" } }}
                    onClick={() => navigate(`/line/${line.line_id}?group=${selectedGroup}`)}
                  >
                    {line.line_number}
                  </TableCell>
                  <TableCell>{randomEndTimes[line.line_id]}</TableCell>
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
                      >
                        {""}
                      </TableCell>
                    );
                  })}
                  <TableCell>{randomStartTimes[line.line_id]}</TableCell>
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
