from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django import forms

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page",
            "author": "Developed by: Santiago Gomez Rueda",
        })

        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "email": "onlinestore@storeonline.com",
            "address": "Street 123, City",
            "phone": "+1234567890",
        })
        return context

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price":900.0},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":1500.0},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":250.0},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":50.0},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            return redirect('home')

        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product
        }

        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    price = forms.FloatField(required=True, min_value=1)

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = {
                "id": str(len(Product.products) + 1),
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "price": form.cleaned_data["price"]
            }
            Product.products.append(new_product)
            return redirect('createdproduct')
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)

class ProductCreatedView(View):
    template_name = 'products/createdproduct.html'
    
    def get(self, request):
        viewData = {
            "title": "Product created",
            "subtitle": "Product created successfully",
        }
        return render(request, self.template_name, viewData)
