from django.urls import path
from django.contrib import admin
from orders import views as my_order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # ─── Orders ───────────────────────────────────────────────────────────────
    path('',                              my_order.index_order,      name='home'),
    path('orders/',                       my_order.index_order,      name='index_order'),
    path('orders/new/',                   my_order.new_order,        name='new_order'),
    path('orders/<int:order_id>/',        my_order.show_order,       name='show_order'),
    path('orders/edit/<int:order_id>/',   my_order.edit_order,       name='edit_order'),
    path('orders/delete/<int:order_id>/', my_order.destroy_order,    name='destroy_order'),

    # Inline OrderItem management (optional)
    path('orders/<int:order_id>/items/new/',    my_order.new_order_item,      name='new_order_item'),
    path('orders/items/edit/<int:item_id>/',    my_order.edit_order_item,     name='edit_order_item'),
    path('orders/items/delete/<int:item_id>/',  my_order.destroy_order_item,  name='destroy_order_item'),

    # ─── Products ─────────────────────────────────────────────────────────────
    path('products/',                        my_order.index_product,    name='index_product'),
    path('products/new/',                    my_order.new_product,      name='new_product'),
    path('products/edit/<int:product_id>/',  my_order.edit_product,     name='edit_product'),
    path('products/delete/<int:product_id>/',my_order.destroy_product,  name='destroy_product'),

    # ─── Categories ──────────────────────────────────────────────────────────
    path('categories/',                      my_order.index_category,   name='index_category'),
    path('categories/new/',                  my_order.new_category,     name='new_category'),
    path('categories/edit/<int:category_id>/',   my_order.edit_category,     name='edit_category'),
    path('categories/delete/<int:category_id>/', my_order.destroy_category,  name='destroy_category'),

    # ─── Tables ─────────────────────────────────────────────────────────────
    path('tables/',                         my_order.index_table,      name='index_table'),
    path('tables/new/',                     my_order.new_table,        name='new_table'),
    path('tables/edit/<int:table_id>/',     my_order.edit_table,       name='edit_table'),
    path('tables/delete/<int:table_id>/',   my_order.destroy_table,    name='destroy_table'),

    # ─── Waiters ────────────────────────────────────────────────────────────
    path('waiters/',                        my_order.index_waiter,     name='index_waiter'),
    path('waiters/new/',                    my_order.new_waiter,       name='new_waiter'),
    path('waiters/edit/<int:waiter_id>/',   my_order.edit_waiter,      name='edit_waiter'),
    path('waiters/delete/<int:waiter_id>/', my_order.destroy_waiter,   name='destroy_waiter'),

    # ─── Authentication ──────────────────────────────────────────────────────
    path('users/login/',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('users/logout/',
         LogoutView.as_view(next_page='/'),
         name='logout'),
    path('users/change_password/',
         login_required(PasswordChangeView.as_view(
             template_name='change_password.html',
             success_url='/'
         )),
         name='change_password'),
]
