import machine
import dht
import utime
import urequests as requests
import network

# Identificador único del sensor
sensor_id = 1  # Asegúrate de que este ID sea único para cada sensor si estás desplegando múltiples unidades

# Configuración de Wi-Fi
ssid = 'Totalplay-C1A2' #agrega tu nombre de internet
password = 'C1A25AF26uQuFC6w' #agrega la contraseña

# Conectarse a Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Espera hasta que esté conectado
while not wlan.isconnected():
    utime.sleep(1)

print("Conectado a Wi-Fi")

# Configuración del pin y del sensor
dht_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
dht_sensor = dht.DHT22(dht_pin)

# Valores máximos y mínimos
temp_max = 26.0
temp_min = 21.0
hum_max = 55.0
hum_min = 30.0

# URL de la API
api_url = 'http://192.168.100.41:3000/sensor-data'  # Asegúrate de que esta dirección IP sea accesible

# Cálculo del índice de calor
def heat_index(temp, hum):
    return -8.78469475556 + 1.61139411 * temp + 2.33854883889 * hum - 0.14611605 * temp * hum \
           - 0.012308094 * temp**2 - 0.0164248277778 * hum**2 + 0.002211732 * temp**2 * hum \
           + 0.00072546 * temp * hum**2 - 0.000003582 * temp**2 * hum**2

# Lectura de los datos del sensor
def read_dht():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        return temp, hum
    except Exception as e:
        print("Error al leer el sensor DHT22:", e)
        return None, None

# Envío de los datos a la API
def send_data_to_api(sensor_id, temp, hum, heat_idx):
    data = {'sensor_id': sensor_id, 'temperature': temp, 'humidity': hum, 'heat_index': heat_idx}
    try:
        response = requests.post(api_url, json=data)
        print("Respuesta del servidor:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar datos a la API:", e)

# Bucle principal
while True:
    temp, hum = read_dht()
    if temp is not None and hum is not None:
        hi = heat_index(temp, hum)
        print(f"Temperatura: {temp} °C, Humedad: {hum} %, Índice de Calor: {hi}")
        send_data_to_api(sensor_id, temp, hum, hi)
    utime.sleep(30)


