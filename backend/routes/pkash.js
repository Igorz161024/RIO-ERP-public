const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json([
    { operation: 'Cash In', amount: 500, date: '2026-04-29' },
    { operation: 'Cash Out', amount: 200, date: '2026-04-28' }
  ]);
});

module.exports = router;
