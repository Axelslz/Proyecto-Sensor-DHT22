const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const port = 3000;

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'sensor_data'
});

db.connect(err => {
  if (err) {
    throw err;
  }
  console.log('Conectado a la base de datos MySQL');
});

app.use(bodyParser.json());

app.post('/sensor-data', (req, res) => {
  const { sensor_id, temperature, humidity, heat_index } = req.body;

  if (!sensor_id) {
      return res.status(400).json({ error: 'sensor_id es requerido' });
  }

  console.log('Recibido:', { sensor_id, temperature, humidity, heat_index });

  // Insertar en la tabla de último estado
  const sqlUpdate = `INSERT INTO sensor_readings (sensor_id, temperature, humidity, heat_index)
                     VALUES (?, ?, ?, ?)
                     ON DUPLICATE KEY UPDATE
                     temperature = VALUES(temperature),
                     humidity = VALUES(humidity),
                     heat_index = VALUES(heat_index)`;

  // Insertar en la tabla de historial
  const sqlHistory = `INSERT INTO sensor_readings_history (sensor_id, temperature, humidity, heat_index)
                      VALUES (?, ?, ?, ?)`;

  // Ejecutar las consultas
  db.query(sqlUpdate, [sensor_id, temperature, humidity, heat_index], (err, result) => {
      if (err) {
          console.error('Error al actualizar datos en la base de datos:', err);
          return res.status(500).json({ error: 'Error interno del servidor' });
      }
      console.log('Datos actualizados correctamente en la base de datos');
      // Insertar en el historial después de actualizar el último estado
      db.query(sqlHistory, [sensor_id, temperature, humidity, heat_index], (err, result) => {
          if (err) {
              console.error('Error al insertar en la tabla de historial:', err);
              return res.status(500).json({ error: 'Error interno del servidor al insertar historial' });
          }
          console.log('Historial registrado correctamente');
          res.status(200).json({ message: 'Datos actualizados y registrados en el historial correctamente' });
      });
  });
});

app.listen(port, '192.168.100.41', () => {
    console.log(`Server listening on port ${port}`);
});


