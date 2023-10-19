from typing import Optional

from typer.testing import CliRunner

from profitpulse.ui.typercli.main import app
from testrig.scenario import BaseScenario

runner = CliRunner(mix_stderr=False)


class CLIScenario(BaseScenario):
    """
    Builds scenarios up on the tests can be run.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> None:
        self._app = app

    def show_accounts(self):
        """
        Shows all the accounts and their current balance.
        """
        result = runner.invoke(self._app, ["accounts", "show"], catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec

        return result.stdout

    def open_account(self, account_name):
        """
        Opens a new account.
        """

        result = runner.invoke(
            self._app, ["accounts", "open", account_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec

    def close_account(self, account_name: str) -> None:
        """
        Closes an account.
        """
        result = runner.invoke(
            self._app, ["accounts", "close", account_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec
        assert result.stdout == "", result.stdout  # nosec

    def deposit(
        self, cent_amount: int, account_name: str, comment: Optional[str] = None
    ) -> None:
        args = ["deposit", str(cent_amount), account_name]
        if comment:
            args.append("--comment")
            args.append(comment)
        result = runner.invoke(self._app, args, catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec

    def withdraw(self, cent_amount: int, account_name: str) -> None:
        result = runner.invoke(
            self._app,
            ["withdraw", str(cent_amount), account_name],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec

    def report(self, seller: Optional[str] = None, month: Optional[int] = None):
        cmd = ["report"]
        if seller:
            cmd.append("--seller")
            cmd.append(seller)

        if month:
            cmd.append("--since")
            cmd.append(f"2023-{month}-01")

        result = runner.invoke(self._app, cmd, catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    @property
    def current_month(self) -> str:
        """
        Returns the current month of the imported transactions.
        """
        # This is one of the months defined in the fixture file comprovativo_cgd.csv
        return "8"

    def import_transactions(self, transactions_file: str, account_name: str):
        result = runner.invoke(
            self._app,
            ["import", str(transactions_file), account_name],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    def transfer(self, amount: int, from_account: str, to_account: str):
        result = runner.invoke(
            self._app,
            ["transfer", str(amount), from_account, to_account],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout
