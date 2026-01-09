const express = require('express');
const router = express.Router();
const Workout = require('../models/Workout');
const auth = require('../middleware/auth');

router.get('/personal', auth, async (req, res) => {
  try {
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    
    const workouts = await Workout.find({
      userId: req.user.id,
      date: { $gte: weekAgo },
      completed: true
    });
    
    const avgFormScore = workouts.length > 0
      ? workouts.reduce((sum, w) => sum + (w.performance?.formScore || 0), 0) / workouts.length
      : 0;
    
    res.json({
      workoutsThisWeek: workouts.length,
      avgFormScore: Math.round(avgFormScore)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;

