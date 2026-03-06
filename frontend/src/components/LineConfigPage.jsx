import { useState } from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import { apiService } from '../services/api';

function LineConfigPage() {
  const [groups, setGroups] = useState({
    '24-5': ['1', '2', '5', '7', '9', '15', '16', '17', '18'],
    '24-7': ['11', '12', '13', '14', '91', '92', '93'],
    'spirits': ['21', '23', '24']
  });
  const [newGroupName, setNewGroupName] = useState('');
  const [newLineInputs, setNewLineInputs] = useState({});

  const handleCreateGroup = async () => {
    if (!newGroupName.trim()) return;
    if (groups[newGroupName]) {
      alert('Group already exists');
      return;
    }
    
    try {
      await apiService.lineGroups.create({ group_name: newGroupName });
      setGroups({ ...groups, [newGroupName]: [] });
      setNewGroupName('');
    } catch (error) {
      alert('Error creating group: ' + error.message);
    }
  };

  const handleDeleteGroup = (groupName) => {
    if (!window.confirm(`Delete group "${groupName}" and all its lines?`)) return;
    const newGroups = { ...groups };
    delete newGroups[groupName];
    setGroups(newGroups);
  };

  const handleAddLine = (groupName) => {
    const lineNum = newLineInputs[groupName]?.trim();
    if (!lineNum) return;
    
    // Check if line exists in any group
    const lineExists = Object.values(groups).some(lines => lines.includes(lineNum));
    if (lineExists) {
      alert('Line already exists');
      return;
    }

    setGroups({
      ...groups,
      [groupName]: [...groups[groupName], lineNum]
    });
    setNewLineInputs({ ...newLineInputs, [groupName]: '' });
  };

  const handleRemoveLine = (groupName, lineNum) => {
    if (!window.confirm(`Remove Line ${lineNum} from group "${groupName}"?`)) return;
    setGroups({
      ...groups,
      [groupName]: groups[groupName].filter(l => l !== lineNum)
    });
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 600, textAlign: 'center' }}>
        Group & Line Configuration
      </Typography>

      <Paper sx={{ p: 2.5, mb: 3, bgcolor: 'background.paper' }}>
        <Typography variant="h6" sx={{ mb: 2, color: 'primary.main' }}>
          Create New Group
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Group name (e.g., 24/5)"
            value={newGroupName}
            onChange={(e) => setNewGroupName(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleCreateGroup()}
          />
          <Button variant="contained" onClick={handleCreateGroup}>
            + Create Group
          </Button>
        </Box>
      </Paper>

      {Object.entries(groups).map(([groupName, lines]) => (
        <Paper key={groupName} sx={{ p: 2.5, mb: 2, bgcolor: 'background.paper' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ color: 'primary.main' }}>
              Group: {groupName}
            </Typography>
            <Button
              variant="contained"
              color="error"
              size="small"
              startIcon={<DeleteIcon />}
              onClick={() => handleDeleteGroup(groupName)}
            >
              Delete Group
            </Button>
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1.5, fontWeight: 600, color: 'primary.main' }}>
              Lines in this group:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {lines.map(line => (
                <Box
                  key={line}
                  sx={{
                    bgcolor: 'background.default',
                    px: 1.5,
                    py: 0.75,
                    borderRadius: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1
                  }}
                >
                  <Typography variant="body2">Line {line}</Typography>
                  <IconButton
                    size="small"
                    sx={{ p: 0.25, color: 'error.main' }}
                    onClick={() => handleRemoveLine(groupName, line)}
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </Box>
              ))}
              {lines.length === 0 && (
                <Typography variant="body2" sx={{ color: 'text.secondary', fontStyle: 'italic' }}>
                  No lines in this group
                </Typography>
              )}
            </Box>
          </Box>

          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              size="small"
              placeholder="Add line number"
              value={newLineInputs[groupName] || ''}
              onChange={(e) => setNewLineInputs({ ...newLineInputs, [groupName]: e.target.value })}
              onKeyPress={(e) => e.key === 'Enter' && handleAddLine(groupName)}
              sx={{ width: 200 }}
            />
            <Button variant="contained" onClick={() => handleAddLine(groupName)}>
              + Add Line
            </Button>
          </Box>
        </Paper>
      ))}
    </Box>
  );
}

export default LineConfigPage;
