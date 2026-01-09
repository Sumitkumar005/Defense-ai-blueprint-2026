const express = require('express');
const router = express.Router();
const Assessment = require('../models/Assessment');
const auth = require('../middleware/auth');

router.post('/simulate', auth, async (req, res) => {
  try {
    const { pushups, situps, runTime } = req.body;
    
    // Calculate PT test score (simplified)
    const score = calculatePTScore(pushups, situps, runTime);
    
    res.json({
      score,
      passed: score >= 60,
      breakdown: {
        pushups: pushups,
        situps: situps,
        runTime: runTime
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

function calculatePTScore(pushups, situps, runTime) {
  // Simplified scoring (would use official Army/Navy standards)
  let score = 0;
  score += Math.min(100, (pushups / 50) * 100) * 0.33;
  score += Math.min(100, (situps / 50) * 100) * 0.33;
  score += Math.min(100, ((600 - runTime) / 600) * 100) * 0.34;
  return Math.round(score);
}

module.exports = router;

