# 🕵️‍♂️ Anonymous Telegram Chat Bot

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=for-the-badge&logo=telegram)
![SQLite](https://img.shields.io/badge/SQLite-DB-lightgrey?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Git](https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## 📌 Description

An anonymous Telegram bot that allows users to send messages (text and photos) to other chat participants **without revealing their identity**. The bot is built on `Aiogram 3.x` and stores users in an SQLite database.

## 🚀 Features

- 📬 Sending anonymous messages to all participants
- 🖼 Support for images with captions
- 🔒 Admin commands with a password
- ✅ Automatic addition of new users
- 🧼 Deleting inactive (erroneous) users

---

## 📁 Project structure

```
#bash
.
├── bot.py # The main logic of the Telegram bot
├── utils/
│ └── db.py # Working with SQLite through SQLAlchemy
├── .env # Token and administrator password
├── requirements.txt # Dependencies
└── README.md # Documentation (you are here)

```

---

## 🔐 Admin commands

- `/users <password>` — list of all user_ids
- `/kick <user_id> <password>` — removing a user

---

Created with ❤️ for the Telegram community.

---
