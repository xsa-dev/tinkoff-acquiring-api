import requests
import hashlib
import uuid
from datetime import datetime

# Конфигурация


def generate_order_id():
    """Генерация уникального ID заказа"""
    return f"ORDER-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:2]}"


def primary_payment(amount, customer_key, email=None, phone=None, description="Первичный платеж"):
    order_id = generate_order_id()
    
    # Параметры для формирования токена
    params = {
        'Amount': str(amount),
        'OrderId': order_id,
        'Password': PASSWORD,
        'TerminalKey': TERMINAL_KEY
    }
    
    # Получаем токен
    token = get_token(params)

    # Формируем данные запроса
    payment_data = {
        'TerminalKey': TERMINAL_KEY,
        'Amount': amount,
        'OrderId': order_id,
        'Token': token,
        'Description': description,
        'CustomerKey': str(customer_key),
        'Recurrent': 'Y',
        'Language': 'ru',
        'SuccessURL': 'https://your-site.com/success',
        'FailURL': 'https://your-site.com/fail',
        'NotificationURL': 'https://your-site.com/notification',
        'DATA': {
            'Email': email,
            'Phone': phone
        }
    }

    response = requests.post(API_URL_INIT, json=payment_data)
    result = response.json()
    
    if result.get('Success'):
        return {
            'success': True,
            'payment_url': result['PaymentURL'],
            'payment_id': result['PaymentId'],
            'order_id': order_id
        }
    else:
        return {
            'success': False,
            'error': f"{result.get('Message')} - {result.get('Details')}"
        }

# Пример использования
if __name__ == "__main__":
    result = primary_payment(
        amount=100000,
        customer_key="CUSTOMER-001",
        email="customer@example.com",
        phone="+79001234567",
        description="Первичный платеж"
    )
    
    if result['success']:
        print("\nPrimary payment initiated successfully:")
        print(f"Payment URL: {result['payment_url']}")
        print(f"Payment ID: {result['payment_id']}")
        print(f"Order ID: {result['order_id']}")
    else:
        print("\nError initiating primary payment:")
        print(f"Error: {result['error']}")

test_payment_data = {
    'TerminalKey': '',
    'Amount': '100000',
    'OrderId': 'TEST-ORDER-001',
    'Description': 'Test payment',
    'Token': 'TOKEN',  # Будет сгенерирован
    'DATA': {
        'Phone': '+79031234567',
        'Email': 'a@test.com'
    }
}