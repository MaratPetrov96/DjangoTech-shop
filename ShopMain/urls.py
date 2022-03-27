from . import views
from django.urls import path

urlpatterns = [
    path('',views.main,name='main'),
    path('category/<slug:title>/<slug:sub>',views.SubcategoryView.as_view(),name='subcategory'),
    path('category/<slug:title>/<slug:sub>/price=<int:min_>_<int:max_>',views.SubcategoryView.as_view(),name='subcategory'),
    path('category/<slug:title>/<slug:sub>/price=<int:min_>_<int:max_>/<int:pg>',views.SubcategoryView.as_view(),name='subcategory'),
    path('category/<slug:title>/<slug:sub>/<int:pg>',views.SubcategoryView.as_view(),name='subcategory_page'),
    path('item/<int:pk>',views.ItemView.as_view(),name='item'),
    path('review/<int:pk>',views.review,name='review'),
    path('search',views.search),
    path('search/query=<str:query>',views.search_res,name='search'),
    path('search/query=<str:query>/page=<int:pg>',views.search_res,name='search'),
    path('search/query=<str:query>/price=<int:min_>_<int:max_>',views.search_res,name='search_price'),
    path('search/query=<str:query>/price=<int:min_>_<int:max_>/page=<int:pg>',views.search_res,name='search_price'),
    path('about',views.about,name='about'),
    path('add/<int:pk>',views.add),
    path('busket',views.BusketView.as_view(),name='busket'),
    path('delete/<int:pk>',views.delete_busket,name='delete'),
    path('order',views.order,name='order'),
    path('pay/<slug:summ>',views.pay,name='pay'),
    ]
