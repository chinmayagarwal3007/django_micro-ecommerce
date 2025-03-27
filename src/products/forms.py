from django import forms # type: ignore
from .models import Product, ProductAttachment
from django.forms import modelformset_factory, inlineformset_factory # type: ignore


input_css_class = "form-control"
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price', 'long_description', 'short_description', 'image']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
              self.fields[field].widget.attrs['class'] = input_css_class
  

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image','name', 'handle', 'price', 'long_description', 'short_description']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
              self.fields[field].widget.attrs['class'] = input_css_class


class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ['file', 'is_free', 'is_active']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
              if field in ('is_free', 'is_active'):   
                continue
              self.fields[field].widget.attrs['class'] = input_css_class


ProductAttachmentModelFormSet = modelformset_factory(ProductAttachment, form = ProductAttachmentForm, fields=['file', 'is_free', 'is_active'],  extra=0, can_delete=True)

ProductAttachmentInlineFormSet = inlineformset_factory(Product, ProductAttachment, form = ProductAttachmentForm,formset=ProductAttachmentModelFormSet, fields=['file', 'is_free', 'is_active'],extra=0,can_delete=True)
