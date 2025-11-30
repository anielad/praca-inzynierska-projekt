import React, { useState } from 'react';
import { Box, Slider, Button, Typography, Paper } from '@mui/material';
import axios from 'axios';
import { useDispatch, useSelector } from 'react-redux';
import { setWorkout } from '../store/workoutSlice';

const MoodForm = () => {
const [fatigue, setFatigue] = useState(5);
const [stress, setStress] = useState(5);
const [motivation, setMotivation] = useState(5);
const [loading, setLoading] = useState(false);
const dispatch = useDispatch();
const token = useSelector(state => state.auth.token);
const handleSubmit = async (e) => {
e.preventDefault();
setLoading(true);
try {
const response = await axios.post(
`${process.env.REACT_APP_API_URL}/api/mood`,
{ fatigue, stress, motivation },
{ headers: { Authorization: `Bearer ${token}` } }
);
dispatch(setWorkout(response.data.workout));
console.log('Plan treningowy wygenerowany:', response.data);
} catch (error) {
console.error('Błąd:', error.response.data);
} finally {
setLoading(false);
}
};
return (
<Paper elevation={3} sx={{ p: 3, maxWidth: 500, mx: 'auto' }}>
<Typography variant="h5" gutterBottom>
Jak się dzisiaj czujesz?
</Typography>
<Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
{/* Slider Zmęczenia */}
<Box sx={{ mb: 3 }}>
<Typography variant="body1">
Zmęczenie: <strong>{fatigue}/10</strong>
</Typography>
<Slider
value={fatigue}
onChange={(e, val) => setFatigue(val)}
min={1}
max={10}
marks
valueLabelDisplay="auto"
/>
</Box>
{/* Slider Stresu */}
<Box sx={{ mb: 3 }}>
<Typography variant="body1">
Stres: <strong>{stress}/10</strong>
</Typography>
<Slider
value={stress}
onChange={(e, val) => setStress(val)}
min={1}
max={10}
marks
valueLabelDisplay="auto"
/>
</Box>
{/* Slider Motywacji */}
<Box sx={{ mb: 3 }}>
<Typography variant="body1">
Motywacja: <strong>{motivation}/10</strong>
</Typography>
<Slider
value={motivation}
onChange={(e, val) => setMotivation(val)}
min={1}
max={10}
marks
valueLabelDisplay="auto"
/>
</Box>
<Button
type="submit"
variant="contained"
color="primary"
fullWidth
disabled={loading}
>
{loading ? 'Generowanie planu...' : 'Wygeneruj plan treningowy'}
</Button>
</Box>
</Paper>
);
};
export default MoodForm;