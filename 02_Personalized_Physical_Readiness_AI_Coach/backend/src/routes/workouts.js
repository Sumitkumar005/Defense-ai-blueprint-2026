/**
 * Workout Routes
 */

const express = require('express');
const router = express.Router();
const Workout = require('../models/Workout');
const auth = require('../middleware/auth');
const { generateWorkout } = require('../services/workoutGenerator');

// Get user's workouts
router.get('/', auth, async (req, res) => {
  try {
    const workouts = await Workout.find({ userId: req.user.id })
      .sort({ date: -1 })
      .limit(50);
    res.json(workouts);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Generate AI workout
router.post('/generate', auth, async (req, res) => {
  try {
    const { date, type, goals } = req.body;
    
    const workout = await generateWorkout(
      req.user.id,
      date || new Date(),
      type,
      goals
    );
    
    res.json(workout);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Complete workout
router.patch('/:id/complete', auth, async (req, res) => {
  try {
    const { performance, formScore } = req.body;
    
    const workout = await Workout.findOne({
      _id: req.params.id,
      userId: req.user.id
    });
    
    if (!workout) {
      return res.status(404).json({ error: 'Workout not found' });
    }
    
    workout.completed = true;
    workout.performance = {
      ...workout.performance,
      ...performance,
      formScore
    };
    
    await workout.save();
    res.json(workout);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Analyze form from video
router.post('/:id/analyze-form', auth, async (req, res) => {
  try {
    // PLACEHOLDER: In production, this would:
    // 1. Receive video file
    // 2. Process with MediaPipe/YOLOv8
    // 3. Analyze exercise form
    // 4. Return feedback
    
    const { videoUrl, exerciseType } = req.body;
    
    // Mock form analysis
    const formScore = Math.floor(Math.random() * 30) + 70; // 70-100
    const feedback = [
      "Good form overall",
      "Maintain straight back during pushups",
      "Full range of motion achieved"
    ];
    
    res.json({
      formScore,
      feedback,
      improvements: ["Focus on core engagement", "Slight knee alignment issue"]
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;

