from django.shortcuts import render, redirect,get_object_or_404 # type: ignore
from .forms import ProductForm, ProductUpdateForm
from .models import Product, ProductAttachment
import mimetypes
from django.http import FileResponse, HttpResponseBadRequest # type: ignore

# Create your views here.

def product_create_view(request):
    context = {}
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
              obj.user = request.user
              obj.save()
              return redirect('products:create')
            else:
              form.add_error("User must be logged in")
    else:
      form = ProductForm()
    context['form'] = form
    return render(request, 'products/create.html', context) 


def product_list_view(request):
    context = {}
    context['object_list'] = Product.objects.all()
    return render(request, 'products/list.html', context)

def product_detail_view(request, slug=None):
  obj = get_object_or_404(Product, handle=slug)
  context = {"object": obj}
  is_owner = False
  if request.user.is_authenticated:
    is_owner = obj.user == request.user
    form = None
    if is_owner:
      if request.method == "POST":
          form = ProductUpdateForm(request.POST, request.FILES, instance=obj)
          if form.is_valid():
              obj = form.save(commit=False)
              obj.user = request.user
              obj.save()
              #return redirect('products:create')
      else:
        form = ProductUpdateForm(instance=obj)
      context['form'] = form
  return render(request, 'products/detail.html', context) 

def product_attachment_download_view(request, slug=None):
   attachment = ProductAttachment.objects.all().first()
   can_download = attachment.is_free or False
   if request.user.is_authenticated:
       can_download = True
   if not can_download:
       return HttpResponseBadRequest("You can't download this file")
   file = attachment.file.open(mode='rb')
   filename = attachment.file.name
   content_type, _ = mimetypes.guess_type(filename)
   response = FileResponse(file)
   response['Content-Type'] = content_type or 'application/octet-stream'
   response['Content-Disposition'] = f'attachment; filename={filename}'
   return response
