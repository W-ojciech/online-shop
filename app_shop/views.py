from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from app_shop.forms import AddCategoryForm, AddProductForm, AddProductToBasketForm, RemoveCategoryForm, AddCommentForm
from app_shop.models import Category, Product, Basket, ProductInBasket, Comment
from django.contrib.auth.mixins import PermissionRequiredMixin



class BaseView(View):
    def get(self, request):
        return render(request, "base.html")



class ShowCategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all().order_by('votes', 'added_date')
        return render(request, "show_categories.html", {"categories": categories, "products": products})
    def post(self, request):
        form = RemoveCategoryForm(request.POST)
        if form.is_valid():
            category_id = form.cleaned_data['category']
            category = Category.objects.get(pk=category_id)
            category.delete()
        return redirect('/categories/')




class AddCategoryView(View, PermissionRequiredMixin):
    permission_required = ('category.add_category')
    def get(self, request):
        if not request.user.is_superuser:
            raise Exception('Nie masz uprawnien')
        form = AddCategoryForm()
        return render(request, "add_category.html", {"form": form})
    def post(self, request):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            new_category = Category()
            new_category.name = name
            new_category.description = description
            new_category.save()
            return redirect('/categories/')



class ShowProductsByCategoryIdView(View):
    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category_id=category_id)
        form = AddProductToBasketForm()
        return render(request, "show_products_by_category_id.html", {"category": category,
                                        "products": products, "form": form})
    def post(self, request, category_id):
        form = AddProductToBasketForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product']
            basket = Basket.objects.get_or_create(customers=request.user)[0]
            basket.quantity += 1
            basket.save()
            product = Product.objects.get(pk=product_id)
            basket.add_product(product)
        return redirect(f"/products/{category_id}")



class AddProductView(View, PermissionRequiredMixin):
    permission_required = ('product.add_product')
    def get(self, request):
        if not request.user.is_superuser:
            raise Exception('Nie masz uprawnien')
        form = AddProductForm()
        return render(request, "add_product.html", {"form": form})
    def post(self, request):
        form = AddProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            quantity = form.cleaned_data["quantity"]
            price = form.cleaned_data["price"]
            category_id = form.cleaned_data["category"]
            new_product = Product()
            new_product.name = name
            new_product.description = description
            new_product.quantity = quantity
            new_product.price = price
            new_product.category_id = int(category_id)
            new_product.save()
        return redirect('/products-list/')




class RemoveProductView(View):
    def get(self, request, id):
        product_to_remove = Product.objects.get(pk=id)
        product_to_remove.delete()
        return render(request, "show_products_by_category_id.html")



class ShowProductInfoView(View):
    def get(self, request, id):
        product = Product.objects.get(pk=id)
        form = AddProductToBasketForm()
        form2 = AddCommentForm()
        user = User.objects.get(pk=request.user.id)
        comments = Comment.objects.filter(customer_id=user, product_id=product)
        return render(request, "show_product_info.html", {"product": product, "form": form,
                                                          "form2": form2, "comments": comments})
    def post(self, request, id):
        form = AddProductToBasketForm(request.POST)
        # form2 = AddCommentForm(request.POST)
        # product = Product.objects.get(pk=id)
        if form.is_valid():
            option = request.POST.get('submit')
            if option == "Add to basket":
                product_id = form.cleaned_data['product']
                basket = Basket.objects.get_or_create(customers=request.user)[0]
                basket.quantity += 1
                basket.save()
                product = Product.objects.get(pk=product_id)
                basket.add_product(product)
            elif option == "Delete":
                product_id = form.cleaned_data['product']
                product = Product.objects.get(pk=product_id)
                product.delete()
            elif option == "Add comment":
                product_id = request.POST.get('product')
                user = User.objects.get(pk=request.user.id)
                text = request.POST.get('text')
                new_comment = Comment()
                new_comment.text = text
                new_comment.product_id = product_id
                new_comment.customer = user
                new_comment.save()
        return redirect(f"/show-product/{id}/")



class AllProductsListView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        return render(request, "products_list.html", {"categories": categories, "products": products})



class ShowUserView(View):
    def get(self, request, id):
        user = User.objects.get(pk=id)
        basket = Basket.objects.get(customers_id=id)
        form = AddProductToBasketForm()
        product_in_basket = ProductInBasket.objects.all()
        sum_price = 0
        for i in product_in_basket:
            sum_price += round((i.product_id.price * i.volume_of_product), 3)
        return render(request, "show_user.html", {"user_": user, "basket": basket,
                                                  "form": form, "sum_price": sum_price,
                                                    "product_in_basket": product_in_basket})
    def post(self, request, id):
        basket = Basket.objects.get(customers=request.user)
        form = AddProductToBasketForm(request.POST)
        if request.POST.get('submit') == "Clear all":
            basket.products.clear()
            basket.quantity = 0
            basket.save()
            return redirect(f'/show-user/{id}')
        if form.is_valid():
            option = request.POST.get('submit')
            if option == "Remove from basket":
                product_id = form.cleaned_data['product']
                product = Product.objects.get(pk=product_id)
                basket.remove_product(product)
            elif option == "Clear all":
                basket.products.clear()
                basket.quantity = 0
                basket.save()
        return redirect(f'/show-user/{id}')



class UsersListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users_list.html", {"users": users})


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")


class SearchView(View):
    def get(self, request):
        name = request.GET.get('search', '')
        result = Product.objects.filter(name__icontains=name)
        return render(request, "search.html", {"result": result})
