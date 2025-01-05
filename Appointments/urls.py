from django.urls import path
from .views import (
    IndexView,
    InstructorListView,
    LoadMoreContentView,
    SearchInstitution,
    Search,
    MakeAppointmentView,
    CreateAppointmentView,
    GetAppointmentTimes,
    UserAppointmentsList,
    EditAppointmentVerifiedUser,
    DeleteAppointment,
    UpdateCreatedAppointment,
    DeleteCreatedAppointment
)   


urlpatterns = [
    path(route='', view=IndexView.as_view(), name='index'),
    path(route='ögretim-görevlileri/', view=InstructorListView.as_view(), name='instructor_list'),
    path(route='ogretim-gorevlileri/daha-fazla-yukle/', view=LoadMoreContentView.as_view(), name='load_more'),
    path(route='ogretim-gorevlileri/kurum-arama/', view=SearchInstitution.as_view(), name='search_institution'),
    path(route='ogretim-gorevlileri/arama/', view=Search.as_view(), name='search'),
    path(route='randevu-al/<slug:slug>', view=MakeAppointmentView.as_view(), name='make_appointment'),
    path(route='randevu-olustur', view=CreateAppointmentView.as_view(), name='create_appointment'),
    path('get-times/<slug:slug>', GetAppointmentTimes.as_view(), name='get_times'),
    path('alinan-randevular/', UserAppointmentsList.as_view(), name='user_appointment_list'),
    path('alinan-randevuyu/düzenle/<int:id>/', EditAppointmentVerifiedUser.as_view(), name='edit_appointment'),
    path('alinan-randevuyu/sil/<int:id>/', DeleteAppointment.as_view(), name='delete_appointment'),
    path('olusturulan-randevuyu/güncelle/<int:id>/',view=UpdateCreatedAppointment.as_view(), name='updated_created_appointment' ),
    path('olusturulan-randevuyu/sil/<int:id>/', view=DeleteCreatedAppointment.as_view(), name='delete_created_appointment' )
]
