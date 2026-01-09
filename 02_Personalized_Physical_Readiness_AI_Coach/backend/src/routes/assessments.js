const express = require('express');
const router = express.Router();
const Assessment = require('../models/Assessment');
const auth = require('../middleware/auth');

router.get('/', auth, async (req, res) => {
  try {
    const assessments = await Assessment.find({ userId: req.user.id })
      .sort({ date: -1 });
    res.json(assessments);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/', auth, async (req, res) => {
  try {
    const assessment = new Assessment({
      userId: req.user.id,
      ...req.body
    });
    await assessment.save();
    res.json(assessment);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;

