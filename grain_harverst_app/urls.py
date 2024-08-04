from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert/', views.NewUser, name='inserts'),
    path('user/<int:user_id>/', views.RetrieveUser, name='user_detail'),
    path('user/<int:user_id>/update/', views.UpdateUser, name='update_user'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dash, name='dashboardd'),
    path('signup/', views.insertt, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('predict_rice_quality/', views.predict_rice_quality, name='predict_rice_quality'),
    path('predict_maize_quality/', views.predict_maize_quality, name='predict_maize_quality'),
    path('predict_wheat_quality/', views.predict_wheat_quality, name='predict_wheat_quality'),
    path('store_rice/', views.store_rice, name='store_rice'),
    path('store_maize/', views.store_maize, name='store_maize'),
    path('store_wheat/', views.store_wheat, name='store_wheat'),
    path('supplier_dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('stockkeeper_dashboard/', views.stockkeeper_dashboard, name='stockkeeper_dashboard'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory_store/', views.inventory_list_storekeeper, name='inventory_list_storekeeper'),
    path('inventory/createe/', views.inventory_create, name='inventory_create'),
    path('inventory/update/<int:pk>/', views.inventory_update, name='inventory_update'),
    path('inventory/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('get_user_name/<int:user_id>/<str:role>/', views.get_user_name, name='get_user_name'),
    path('inventory_received/update/<int:pk>/', views.inventory_update_recieved, name='inventory_update_recieved'),
    
    path('list/', views.chat_message_list, name='chat_message_list'),
    path('create/', views.chat_message_create, name='chatmessage_create'),
    path('<int:pk>/', views.chat_message_detail, name='chatmessage_detail'),
    path('<int:pk>/update/', views.chat_message_update, name='chatmessage_update'),

    path('lists/', views.chat_message_list_farmer, name='chat_message_list_farmer'),
    path('creates/', views.chat_message_create_farmer, name='chatmessage_create_farmer'),
    path('<int:pk>/', views.chat_message_detail, name='chatmessage_detail'),
    path('<int:pk>/updatee/', views.chat_message_update_famer, name='chatmessage_update_farmer'),

    path('contact/', views.contact_us, name='contact'),
    path('success/', views.success_view, name='success'),
    
]

