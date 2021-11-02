from django.urls import path
from . import views

urlpatterns = [
    path('get-product/<slug:pk>/', view=views.getProductForDisplay, name='get-single-product' ),
    path('product-manager/<slug:pk>/', view=views.editOrGetProductsManager, name='product'),
    path('create-product/', views.CreateProduct.as_view(), name='create-product'),
    path('create-review/', view=views.CreateProductReview.as_view(), name='create-product-review'),
    path('get-categories/<slug:pk>/', view=views.getProductcategories, name='get-categories'),
    path('get-reviews/<slug:pk>/', view=views.getProductReviews, name ='get-product-reviews'),
    path('get-products', view=views.getProductsQuery, name ='get-products'),
    path('edit-product-review/<slug:pk>/', view=views.editProductReviews, name = 'edit-product-review'),
    path('get-all-categories/', view=views.getAllCategories, name = 'get-all-categories'),
]
