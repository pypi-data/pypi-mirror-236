import requests
import json
from . import core
from . import types
from . import exceptions
from typing import List, Literal


class BillingAPI:
    def __init__(self, api_token: str, environment_id: int, api_url: str = None) -> None:
        assert isinstance(environment_id, int)
        self.api_token = api_token
        self.environment_id = environment_id
        self._requests_params = {
            "verify": False
        }
        if api_url is not None:
            assert api_token.endswith('/')

        self.api_url = api_url or core.API_URL
        self.__load_api_urls()
        self.ping()

    def __load_api_urls(self):
        self.__user_api_url = self.api_url + 'user/'
        self.__deposit_api_url = self.api_url + 'deposit/'
        self.__ping_api_url = self.api_url + 'ping/'
        self.__withdrawal_api_url = self.api_url + 'withdrawal/'
        self.__in_system_transfer_api_url = self.api_url + 'transfer/in/'
        self.__out_system_transfer_api_url = self.api_url + 'transfer/out/'
        self.__transactions_api_url = self.api_url + 'transactions/'
        self.__subscriptions_api_url = self.api_url + 'subscriptions/'
        self.__subscription_plans_api_url = self.api_url + 'subscription_plans/'
        self.__out_system_service_api_url = self.api_url + 'out_system_service/'

    def _exception_raiser(self, response: requests.Response):
        if response.status_code // 100 != 2:
            if response.headers.get('Content-Type') == 'application/json':
                error_data = json.load(response.body)
                exc = exceptions.exceptions_register.get(error_data['error_code'])
                if exc is not None:
                    raise exc
                
                raise Exception(error_data['error_message'])
            
            response.raise_for_status()

    @property
    def headers(self):
        return {
            "Authorization": f"Token {self.api_token}"
        } 

    def ping(self):
        params = {
            "environment": self.environment_id,
        }
        response = requests.get(
            url=self.__ping_api_url,
            headers=self.headers,
            params=params,
            **self._requests_params,
        )
        self._exception_raiser(response)
        assert json.loads(response.text)['status'] == 'ok'


    def create_user(self, unique_id: str, **kwars) -> types.BillingUser:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            **kwars
        }

        response = requests.post(
            url=self.__user_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)
        data.pop('environment')
        return types.BillingUser.from_dict(balance=0, **data)

    def update_user(self, unique_id: str, **kwars) -> types.BillingUser:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            **kwars
        }
        response = requests.patch(
            url=self.__user_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)
        data.pop('environment')
        return types.BillingUser.from_dict(**data)
    
    def get_user(self, unique_id: str) -> types.BillingUser:
        params = {
            "environment": self.environment_id,
            "unique_id": unique_id,
        }
        
        response = requests.get(
            url=self.__user_api_url,
            headers=self.headers,
            params=params,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)
        data.pop('environment')
        return types.BillingUser.from_dict(**data)

    def get_users(self) -> List[types.BillingUser]:
        params = {
            "environment": self.environment_id,
        }
        
        response = requests.get(
            url=self.__user_api_url,
            headers=self.headers,
            params=params,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)
        users = list()
        for user in data['users']:
            user.pop('environment')
            users.append(types.BillingUser.from_dict(**user))
        
        return users
        
    def deposit(self, unique_id: str, amount: float, comment: str = None) -> types.Transaction:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            "amount": amount,
            "comment": comment or ''
        }

        response = requests.post(
            url=self.__deposit_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Transaction.from_dict(**data)
    

    def withdrawal(self, unique_id: str, amount: float, comment: str = None, fee_on_sender: bool = False) -> types.Transaction:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            "amount": amount,
            "comment": comment or '',
            "fee_on_sender": fee_on_sender
        }

        response = requests.post(
            url=self.__withdrawal_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Transaction.from_dict(**data)
    
    def process_withdrawal(self, unique_id: str, transaction_id: int, status: bool = True) -> types.Transaction:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            "transaction_id": transaction_id,
            "status": status
        }

        response = requests.patch(
            url=self.__withdrawal_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Transaction.from_dict(**data)

    def in_system_transfer(self, from_unique_id: str, to_unique_id: str, amount: float, comment: str = None, fee_on_sender: bool = True) -> types.Transaction:
        body = {
            "environment": self.environment_id,
            "from_unique_id": from_unique_id,
            "to_unique_id": to_unique_id,
            "amount": amount,
            "comment": comment or '',
            "fee_on_sender": fee_on_sender
        }

        response = requests.post(
            url=self.__in_system_transfer_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Transaction.from_dict(**data)

    def out_system_transfer(self, unique_id: str, amount: float, comment: str = None, fee_on_sender: bool = False, service_unique_id: str = None) -> types.Transaction:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            "amount": amount,
            "comment": comment or '',
            "fee_on_sender": fee_on_sender,
            "service_unique_id": service_unique_id
        }

        response = requests.post(
            url=self.__out_system_transfer_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params,
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Transaction.from_dict(**data)
    
    def get_out_system_service(self, service_unique_id: str) -> types.OutSystemService:
        body = {
            "environment": self.environment_id,
            "service_unique_id": service_unique_id
        }

        response = requests.get(
            url=self.__out_system_service_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.OutSystemService.from_dict(**data)

    def create_out_system_service(self, service_unique_id: str, title: str, service_prefix: str = '', description: str = '', cost: float = None):
        body = {
            "environment": self.environment_id,
            "service_unique_id": service_unique_id,
            "service_prefix": service_prefix,
            "title": title,
            "description": description,
            "cost": cost,
        }

        response = requests.post(
            url=self.__out_system_service_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.OutSystemService.from_dict(**data)

    def get_out_system_services(self, service_prefix: str = '') -> List[types.OutSystemService]:
        body = {
            "environment": self.environment_id,
            "service_prefix": service_prefix
        }

        response = requests.get(
            url=self.__out_system_service_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        services = list()
        for service in data['services']:
            services.append(types.OutSystemService.from_dict(**service))

        return services

    def create_subscription_plan(self, plan_unique_id: str, 
    service_unique_id: str = None, type: Literal["default", "count"] = "default",
    first_payment_amount: float = 0, amount: float = 0, days_frequency: int = 7
    ) -> types.SubscriptionPlan:
        body = {
            "environment": self.environment_id,
            "plan_unique_id": plan_unique_id,
            "service_unique_id": service_unique_id,
            "type": type,
            "first_payment_amount": first_payment_amount,
            "amount": amount,
            "days_frequency": days_frequency
        }

        response = requests.post(
            url=self.__subscription_plans_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.SubscriptionPlan.from_dict(**data)

    def get_user_transactions(self, unique_id: str) -> List[types.Transaction]:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
        }

        response = requests.get(
            url=self.__transactions_api_url,
            headers=self.headers,
            params=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        transactions = list()
        for transaction in data['transactions']:
            transactions.append(types.Transaction.from_dict(**transaction))
        
        return transactions

    
    def get_user_subscriptions(self, unique_id: str) -> List[types.Subscription]:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
        }

        response = requests.get(
            url=self.__subscriptions_api_url,
            headers=self.headers,
            params=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        subscriptions = list()
        for sub in data['subscriptions']:
            subscriptions.append(types.Subscription.from_dict(**sub))
        
        return subscriptions

    def new_user_subscription(self, unique_id: str, plan_unique_id: str) -> types.Subscription:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            "plan_unique_id": plan_unique_id
        }

        response = requests.post(
            url=self.__subscriptions_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Subscription.from_dict(**data)


    def _patch_user_subscription(self, unique_id: str, plan_unique_id: str, **kwars) -> types.Subscription:
        body = {
            "environment": self.environment_id,
            "unique_id": unique_id,
            "plan_unique_id": plan_unique_id,
            **kwars
        }

        response = requests.patch(
            url=self.__subscriptions_api_url,
            headers=self.headers,
            json=body,
            **self._requests_params
        )
        self._exception_raiser(response)

        data = json.loads(response.text)

        return types.Subscription.from_dict(**data)

    def set_subscription_status(self, unique_id: str, plan_unique_id: str, is_disabled: bool) -> types.Subscription:
        return self._patch_user_subscription(unique_id, plan_unique_id, is_disabled=is_disabled)

    def set_subscription_count_value(self, unique_id: str, plan_unique_id: str, count: int) -> types.Subscription:
        return self._patch_user_subscription(unique_id, plan_unique_id, count=count)
    
    def increment_subscription_count_value(self, unique_id: str, plan_unique_id: str) -> types.Subscription:
        return self._patch_user_subscription(unique_id, plan_unique_id, count_event='inc')

    def decrement_subscription_count_value(self, unique_id: str, plan_unique_id: str) -> types.Subscription:
        return self._patch_user_subscription(unique_id, plan_unique_id, count_event='dec')
