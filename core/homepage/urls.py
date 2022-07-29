from django.urls import path
from core.homepage.views.services.views import *
from core.homepage.views.departments.views import *
from core.homepage.views.socialnetworks.views import *
from core.homepage.views.statistics.views import *
from core.homepage.views.mainpage.views import *
from core.homepage.views.freqquestions.views import *
from core.homepage.views.testimonials.views import *
from core.homepage.views.gallery.views import *
from core.homepage.views.mecanicos.views import *
from core.homepage.views.comments.views import *
from core.homepage.views.qualities.views import *
from core.homepage.views.news.views import *
from core.homepage.views.videos.views import *

urlpatterns = [
    # mainpage
    path('', MainPageIndexView.as_view(), name='index'),
    path('mainpage/update/', MainPageUpdateView.as_view(), name='main_update'),
    path('signin/', SignInView.as_view(), name='signin'),
    # services
    path('homepage/services/', ServicesListView.as_view(), name='services_list'),
    path('homepage/services/add/', ServicesCreateView.as_view(), name='services_create'),
    path('homepage/services/update/<int:pk>/', ServicesUpdateView.as_view(), name='services_update'),
    path('homepage/services/delete/<int:pk>/', ServicesDeleteView.as_view(), name='services_delete'),
    # departments
    path('homepage/departments/', DepartmentsListView.as_view(), name='departments_list'),
    path('homepage/departments/add/', DepartmentsCreateView.as_view(), name='departments_create'),
    path('homepage/departments/update/<int:pk>/', DepartmentsUpdateView.as_view(), name='departments_update'),
    path('homepage/departments/delete/<int:pk>/', DepartmentsDeleteView.as_view(), name='departments_delete'),
    # socialnetworks
    path('homepage/socialnetworks/', SocialNetworksListView.as_view(), name='socialnetworks_list'),
    path('homepage/socialnetworks/add/', SocialNetworksCreateView.as_view(), name='socialnetworks_create'),
    path('homepage/socialnetworks/update/<int:pk>/', SocialNetworksUpdateView.as_view(), name='socialnetworks_update'),
    path('homepage/socialnetworks/delete/<int:pk>/', SocialNetworksDeleteView.as_view(), name='socialnetworks_delete'),
    # statistics
    path('homepage/statistics/', StatisticsListView.as_view(), name='statistics_list'),
    path('homepage/statistics/add/', StatisticsCreateView.as_view(), name='statistics_create'),
    path('homepage/statistics/update/<int:pk>/', StatisticsUpdateView.as_view(), name='statistics_update'),
    path('homepage/statistics/delete/<int:pk>/', StatisticsDeleteView.as_view(), name='statistics_delete'),
    # freqquestions
    path('homepage/freqquestions/', FreqQuestionsListView.as_view(), name='freqquestions_list'),
    path('homepage/freqquestions/add/', FreqQuestionsCreateView.as_view(), name='freqquestions_create'),
    path('homepage/freqquestions/update/<int:pk>/', FreqQuestionsUpdateView.as_view(), name='freqquestions_update'),
    path('homepage/freqquestions/delete/<int:pk>/', FreqQuestionsDeleteView.as_view(), name='freqquestions_delete'),
    # testimonials
    path('homepage/testimonials/', TestimonialsListView.as_view(), name='testimonials_list'),
    path('homepage/testimonials/add/', TestimonialsCreateView.as_view(), name='testimonials_create'),
    path('homepage/testimonials/update/<int:pk>/', TestimonialsUpdateView.as_view(), name='testimonials_update'),
    path('homepage/testimonials/delete/<int:pk>/', TestimonialsDeleteView.as_view(), name='testimonials_delete'),
    # galery
    path('homepage/gallery/', GalleryListView.as_view(), name='gallery_list'),
    path('homepage/gallery/add/', GalleryCreateView.as_view(), name='gallery_create'),
    path('homepage/gallery/update/<int:pk>/', GalleryUpdateView.as_view(), name='gallery_update'),
    path('homepage/gallery/delete/<int:pk>/', GalleryDeleteView.as_view(), name='gallery_delete'),
    # team
    path('homepage/team/', TeamListView.as_view(), name='team_list'),
    path('homepage/team/add/', TeamCreateView.as_view(), name='team_create'),
    path('homepage/team/update/<int:pk>/', TeamUpdateView.as_view(), name='team_update'),
    path('homepage/team/delete/<int:pk>/', TeamDeleteView.as_view(), name='team_delete'),
    # qualities
    path('homepage/qualities/', QualitiesListView.as_view(), name='qualities_list'),
    path('homepage/qualities/add/', QualitiesCreateView.as_view(), name='qualities_create'),
    path('homepage/qualities/update/<int:pk>/', QualitiesUpdateView.as_view(), name='qualities_update'),
    path('homepage/qualities/delete/<int:pk>/', QualitiesDeleteView.as_view(), name='qualities_delete'),
    # comments
    path('homepage/comments/', CommentsListView.as_view(), name='comments_list'),
    path('homepage/comments/delete/<int:pk>/', CommentsDeleteView.as_view(), name='comments_delete'),
    #  videos
    path('homepage/videos/', VideosListView.as_view(), name='videos_list'),
    path('homepage/videos/add/', VideosCreateView.as_view(), name='videos_create'),
    path('homepage/videos/update/<int:pk>/', VideosUpdateView.as_view(), name='videos_update'),
    path('homepage/videos/delete/<int:pk>/', VideosDeleteView.as_view(), name='videos_delete'),
    #  news
    path('homepage/news/', NewsListView.as_view(), name='news_list'),
    path('homepage/news/add/', NewsCreateView.as_view(), name='news_create'),
    path('homepage/news/update/<int:pk>/', NewsUpdateView.as_view(), name='news_update'),
    path('homepage/news/delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
]
