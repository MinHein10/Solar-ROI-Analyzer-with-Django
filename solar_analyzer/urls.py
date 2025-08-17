from django.urls import path
# from . import views 
from .views import index, solar_form_view, form_success_view, login_view, logout_view, register_view, ProtectedView, solar_input_view, solar_detail_view, solar_step1_view, solar_step2_view, visualize_region, download_solar_detail_pdf

urlpatterns = [
    # path('',views.index)
    path('',index,name="index"),
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name="logout"),
    path('register/',register_view,name="register"),
    path('protected/',ProtectedView.as_view(),name='protected'),
    path('form/',solar_form_view,name="solar_form_view"),
    path('form/success/',form_success_view,name="form-success"),
    path('solar/input/', solar_input_view, name='solar_input'),
    path('solar/detail/<int:pk>/', solar_detail_view, name='solar_result_detail'),
    path('solar/input/step1/', solar_step1_view, name='solar_step1'),
    path('solar/input/step2/', solar_step2_view, name='solar_step2'),
    path('regiondata/',visualize_region, name='visualize_region'),
    path('solar/download/pdf/', download_solar_detail_pdf, name='download_solar_pdf'),
]
