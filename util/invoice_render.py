from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template


class Render:

    @staticmethod
    def view(template_src, context_dict):
        pass
        # template = get_template(template_src)
        # html = template.render(context_dict)
        # result = BytesIO()
        # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        # if not pdf.err:
        #     return HttpResponse(result.getvalue(), content_type='application/pdf')
        # return None
