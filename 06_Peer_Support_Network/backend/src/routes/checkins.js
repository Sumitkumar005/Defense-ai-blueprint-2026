const express = require('express');
const router = express.Router();
const CheckIn = require('../models/CheckIn');
const sentimentAnalyzer = require('../services/sentiment');

router.post('/', async (req, res) => {
  try {
    const { userId, battleBuddyId, mood, notes } = req.body;
    
    // Analyze sentiment
    const sentiment = await sentimentAnalyzer.analyzeCheckIn(notes || '');
    
    const checkIn = new CheckIn({
      userId,
      battleBuddyId,
      mood,
      notes,
      sentimentScore: sentiment.sentimentScore,
      concerns: sentiment.requiresEscalation ? ['Requires attention'] : []
    });
    
    await checkIn.save();
    
    // Escalate if needed
    if (sentiment.requiresEscalation) {
      // PLACEHOLDER: Would notify chain of command
      console.log('ALERT: Check-in requires escalation', checkIn._id);
    }
    
    res.json(checkIn);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/', async (req, res) => {
  try {
    const { userId } = req.query;
    const checkIns = await CheckIn.find({ userId })
      .sort({ createdAt: -1 })
      .limit(30);
    res.json(checkIns);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;

