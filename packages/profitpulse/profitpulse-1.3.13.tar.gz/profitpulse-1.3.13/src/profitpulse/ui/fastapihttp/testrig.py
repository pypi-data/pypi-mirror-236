# from typing import Optional

# import httpx


# from testrig.scenario import BaseScenario


# class FastAPIScenario(BaseScenario):
#     def __init__(self):
#         self._hostname = "127.0.0.1"
#         self._port = "8080"

#     def show_accounts(self):
#         """
#         Shows all the accounts and their current balance.
#         """

#         r = httpx.get(f"http://{self._hostname}:{self._port}/api/1/accounts")
#         assert r.status_code == 200, r.text  # nosec
#         return r.json()

#     def open_account(self, account_name):
#         """
#         Opens a new account.
#         """

#         r = httpx.post(
#             f"http://{self._hostname}:{self._port}/api/1/accounts",
#             json={"name": account_name},
#         )
#         assert r.status_code == 200, r.text  # nosec
#         assert r.text == "", r.text  # nosec

#     def close_account(self, account_name: str) -> None:
#         """
#         Closes an account.
#         """
#         r = httpx.delete(
#             f"http://{self._hostname}:{self._port}/api/1/accounts/{account_name}",
#         )
#         assert r.status_code == 200, r.text  # nosec
#         assert r.text == "", r.text  # nosec

#     def deposit(
#         self, cent_amount: int, account_name: str, comment: Optional[str] = None
#     ) -> None:
#         r = httpx.post(
#             f"http://{self._hostname}:{self._port}/api/1/accounts/{account_name}/deposit",
#             json={"amount": cent_amount, "comment": comment},
#         )
#         assert r.status_code == 200, r.text  # nosec

#     def withdraw(self, cent_amount: int, account_name: str) -> None:
#         r = httpx.post(
#             f"http://{self._hostname}:{self._port}/api/1/accounts/{account_name}/withdraw",
#             json={"amount": cent_amount},
#         )
#         assert r.status_code == 200, r.text  # nosec

#     def report(self, seller: Optional[str] = None):
#         if seller:
#             r = httpx.get(
#                 f"http://{self._hostname}:{self._port}/api/1/transactions?seller={seller}"
#             )
#         else:
#             r = httpx.get(f"http://{self._hostname}:{self._port}/api/1/transactions")
#         assert r.status_code == 200, r.text  # nosec
#         return r.json()

#     def import_transactions(self, transactions_file: str, account_name: str):
#         r = httpx.post(
#             f"http://{self._hostname}:{self._port}/api/1/accounts/{account_name}/import",
#             files={"transactions_file": open(transactions_file, "rb")},
#         )
#         assert r.status_code == 200, r.text  # nosec

#     def show_transactions(self, account_name: str):
#         r = httpx.get(
#             f"http://{self._hostname}:{self._port}/api/1/accounts/{account_name}/transactions"
#         )
#         assert r.status_code == 200, r.text  # nosec
#         return r.json()
