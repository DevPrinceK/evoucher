from knox import views as knox_views
from django.urls import path
from . import views

# authentication
urlpatterns = [
    # API Overview
    path("", views.OverviewAPI.as_view(), name="api-overview"),
    # signup a new user
    path('sign-up/', views.SignUpAPI.as_view(), name="sign_up"),
    # login users
    path('login/', views.LoginAPI.as_view(), name="login"),
    # logout user
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # logout user from all sessions
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

# events
urlpatterns += [
    # Gets all events created by user
    path("all-events/", views.EventListAPI.as_view(), name="all_events"),
    # create, update, delete event
    path("cud-event/", views.CUDEventAPI.as_view(), name="cud_events"),
    # add participant to event
    path("add-participant/", views.AddEventParticipantAPI.as_view()),
    path("rem-participant/", views.RemoveParticipant.as_view()),
]

# vouchers
urlpatterns += [
    # gets system statistics
    path("stats/", views.SystemStatsAPI.as_view(), name="stats"),
    # Gets all vouchers created by user
    path("all-vouchers/", views.VoucherListAPI.as_view(), name="all_vouchers"),
    # create, update, delete voucher
    path("cud-voucher/", views.CUDVoucherAPI.as_view(), name="cud_vouchers"),
    # revoke redeemer's ability to redeem a voucher
    path("revoke-redeemer/", views.RevokeRedeemersVoucherAPI.as_view()),
    # redeems user's voucher
    path("redeem-voucher/", views.RedeemVoucherAPI.as_view()),
    # sends vouchers to event participants
    path("broadcast-voucher/", views.BroadcastVoucherAPI.as_view())
]

# wallet
urlpatterns += [
    path("credit-wallet/", views.FundWalletAPI.as_view(), name="credit_wallet"),
    path('debit-wallet/', views.WithdrawFromWalletAPI.as_view(), name='debit_wallet'),
]