from django.http import HttpResponse
from django.conf import settings
from django.views.generic import DetailView
import pdfkit
from order.models import Order


class GenerateInvoiceView(DetailView):
    model = Order
    template_name = 'invoice.html'


def generate_view(request, id):  # Create a URL of our project and go to the template route
    if settings.PDF_KIT_BIN:
        projectUrl = request.get_host() + '/core/system/generate-invoice/{}'.format(id)
        pdf = pdfkit.from_url(projectUrl, False, configuration=pdfkit.configuration(
            wkhtmltopdf=settings.PDF_KIT_BIN), options={'encoding': "UTF-8", 'quiet': ''})
        # Generate download
        response = HttpResponse(pdf, content_type='application/pdf')
        if settings.PDF_KIT_DOWNLOAD:
            response['Content-Disposition'] = 'attachment; filename="invoice-{}.pdf"'.format(id)

        return response

    return HttpResponse('No Config')
