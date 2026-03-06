import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

function LinesStatusBoard() {
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
        Lines Status Board
      </Typography>
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
            {/* Table rows will go here */}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default LinesStatusBoard;
