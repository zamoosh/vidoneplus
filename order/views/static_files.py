from .imports import *


@login_required
def static_files(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.image and order.image.path:
        path = order.image.path
        if os.path.exists(path):
            with open(path, 'rb') as f:
                content = f.read()
                f.close()
            mimetypes.init()
            mime = mimetypes.types_map['.' + path.split('.')[-1]]
            return HttpResponse(content, status=200, content_type=mime)
