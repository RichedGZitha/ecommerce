from django.urls import path
from . import views

urlpatterns = [
    path('get-product-public/<slug:pk>/', view=views.getProductForDisplay, name='get-product-public' ),
    path('get-product-admin/<slug:pk>/', view=views.getProductAdmin, name = 'get-product-admin'),
    path('edit-product/<slug:pk>/', view=views.editProductsManager, name='product'),
    path('create-product/', views.CreateProduct.as_view(), name='create-product'),
    path('create-review/', view=views.CreateProductReview.as_view(), name='create-product-review'),
    path('get-categories/<slug:pk>/', view=views.getProductcategories, name='get-categories'),
    path('get-reviews/<slug:pk>/', view=views.getProductReviews, name ='get-product-reviews'),
    path('get-products', view=views.getProductsQuery, name ='get-products'),
    path('edit-product-review/<slug:pk>/', view=views.editProductReviews, name = 'edit-product-review'),
    path('get-all-categories/', view=views.getAllCategories, name = 'get-all-categories'),
    path('update-product-categories/<slug:pk>/', view = views.updateProductCategories, name = 'update-product-categories'),
]
