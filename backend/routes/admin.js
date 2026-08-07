const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');

// Отримати всіх адміністраторів
router.get('/', adminController.getAllAdmins);

module.exports = router;
