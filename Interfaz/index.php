<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datos del Sensor</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script>
        $(document).ready(function() {
            setInterval(function() {
                $("#sensorData").load("load_sensor_data.php");
            }, 2000); // Carga los datos cada 2 segundos
        });
    </script>
    <style>
        body {
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        .sensor-table th, .sensor-table td {
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="my-4">Datos del Sensor DHT22</h1>
        <div id="sensorData">
            <?php include('load_sensor_data.php'); ?>
        </div>
    </div>
</body>
</html>

