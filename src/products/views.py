from django.shortcuts import render, redirect,get_object_or_404 # type: ignore
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormSet
from .models import Product, ProductAttachment
import mimetypes
from django.http import FileResponse, HttpResponseBadRequest # type: ignore
import os

# Create your views here.

def product_create_view(request):
    context = {}
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
              obj.user = request.user
              obj.save()
              return redirect('products:manage', slug=obj.handle)
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

def product_manage_detail_view(request, slug=None):
  obj = get_object_or_404(Product, handle=slug)
  print(slug)
  context = {"object": obj}
  attachments = obj.attachments.all()
  for attachment in attachments:
        attachment.file_name = os.path.basename(attachment.file.name)
  is_manager = False
  if request.user.is_authenticated:
    is_manager = obj.user == request.user
    form = None
    if not is_manager:
       return HttpResponseBadRequest("You are not allowed to see this page")

    if request.method == "POST":
        form = ProductUpdateForm(request.POST, request.FILES, instance=obj)
        formset = ProductAttachmentInlineFormSet(request.POST, request.FILES,queryset=attachments)
        if form.is_valid() and formset.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            formset.save(commit=False)
            for _form in formset:
              is_delete = _form.cleaned_data.get('DELETE')
              try:
                 attachment_obj = _form.save(commit=False)
              except:
                  attachment_obj = None
              if is_delete:
                print("Deleting")
                if attachment_obj is not None:
                  print("Deleting-1")
                  if attachment_obj.pk:
                    attachment_obj.delete()
              else:
                if attachment_obj is not None:
                  attachment_obj.product = obj
                  attachment_obj.save()
            return redirect('products:manage', slug=obj.handle)               
    else:
      form = ProductUpdateForm(instance=obj)
      formset = ProductAttachmentInlineFormSet(queryset=attachments)
    context['form'] = form
    context['formset'] = formset
  return render(request, 'products/manager.html', context) 


def product_detail_view(request, slug=None):
  obj = get_object_or_404(Product, handle=slug)
  attachments = obj.attachments.all()
  for attachment in attachments:
        attachment.file_name = os.path.basename(attachment.file.name)
  context = {"object": obj, "attachments": attachments}
  is_owner = False
  if request.user.is_authenticated:
    is_owner = True
    context['is_owner'] = is_owner
  return render(request, 'products/detail.html', context) 

def product_attachment_download_view(request, slug=None, pk=None):
   attachment = get_object_or_404(ProductAttachment, product__handle = slug, pk = pk)
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
