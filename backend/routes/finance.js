const express = require('express');
const router = express.Router();

// Тестові дані для фінансів
router.get('/', (req, res) => {
  res.json([
    { amount: 1000, description: 'Invoice #123', date: '2026-04-29' },
    { amount: 2500, description: 'Payment HR', date: '2026-04-28' }
  ]);
});

module.exports = router;
