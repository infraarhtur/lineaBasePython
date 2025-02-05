import json

from app.config import Config
from app.infrastructure.aws_sqs import SQSClient


class MessageService:
    def __init__(self):
        self.config = Config("config.yaml")
        self.root = self.config.get("sqs","url-queue-client")
        self.sqs_client = SQSClient(queue_url=self.root)

    def process_messages(self):
        """Recibe y procesa los mensajes de la cola"""
        messages = self.sqs_client.receive_messages()
        messages_data = []
        for message in messages:
            try:
                data = json.loads(message['Body'])  # Convertir a JSON
                print(f"Procesando mensaje: {data}")  # Aquí pondrías la lógica real

                # Marcar el mensaje como procesado eliminándolo de la cola
                self.sqs_client.delete_message(message['ReceiptHandle'])
                print("Mensaje procesado y eliminado de la cola.")
                messages_data.append(data)        

            except Exception as e:
                print(f"Error al procesar mensaje: {e}")

        return messages_data

    def enviar_mensaje(self, payload):
        """Envía un mensaje a la cola SQS"""
        
        message_id = self.sqs_client.send_message(payload)
        print(f"Mensaje enviado con ID: {message_id}")
        return message_id
    
