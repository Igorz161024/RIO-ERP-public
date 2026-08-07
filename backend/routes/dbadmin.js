const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json([
    { table: 'users', rows: 120 },
    { table: 'finance', rows: 45 }
  ]);
});

module.exports = router;
