import random

class PaymentGateway:
    def charge(self, user_id, amount):
        num = random.randint(1, 25)
        if num == 1:
            return {
                "status": "failure"
            }
        else:
            return {
                "status": "success",
            }