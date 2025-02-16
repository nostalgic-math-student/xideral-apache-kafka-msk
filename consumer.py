from kafka import KafkaConsumer
import json
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

# Configuración del tópico, brokers y región
topicname = 'template-topic'
BROKERS = 'MSK-BROKER-URL:PORT'
region = 'us-east-1'

# Definición de la clase que genera el token para autenticación, igual que en el producer
class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token

tp = MSKTokenProvider()

# Configuración del consumer
consumer = KafkaConsumer(
    topicname,
    bootstrap_servers=BROKERS,
    auto_offset_reset='earliest',            # Para leer desde el inicio si no hay offset comprometido
    enable_auto_commit=True,                 # Se autocomitean los offsets
    group_id='mi_consumer_group',            # Define un group id (modifícalo según tus necesidades)
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Deserializa el mensaje de JSON a dict
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
)

print("Consumer iniciado. Esperando mensajes...")

# Bucle infinito para leer y procesar mensajes
try:
    for message in consumer:
        # Cada 'message' es un objeto con metadatos (topic, partition, offset, key, value, etc.)
        print("Mensaje recibido:")
        print("  Topic:     ", message.topic)
        print("  Partition: ", message.partition)
        print("  Offset:    ", message.offset)
        print("  Valor:     ", message.value)
except KeyboardInterrupt:
    print("Consumer interrumpido por el usuario.")
finally:
    consumer.close()
