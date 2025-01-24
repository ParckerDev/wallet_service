from locust import HttpUser, task, between
import random


class WalletUser(HttpUser):
    wait_time = between(1, 5)  # Время ожидания между запросами
    wallet_uuid = "7be560f5-0c21-439d-9a57-e62c51ce5f93"

    def create_wallet(self):
        """
        Отправляет GET-запрос на создание нового кошелька и сохраняет его UUID.
        """
        response = self.client.get(
            "/api/v1/wallets/new"
        )  # Запрос на создание нового кошелька
        if response.status_code == 201:
            # Предполагаем, что сервер возвращает JSON с UUID кошелька
            wallet_data = response.json()  # Извлекаем JSON-ответ
            wallet_uuid = wallet_data.get("uuid")  # Получаем UUID из ответа
            print(f"Кошелек создан: {self.wallet_uuid}")
            return wallet_uuid
        else:
            print(f"Ошибка при создании кошелька: {response.text}")

    @task
    def deposit(self):
        """
        Выполняет операцию депозита на созданный кошелек.
        """
        amount = random.randint(1, 100)  # Генерируем случайную сумму для депозита
        self.client.post(
            f"/api/v1/wallets/{self.wallet_uuid}/operation",
            json={"operation_type": "DEPOSIT", "amount": amount},
        )

    @task
    def withdraw(self):
        """
        Выполняет операцию вывода с созданного кошелька.
        """
        amount = random.randint(1, 100)  # Генерируем случайную сумму для вывода
        self.client.post(
            f"/api/v1/wallets/{self.wallet_uuid}/operation",
            json={"operation_type": "WITHDRAW", "amount": amount},
        )


# for run test input:
# locust -f test.py --host=http://localhost:8000
