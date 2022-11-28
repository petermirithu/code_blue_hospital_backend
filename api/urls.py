from django.urls import path
from . import views

urlpatterns = [          
    path('api/register_user', views.register_user),
    path('api/login_user', views.login_user),
    path('api/update_user', views.update_user),
    path('api/delete_user/<str:user_type>/<str:user_id>', views.delete_user),

    path('api/get_patients', views.get_patients),
    path('api/get_doctors', views.get_doctors),
    path('api/get_nurses', views.get_nurses),
    path('api/get_pharmacists', views.get_pharmacists),        
    path('api/get_revenue', views.get_revenue),        

    path('api/add_patient', views.add_patient),   

    path('api/get_admissions', views.get_admissions),  
    path('api/add_admissions', views.add_admissions),  
    path('api/update_admissions', views.update_admissions),  
    path('api/delete_admission/<str:admission_id>', views.delete_admission), 

    path('api/add_payment', views.add_payment),     
    path('api/get_payments', views.get_payments),     
    
]