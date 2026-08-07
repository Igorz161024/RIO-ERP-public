const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json([
    { name: 'Ivan Petrenko', position: 'HR Manager', hired: '2024-05-10' },
    { name: 'Olena Shevchenko', position: 'Recruiter', hired: '2025-01-15' }
  ]);
});

module.exports = router;
