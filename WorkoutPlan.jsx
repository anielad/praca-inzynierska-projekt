import React from 'react';
import { Box, Card, CardContent, Typography, List, ListItem, Chip } from '@mui/material';
import { useSelector } from 'react-redux';
const WorkoutPlan = () => {
const workout = useSelector(state => state.workout.currentPlan);
if (!workout) {
return <Typography>Brak aktualnego planu. Wypełnij formularz samopoczucia.</Typography>
}
return (
<Box sx={{ mt: 4 }}>
<Card>
<CardContent>
<Typography variant="h5" gutterBottom>
{workout.type}
</Typography>
<Chip
label={`Intensywność: ${workout.intensity}%`}
color={workout.intensity > 70 ? 'error' : 'primary'}
sx={{ mb: 2 }}
/>
<Typography variant="h6" sx={{ mt: 2 }}>Ćwiczenia:</Typography>
<List>
{workout.exercises.map((exercise, idx) => (
<ListItem key={idx}>
<Box>
<Typography variant="body1"><strong>{exercise.name}</strong></Typography>
<Typography variant="body2" color="textSecondary">
Serie: {exercise.sets} × Powtórzenia: {exercise.reps}
{exercise.weight && ` (${exercise.weight})`}
</Typography>
</Box>
</ListItem>
))}
</List>
</CardContent>
</Card>
</Box>
);
};
export default WorkoutPlan;
