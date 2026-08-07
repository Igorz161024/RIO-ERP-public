const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json([
    { entry: 'Finance operation #123', date: '2026-04-29' },
    { entry: 'HR contract signed', date: '2026-04-28' }
  ]);
});

module.exports = router;
