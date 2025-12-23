from .overview import DashboardView
from .orders import OrderListView, OrderItemListView
from .favorites import FavoriteProductsView
from .address import AddressListView, AddressCreateView, AddressUpdateView, set_default_address
from .profile import ProfileView, ProfileUpdateView, change_phone_view, change_phone_verify_view, resend_change_phone_otp
