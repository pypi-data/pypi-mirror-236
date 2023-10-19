import typing

from profitpulse.account import Account
from profitpulse.account_name import AccountName
from profitpulse.application.deposit_into_account import AccountDoesNotExistError


class GatewayTransactions(typing.Protocol):
    """
    Gateway to transactions.
    """

    def __iter__(self):
        pass  # pragma: no cover


class RepositoryTransactions(typing.Protocol):
    """
    Repository to transactions.
    """

    def append(self, transaction, account_name: AccountName):
        pass  # pragma: no cover


class ImportTransactionsRequest(typing.Protocol):
    @property
    def account_name(self) -> AccountName:
        ...  # pragma: no cover


class Accounts(typing.Protocol):
    def __getitem__(self, account_name: AccountName) -> Account:
        ...  # pragma: no cover


class ServiceImportTransactions:
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: GatewayTransactions,
        transactions: RepositoryTransactions,
        accounts: Accounts,
    ):
        self._transactions_gateway = transactions_gateway
        self._transactions = transactions
        self._accounts = accounts

    def execute(self, request: ImportTransactionsRequest):
        try:
            _ = self._accounts[request.account_name]
        except KeyError:
            raise AccountDoesNotExistError

        for transaction in self._transactions_gateway:
            self._transactions.append(transaction, request.account_name)
