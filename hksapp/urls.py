from django.contrib import admin
from django.urls import path,include
from.import views

urlpatterns = [
    path('',views.home),
    path('login',views.login),
    path('registration',views.registration),






    # ***ADMIN****
path('admin_home',views.adminhome),
path('admin_add_ward',views.admin_add_ward,name='addward'),
path('admin_delete_ward/<id>',views.admin_delete_ward),
path('admin_add_hks',views.admin_add_hks,name='admin_manage_hks'),
path('admin_update_hks/<id>',views.admin_update_hks),
path('admin_delete_hks/<id>',views.admin_delete_hks),
path('admin_assign_ward',views.admin_assign_ward,name='admin_assign_ward'),
path('admin_delete_assignment/<id>',views.admin_assign_ward),
path('adminadd_itofficer',views.admin_add_itofficer,name='adminadd_itofficer'),
path('admin_update_itofficer/<id>',views.admin_update_itofficer),
path('admin_delete_itofficer/<id>',views.admin_delete_itofficer),
path('admin_view_user',views.admin_view_user),
path('admin_view_complaints',views.admin_view_complaints,name='admin_view_complaints'),
path('admin_reply_complaint/<id>',views.admin_reply_complaint),
path('user_custom_waste_payment/<id>', views.user_custom_waste_payment, name='user_custom_waste_payment'),




    # ***USER****
path('user_home',views.User_home),
path('user_add_waste',views.user_add_waste,name='user_add_waste'),
path('user_send_complaint',views.user_send_complaint),
path('user_view_notification',views.user_view_notification),
path('user_view_recycle_product', views.user_view_recycle_product, name='user_view_recycle_product'),
path('user_view_cart/<id>',views.add_to_cart,name='user_view_cart'),
path('user_view_cart',views.user_view_cart,name='user_view_cart'),
path('remove_from_cart/<id>', views.remove_cart, name='remove_from_cart'),
path('make_payment/<id>', views.make_payment, name='make_payment'),
path('user_order_history', views.user_order_history, name='user_order_history'),
path('user_send_custom_waste', views.user_send_custom_waste_request, name='user_send_custom_waste'),
path('user_send_publicwaste', views.user_send_public_waste, name='user_send_public_waste'),




    # ***it officer****


path('it_officer_home',views.it_officer_home),
path('user_send_complaint',views.user_send_complaint,name='user_send_complaint'),
path('it_send_notification',views.it_send_notification,name='it_send_notification'),
path('it_office_view_hks',views.it_office_view_hks),
path('it_officer_view_complaints',views.it_officer_view_complaints,name='it_officer_view_complaints'),
path('it_manage_products', views.it_manage_products, name='it_manage_products'),
path('it_delete_product/<id>', views.it_delete_product, name='it_delete_product'),
path('it_update_product/<id>', views.it_update_product, name='it_update_product'),
path('hks_update_custom_status/<id>', views.hks_update_custom_waste, name='hks_update_custom_status'),
path('hks_view_notification_it',views.hks_view_notification_it),
path('it_officer_reply_complaints/<id>',views.it_officer_reply_complaint),
path('itofficer_wastereport',views.itofficer_wastereport),
path('itofficer_payment',views.itofficer_payment),

    

    # ***HKS ****
    path('hks_normal_home',views.hks_home_normal,name='hks_normal_home'),
    path('hks_custom_home',views.hks_home_custom,name='hks_custom_home'),
    path('hks_delivery_home',views.hks_home_delivery,name='hks_delivery_home'),
    path('hks_normal_send_complaint',views.hks_normal_send_complaint,name='hks_normal_send_complaint'),
    path('hks_custom_send_complaint',views.hks_custom_send_complaint,name='hks_custom_send_complaint'),
    path('hks_view_custom_requests', views.hks_custom_view_custom_waste, name='hks_view_custom_requests'),
    path('hks_view_public_waste', views.hks_custom_view_public_waste, name='hks_view_public_waste'),
    path('hks_verify_public_waste/<id>', views.hks_custom_approve_public_waste, name='hks_verify_public_waste'),
    path('hks_Custom_view_notification',views.hks_Custom_view_notification),
    path('hks_delivery_view_order', views.hks_delivery_view_order, name='hks_delivery_view_order'),
    path('hks_delivery_update_order/<id>', views.hks_delivery_update_order, name='hks_delivery_update_order'),  
    path('hks_custom_send_notification', views.hks_custom_send_notification, name='hks_custom_send_notification'),
    path('user_view_hks_notiication',views.user_view_hks_notification),
    path('hks_view_waste',views.hks_view_waste,name='hks_view_waste'),
    path('hks_update_waste/<id>',views.hks_update_waste,name='hks_view_waste'),
    path('hks_delivery_send_complaint',views.hks_delivery_send_complaint,name='hks_delivery_send_complaint'),
    path('hks_delivery_payment_confirmation/<id>',views.hks_delivery_payment_confirmation),




]
