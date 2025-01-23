import aio_pika
import asyncio



async def get_rabbit_connection():
    """
    Устанавливает соединение с RabbitMQ.

    Возвращает:
        aio_pika.Connection: Соединение с RabbitMQ.
    """
    connection = await aio_pika.connect_robust("amqp://user:password@localhost/")
    return connection

async def send_message(queue_name: str, message: dict):
    """
    Отправляет сообщение в указанную очередь RabbitMQ.

    Args:
        queue_name (str): Имя очереди, в которую будет отправлено сообщение.
        message (dict): Сообщение, которое нужно отправить.
    """
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()  # Создаем канал для общения с RabbitMQ
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(message).encode()),  # Преобразуем сообщение в байты
            routing_key=queue_name,  # Указываем, в какую очередь отправить сообщение
        )
