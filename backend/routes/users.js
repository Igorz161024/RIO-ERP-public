const express = require('express');
const router = express.Router();
const usersController = require('../controllers/usersController');

// Отримати всіх користувачів
router.get('/', usersController.getAllUsers);

// Отримати користувача за ID
router.get('/:id', usersController.getUserById);

// Створити нового користувача
router.post('/', usersController.createUser);

// Оновити користувача
router.put('/:id', usersController.updateUser);

// Видалити користувача
router.delete('/:id', usersController.deleteUser);

module.exports = router;
