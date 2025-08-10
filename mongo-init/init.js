// Switch to your target database
db = db.getSiblingDB('weather_db');

// Create a collection (optional)
db.createCollection('weather_data');

// Create a user for this database
db.createUser({
  user: "admin",
  pwd: "password", // change this
  roles: [
    {
      role: "readWrite",
      db: "weather_db"
    }
  ]
});
