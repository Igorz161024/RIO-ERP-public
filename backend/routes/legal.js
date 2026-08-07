const express = require('express');
const router = express.Router();
const legalController = require('../controllers/legalController');

// Отримати всі юридичні документи
router.get('/', legalController.getAllLegalDocs);

module.exports = router;
