from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



from django.conf import settings
from django.conf.urls.static import static

from personal.views import (
    temp,
    home_proj,
    dashboard,
    

)


from account.views import (    
    register_view,
    login_view,
    logout_view,
    academy_add,
    research_add,
    prests_add,
    curpost_add,
    teach_add,
    orient_add,
    academy_cancel,
    research_cancel,
    prests_cancel,
    curpost_cancel,
    teach_cancel,
    orient_cancel,
    
)

from catg_3.views import (	
    jrnl_add,
    jrnl_cancel,
    pub_other_add,
    pub_other_cancel,
    resch_sponsor_add,
    resch_cons_add,
    resch_cancel,
    resch_cons_cancel,
    prj_add,
    prj_cancel,
    resch_guide_add,
    resch_guide_cancel,
    fellow_award_add,
    fellow_award_cancel,
    
    lecture_paper_add,
    lecture_paper_cancel,
    
    lecture_elearn_add,
    lecture_elearn_cancel,
    
)

urlpatterns = [	
       
	path('admin/', admin.site.urls),
    
 
    path('login', login_view, name="login"),
    path('account/', include('account.urls', namespace='account')),
    path('catg_3/', include('catg_3.urls', namespace='catg_3')),

    path('logout/', logout_view, name="logout"),  
    path('', register_view, name="register"),  
    path('academy-add', academy_add, name='academy-add'),
    path('jrnl-add', jrnl_add, name='jrnl-add'),
    path('jrnl-cancel', jrnl_cancel, name='jrnl-cancel'),
    path('pub-add', pub_other_add, name='pub-add'),
    path('pub-cancel', pub_other_cancel, name='pub-cancel'),
   
    path('resch-sponsor-add', resch_sponsor_add, name='resch-sponsor-add'),
    path('resch-cons-add', resch_cons_add, name='resch-cons-add'),
    path('resch-cancel', resch_cancel, name='resch-cancel'),
    path('resch-cons-cancel', resch_cons_cancel, name='resch-cons-cancel'),
     
    
    path('resch-guide-add', resch_guide_add, name='resch-guide-add'),
    path('resch-guide-cancel', resch_guide_cancel, name='resch-guide-cancel'),
    
    
    path('fellow-award-add', fellow_award_add, name='fellow-award-add'),
    path('fellow-award-cancel', fellow_award_cancel, name='fellow-award-cancel'),
        
    path('lecture-paper-add', lecture_paper_add, name='lecture-paper-add'),
    path('lecture-paper-cancel', lecture_paper_cancel, name='lecture-paper-cancel'),
   
    path('lecture-elearn-add', lecture_elearn_add, name='lecture-elearn-add'),
    path('lecture-elearn-cancel', lecture_elearn_cancel, name='lecture-elearn-cancel'),
    
    
    path('prj-add', prj_add, name='prj-add'),
    path('prj-cancel', prj_cancel, name='prj-cancel'),
    
    path('research-add', research_add, name='research-add'),
    path('prests-add', prests_add, name='prests-add'),
    path('curpost-add', curpost_add, name='curpost-add'),
    path('teach-add', teach_add, name='teach-add'),
    path('orient-add', orient_add, name='orient-add'),
    path('academy-cancel', academy_cancel, name='academy-cancel'),
    path('research-cancel', research_cancel, name='research-cancel'),
    path('prests-cancel', prests_cancel, name='prests-cancel'), 
    path('curpost-cancel', curpost_cancel, name='curpost-cancel'),
    path('teach-cancel', teach_cancel, name='teach-cancel'),
    path('orient-cancel', orient_cancel, name='orient-cancel'),    
    path('temp/', temp, name='temp'),    
    path('home-proj/', home_proj, name='home-proj'),
    path('dashboard/', dashboard, name='dashboard'),
    
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),
        
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),    
    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset/reset_password.html"),
         name="reset_password"),

    #path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
    #     name="password_reset_done"),

    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
    #     name="password_reset_confirm"),

    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
    #     name="password_reset_complete"),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    


# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="passsword_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_complete"    

