const express = require('express');
const router = express.Router();

// Тестові дані для Purchases
router.get('/', (req, res) => {
  res.json([
    { id: 1, item: 'Office Chairs', quantity: 10, price: 1500, date: '2026-04-29' },
    { id: 2, item: 'Monitors', quantity: 5, price: 2500, date: '2026-04-28' }
  ]);
});

module.exports = router;
