const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json([
    { product: 'Laptop', price: 1200, stock: 15 },
    { product: 'Printer', price: 300, stock: 8 }
  ]);
});

module.exports = router;
