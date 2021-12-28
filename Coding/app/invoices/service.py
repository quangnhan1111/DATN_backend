from invoices.models import Invoice
from invoices.repository import InvoiceRepository


class InvoiceService():
    def __init__(self):
        self.invoice_repository = InvoiceRepository()

    def getInvoicesByCustomer(self):
        invoices = self.invoice_repository.getInvoicesByCustomer()
        return invoices

    def getInvoicesByEmployee(self):
        invoices = self.invoice_repository.getInvoicesByEmployee()
        return invoices

    def getInvoicesForOneEmployeeStatus(self, pk):
        invoices = self.invoice_repository.getInvoicesForOneEmployeeStatus(pk)
        return invoices

    def getInvoicesForOneCustomerStatus(self, pk):
        invoices = self.invoice_repository.getInvoicesForOneCustomerStatus(pk)
        return invoices

    def getInvoicesForEmployeeStatus(self):
        invoices = self.invoice_repository.getInvoicesForEmployeeStatus()
        return invoices

    def getInvoicesForCustomerStatus(self):
        invoices = self.invoice_repository.getInvoicesForCustomerStatus()
        return invoices

    def showOneInvoices(self, pk):
        invoices = self.invoice_repository.showOneInvoices(pk)
        return invoices

    def showOneInvoicesAndShowEmployee(self, pk):
        invoices = self.invoice_repository.showOneInvoicesAndShowEmployee(pk)
        return invoices

    def showOneInvoicesAndShowCustomer(self, pk):
        invoices = self.invoice_repository.showOneInvoicesAndShowCustomer(pk)
        return invoices

    def showInvoicesByIdEmployee(self, pk):
        invoices = self.invoice_repository.showInvoicesByIdEmployee(pk)
        return invoices

    def showInvoicesByIdCustomer(self, pk):
        invoices = self.invoice_repository.showInvoicesByIdCustomer(pk)
        return invoices


    def store(self, request):
        result = self.invoice_repository.store(request)
        return result

    def update(self, pk, request):
        if Invoice.objects.filter(deleted_at=False, id=pk).exists():
            invoice = Invoice.objects.get(pk=pk)
            result = self.invoice_repository.update(invoice, request)
            return result
        return None

    def destroy(self, pk):
        if Invoice.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Invoice.objects.filter(deleted_at=False, id=pk).exists():
            result = self.invoice_repository.destroy(pk)
            return result
        return None

