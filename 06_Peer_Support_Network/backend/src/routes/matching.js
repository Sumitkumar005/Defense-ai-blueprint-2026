const express = require('express');
const router = express.Router();
const matchingService = require('../services/matching');

router.post('/find-buddy', async (req, res) => {
  try {
    const { userId, preferences } = req.body;
    const match = await matchingService.findBattleBuddy(userId, preferences);
    res.json(match);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/unit-cohesion/:unitId', async (req, res) => {
  try {
    const { unitId } = req.params;
    const analysis = await matchingService.analyzeUnitCohesion(unitId);
    res.json(analysis);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;

