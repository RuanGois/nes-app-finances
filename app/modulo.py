from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List
import time

class Transaction:

    def __init__(self, amount: float, category: str, description: str) -> None:
        self.amount = amount
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.category = category
        self.description = description

    def __str__(self) -> str:
        return f"Transação: {self.description}\nValor: R${self.amount} ({self.category})\nData: {self.date}"

    def update(self, **attributes):
        for chave, valor in attributes.items():
            if hasattr(self, chave):
                setattr(self, chave, valor)
            else:
                raise AttributeError(f"'{chave}' não é um atributo existente.")

class Account:

    def __init__(self, name: str, balance: float, client: "Client"):
        self.name = name
        self.balance = balance
        self.transactions: List[Transaction] = []
        self.cliente = client

    def add_transaction(self, amount:float, category: int, description: str ="") -> Transaction:
        self.balance -= amount
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        print(f"Transação no valor de {amount} realizada com sucesso. Saldo atual: {self.balance}.")

    def get_transactions(self, start_date: datetime = None, end_date: datetime = None, category: int = None) -> List[Transaction]:
        for transaction in self.transactions:
            print("------------\n",transaction, "\n------------")


class Investment:

    def __init__(self, type: str, initial_amount: float, rate_of_return: float, client: "Client"):
        self.type = type
        self.initial_amount = initial_amount
        self.date_purchase = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.rate_of_return = rate_of_return
        self.cliente = client
        self.last_update = self.date_purchase
        self.current_value = initial_amount

    def calculate_value(self) -> float:
        now = datetime.now()
        months_passed = relativedelta(now, self.last_update).months + \
                        (relativedelta(now, self.last_update).years * 12)
        if months_passed > 0:
            for i in range(months_passed):
                self.current_value *= (1 + self.rate_of_return)
            self.last_update += relativedelta(months=months_passed)
        return self.current_value

    def sell(self, account: Account):
        valor_final = self.calculate_value()
        account.balance += valor_final
        print(f"Investimento vendido! Valor de R${valor_final} depositado na conta '{account.name}'.")

class Client:

    def __init__(self, name: str):
        self.name = name
        self.accounts: List[Account] = []
        self.investments: List[Investment] = []
    
    def add_account(self, account_name: str, balance) -> Account:
        nova_conta = Account(account_name, balance, self)
        print(f"\nNova conta criada com sucesso!\nNome da conta: {account_name}.")
        self.accounts.append(nova_conta)

    def add_investment(self, account_name) -> None:
        novo_investimento = Investment("Jogo do Tigrinho", 100.00, 0.1, self)
        print(f"\nNovo investimento iniciado!\nConta: {account_name}\nTipo de investimento: {novo_investimento.type}\nValor investido: {novo_investimento.initial_amount}")
        self.investments.append(novo_investimento)
    
    def get_net_worth(self) -> float:
        valor_total = 0
        for conta in self.accounts:
            valor_total += conta.balance
        for investimento in self.investments:
            valor_total += investimento.calculate_value()
        print(f"Valor total nas contas de {self.name} (saldo e investimentos): {valor_total}.")

# objeto = Transaction(500, "pix", "pagamento da energia")
cliente1 = Client("Ruan")
conta1 = Account("ruru", 500, cliente1)
cliente1.add_account(conta1, 500)
# cliente1.add_account("Conta 2 - Ruan")
investimento1 = Investment("Renda Fixa", 100, 0.05, cliente1)
investimento1.last_update = datetime(2024, 10, 1)
print(cliente1.accounts, cliente1.investments)
print(investimento1.calculate_value())
investimento1.sell(conta1)

cliente1.get_net_worth()

# print(cliente1.investments)
# conta = Account("Conta do Ruan", 700, cliente1)

# conta.add_transaction(200, 1)
# time.sleep(3)
# conta.add_transaction(50, 2)
# time.sleep(1)
# conta.get_transactions()

# for i in conta.transactions:
#     print(i)