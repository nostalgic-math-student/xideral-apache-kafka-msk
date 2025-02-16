from kafka.admin import KafkaAdminClient
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

# Región en la que está desplegado MSK Serverless
region = 'us-east-1'

# Clase para generar el token de autenticación usando MSKAuthTokenProvider
class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token

# Instancia del token provider
tp = MSKTokenProvider()

# Configuración del KafkaAdminClient con los parámetros de seguridad
admin_client = KafkaAdminClient(
    bootstrap_servers='MSK-BROKER-URL:PORT',
    client_id='admin_client',
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    # Opcional: en algunos casos puede ser necesario especificar la versión del API manualmente.
    # api_version=(2, 8, 1)
)

# Borrado del tópico creado
admin_client.delete_topics(topics=["template-topic"])
print("Tópico eliminado")

