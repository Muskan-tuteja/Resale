from django.urls import path
from mysite import views

app_name = "mysite"

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('uservalid/',views.uservalid,name='uservalid'),
    path('signin/',views.signin,name="signin"),
    path('post_add/',views.post_add,name="post_add"),
    path('single_product/',views.single_product,name="single_product"),
    path('categories',views.categories,name="categories"),
    path('all-classifieds',views.all_classifieds,name="all-classifieds"),
    path('products',views.products,name="products"),
    path('contact',views.contact,name="contact"),
    path('uslogout',views.uslogout,name="uslogout"),
    path('myadds',views.myadds,name="myadds"),
    path('delete_add',views.delete_add,name="delete_add"),
]