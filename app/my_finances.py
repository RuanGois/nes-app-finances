from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List

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

    def add_investment(self, type: str, initial_amount: float, rate_of_return: float, account_name: str, last_update: datetime) -> None:
        novo_investimento = Investment(type, initial_amount, rate_of_return, self)
        novo_investimento.last_update = last_update
        print(f"\nNovo investimento iniciado!\nConta: {account_name}\nTipo de investimento: {novo_investimento.type}\nValor investido: {novo_investimento.initial_amount}")
        self.investments.append(novo_investimento)
    
    def get_net_worth(self) -> float:
        valor_total = 0
        for conta in self.accounts:
            valor_total += conta.balance
        for investimento in self.investments:
            valor_total += investimento.calculate_value()
        return valor_total
    
    def generate_report(self):
        print(
            f"\n*********************\nRelatório financeiro:\n\n*Cliente*: {self.name}"
            f"\n*Contas*: {[(account.name, account.balance) for account in self.accounts]}."
            f"\n*Investimentos*: {[(investment.type, investment.date_purchase) for investment in self.investments]}"
            f"\n*Saldo total do cliente*: {self.get_net_worth()}"
            "\n*********************"
            )
    def future_report(self):
        valor_investido = 0
        valor_rendido = 0
        for investment in self.investments:
            valor_investido += investment.initial_amount
            valor_rendido += (investment.current_value - investment.initial_amount)
        print(
            "\n=====================\nRelatório de investimentos:"
            f"\nQuantidade de investimentos ativos: {len(self.investments)}"
            f"\nValot total investido: {valor_investido}"
            f"\nRendimento dos investimentos: {valor_rendido}"
            "\n====================="
        )
