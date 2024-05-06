<?php
$host = 'localhost'; // o la IP del servidor de la base de datos
$dbname = 'sensor_data';
$username = 'root';
$password = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->query("SELECT * FROM sensor_readings ORDER BY created_at DESC LIMIT 1");
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($row) {
        echo "<table class='table table-striped sensor-table'>";
        echo "<thead><tr><th>Temperatura</th><th>Humedad</th><th>Índice de Calor</th></tr></thead>";
        echo "<tbody>";
        echo "<tr>";
        echo "<td>" . htmlspecialchars($row['temperature']) . " °C</td>";
        echo "<td>" . htmlspecialchars($row['humidity']) . " %</td>";
        echo "<td>" . htmlspecialchars($row['heat_index']) . "</td>";
        echo "</tr>";
        echo "</tbody></table>";
    } else {
        echo "<p>No hay datos disponibles.</p>";
    }
} catch (PDOException $e) {
    die("No se pudo conectar a la base de datos $dbname :" . $e->getMessage());
}
?>

