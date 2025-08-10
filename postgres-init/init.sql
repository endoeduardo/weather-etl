-- Enable pgcrypto for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6)
);

INSERT INTO locations (city, state, country, latitude, longitude) VALUES
  ('Curitiba', 'PR', 'Brazil', -25.4284, -49.2733),
  ('São Paulo', 'SP', 'Brazil', -23.5505, -46.6333),
  ('Brasilia', 'DF', 'Brazil', -15.7801, -47.9292);

CREATE TABLE forecast (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID REFERENCES locations(id),
  forecast_date TIMESTAMP,
  temperature DECIMAL(5,2),
  temperature_min DECIMAL(5,2),
  temperature_max DECIMAL(5,2),
  feels_like DECIMAL(5,2),
  condition VARCHAR(100)
);