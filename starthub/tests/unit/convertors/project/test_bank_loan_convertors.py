from django.test import SimpleTestCase
from unittest.mock import Mock
from dataclasses import dataclass

from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.project.bank_loan import (
    BankLoanOrganizationName,
    LoanAmount,
    LoanTerms,
    ProjectBankLoanCreateCommand,
    ProjectBankLoanUpdateCommand,
)
from presentation.request_converters.project.bank_loan import (
    request_to_bank_loan_create_command,
    request_to_bank_loan_update_command,
)


@dataclass
class ValidBankLoanData:
    organization_name = "Test Bank"
    amount = 100000
    terms = "5 years at 3.5% interest"

    organization_name_field = "organization_name"
    amount_field = "amount"
    terms_field = "terms"

    def to_dict(self):
        return {
            self.organization_name_field: self.organization_name,
            self.amount_field: self.amount,
            self.terms_field: self.terms,
        }


class TestRequestToBankLoanCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidBankLoanData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectBankLoanCreateCommand(
            organization_name=BankLoanOrganizationName(value=self.valid_dataclass.organization_name),
            amount=LoanAmount(value=self.valid_dataclass.amount),
            terms=LoanTerms(value=self.valid_dataclass.terms)
        )
        result = request_to_bank_loan_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_organization_name(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.organization_name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_bank_loan_create_command(request)

    def test_missing_amount(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.amount_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_bank_loan_create_command(request)

    def test_missing_terms(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.terms_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_bank_loan_create_command(request)


class TestRequestToBankLoanUpdateCommand(SimpleTestCase):

    def setUp(self):
        self.valid_dataclass = ValidBankLoanData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectBankLoanUpdateCommand(
            organization_name=BankLoanOrganizationName(value=self.valid_dataclass.organization_name),
            amount=LoanAmount(value=self.valid_dataclass.amount),
            terms=LoanTerms(value=self.valid_dataclass.terms)
        )
        result = request_to_bank_loan_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_organization_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.organization_name_field: self.valid_dataclass.organization_name}

        expected = ProjectBankLoanUpdateCommand(
            organization_name=BankLoanOrganizationName(value=self.valid_dataclass.organization_name),
            amount=None,
            terms=None
        )

        result = request_to_bank_loan_update_command(request)

        self.assertEqual(expected, result)

    def test_valid_data_with_amount_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.amount_field: self.valid_dataclass.amount}

        expected = ProjectBankLoanUpdateCommand(
            organization_name=None,
            amount=LoanAmount(value=self.valid_dataclass.amount),
            terms=None
        )

        result = request_to_bank_loan_update_command(request)

        self.assertEqual(expected, result)

    def test_valid_data_with_terms_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.terms_field: self.valid_dataclass.terms}

        expected = ProjectBankLoanUpdateCommand(
            organization_name=None,
            amount=None,
            terms=LoanTerms(value=self.valid_dataclass.terms)
        )

        result = request_to_bank_loan_update_command(request)

        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectBankLoanUpdateCommand(
            organization_name=None,
            amount=None,
            terms=None
        )

        result = request_to_bank_loan_update_command(request)

        self.assertEqual(expected, result)

