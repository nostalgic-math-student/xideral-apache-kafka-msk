from kafka import KafkaProducer
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
import json

# Configuración del tópico y del broker
topicname = 'template-topic'
BROKERS = 'MSK-BROKER-URL:PORT'
region = 'us-east-1'

# Clase para obtener el token de autenticación
class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token

tp = MSKTokenProvider()

# Configuración del productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=BROKERS,
    # Se utiliza JSON para serializar el mensaje
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retry_backoff_ms=500,
    request_timeout_ms=20000,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
)

# Mensaje que se enviará
mensaje = "Hola mundo de MSK Kafka"

# Envío del mensaje
try:
    future = producer.send(topicname, value=mensaje)
    producer.flush()  # Asegura que el mensaje se envíe de inmediato
    record_metadata = future.get(timeout=10)
    print("Mensaje enviado:", mensaje)
except Exception as e:
    print("Error al enviar el mensaje:", e)
