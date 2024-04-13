PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_url TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_arrival DATE NOT NULL,
    date_departure DATE NOT NULL,
    userId INTEGER,
    houseId INTEGER,
    FOREIGN KEY(userId) REFERENCES users(id),
    FOREIGN KEY(houseId) REFERENCES houses(id)
);