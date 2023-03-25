from django.urls import path
from exp.views import GDSC
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',GDSC.home,name="home" ),
    # path('data_save/',views.save_data,name="save_data" ),
    path("send_otp/",GDSC.send_otp,name="send_otp"),
    path("payment/",GDSC.otp_validation,name="payment"),
    path("ticket/",GDSC.ticket,name="ticket"),
    path("success/",GDSC.success,name="success"),

]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        
        