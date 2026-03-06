import { useState, useEffect } from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Box from '@mui/material/Box';
import { apiService } from '../services/api';

function LinesStatusBoard() {
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState('');
  const [lines, setLines] = useState([]);
  const [runs, setRuns] = useState([]);
  const [steps, setSteps] = useState([]);
  const [executions, setExecutions] = useState([]);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await apiService.lineGroups.getAll();
        setGroups(response.data.data);
        if (response.data.data.length > 0) {
          setSelectedGroup(response.data.data[0].group_id);
        }
      } catch (error) {
        console.error('Error fetching groups:', error);
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
          apiService.runs.getActive(),
          apiService.processSteps.getByGroup(selectedGroup)
        ]);
        const groupLines = linesRes.data.data.filter(l => l.line_group_id === selectedGroup);
        setLines(groupLines);
        setRuns(runsRes.data.data);
        setSteps(stepsRes.data.data);
        
        const allExecutions = [];
        for (const run of runsRes.data.data) {
          const execRes = await apiService.stepExecutions.getByRun(run.run_id);
          allExecutions.push(...execRes.data.data);
        }
        setExecutions(allExecutions);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, [selectedGroup]);

  const getStepStatus = (lineId, stepIndex) => {
    const run = runs.find(r => r.line_id === lineId);
    if (!run) return '';
    const step = steps[stepIndex];
    if (!step) return '';
    const execution = executions.find(e => e.run_id === run.run_id && e.step_id === step.step_id);
    if (!execution) return '';
    if (execution.status === 'completed') return 'green';
    if (execution.status === 'in_progress') return 'yellow';
    return '';
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
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
              <TableCell>Operations<br /><small>Line Cleaned and Released</small></TableCell>
              <TableCell>Maintenance<br /><small>Remove bottle handling parts & screens</small></TableCell>
              <TableCell>Finish Wine<br /><small>Caustic, Sterox, Cleanup</small></TableCell>
              <TableCell>Maintenance<br /><small>Lubrication, Install Screens</small></TableCell>
              <TableCell>Sanitation<br /><small>Deep Clean Filler, Line/Ph Swab</small></TableCell>
              <TableCell>Maintenance<br /><small>Filler Checkout, Verify screens</small></TableCell>
              <TableCell>Sanitation<br /><small>Hot Soap, Foam, SSP</small></TableCell>
              <TableCell>Finish Wine<br /><small>Hot water Sanitation</small></TableCell>
              <TableCell>WAM Lab<br /><small>ATP Swab</small></TableCell>
              <TableCell>Finished Wine<br /><small>Pull Samples</small></TableCell>
              <TableCell>Warehouse<br /><small>Material Ready</small></TableCell>
              <TableCell>Operations<br /><small>Line Received Material</small></TableCell>
              <TableCell>Operations<br /><small>HACCP/SSP/Start</small></TableCell>
              <TableCell>Time Till Startup</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {lines.map((line) => {
              const run = runs.find(r => r.line_id === line.line_id);
              return (
                <TableRow key={line.line_id}>
                  <TableCell>{line.line_number}</TableCell>
                  <TableCell>{run?.work_order_end_time || '-'}</TableCell>
                  {[...Array(13)].map((_, i) => (
                    <TableCell 
                      key={i}
                      sx={{ 
                        bgcolor: getStepStatus(line.line_id, i) === 'green' ? 'success.light' : 
                                getStepStatus(line.line_id, i) === 'yellow' ? 'warning.light' : 'transparent'
                      }}
                    />
                  ))}
                  <TableCell>{run?.target_ready_time || '-'}</TableCell>
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
