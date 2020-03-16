"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from app_shop import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),


    path('', views.BaseView.as_view(), name="home"),
    path('categories/', views.ShowCategoriesView.as_view(), name="categories"),
    path('add-category/', views.AddCategoryView.as_view(), name="add_new_category"),
    path('products/<int:category_id>', views.ShowProductsByCategoryIdView.as_view(),
         name="show_products_in_category"),
    path('add-product/', views.AddProductView.as_view(), name="add_new_product"),
    path('show-product/<int:id>/', views.ShowProductInfoView.as_view(), name="product_info"),
    path('show-user/<int:id>', views.ShowUserView.as_view(), name="show_user"),
    path('users-list/', views.UsersListView.as_view(), name="users_list"),
    path('products-list/', views.AllProductsListView.as_view(), name="products_list"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('search/', views.SearchView.as_view(), name="search"),
]
