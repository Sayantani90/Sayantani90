from django.urls import path
from . import views

from catg_3.views import (
	jrnl_view,
	jrnl_edit,
    jrnl_add1,
 	jrnl_delete,
    pub_other_view,
	pub_add1,
	pub_edit,
	pub_delete,
	resch_proj_view,
 	resch_add1,
    resch_cons_add1,
 	resch_edit,
    resch_cons_edit,
  	resch_delete,
    resch_cons_delete,
   	prj_outcm_view,
    prj_add1,
    prj_edit,
    prj_delete,
    
    resch_guide_view,
    resch_guide_add1,
    resch_guide_edit,
    resch_guide_delete,
    
    fellow_award_view,
    fellow_award_add1,
    fellow_award_edit,
    fellow_award_delete,
        
    lecture_paper_add1,
    lecture_paper_edit,
    lecture_paper_delete,
    
    lecture_elearn_add1,
    lecture_elearn_edit,
    lecture_elearn_delete,
    
    api_summary_view,
    LetterView,
    LetterPDF,
    
)


app_name = 'catg_3'

urlpatterns = [

    
    path('<user_id>/letter/', LetterView, name="letter"),
    path('<user_id>/endo-view/', LetterPDF.as_view(), name="endo-view"),
    
	path('<user_id>/jrnl-pub/', jrnl_view, name="jrnl-pub"),
	path('jrnl-edit/<str:pk>/', jrnl_edit, name="jrnl-edit"),
 	path('jrnl-add1/<str:pk>/', jrnl_add1, name="jrnl-add1"),
    path('jrnl-delete/<str:pk>/', jrnl_delete, name="jrnl-delete"),
 	
    path('<user_id>/pub-other/', pub_other_view, name="pub-other"),
	path('pub-edit/<str:pk>/', pub_edit, name="pub-edit"),
	path('pub-add1/<str:pk>/', pub_add1, name="pub-add1"),
	path('pub-delete/<str:pk>/', pub_delete, name="pub-delete"),

 	path('<user_id>/resch-view', resch_proj_view, name="resch-view"),
	path('resch-add1/<str:pk>/', resch_add1, name="resch-add1"),
    path('resch-cons-add1/<str:pk>/', resch_cons_add1, name="resch-cons-add1"),
	path('resch-edit/<str:pk>/', resch_edit, name="resch-edit"),
    path('resch-cons-edit/<str:pk>/', resch_cons_edit, name="resch-cons-edit"),
	path('resch-delete/<str:pk>/', resch_delete, name="resch-delete"),
    path('resch-cons-delete/<str:pk>/', resch_cons_delete, name="resch-cons-delete"),

	path('<user_id>/prj-outcm-view', prj_outcm_view, name="prj-outcm-view"),
	path('prj-add1/<str:pk>/', prj_add1, name="prj-add1"),
	path('prj-edit/<str:pk>/', prj_edit, name="prj-edit"),
 	path('prj-delete/<str:pk>/', prj_delete, name="prj-delete"),
    
    path('<user_id>/resch-guide-view', resch_guide_view, name="resch-guide-view"),
	path('resch-guide-add1/<str:pk>/', resch_guide_add1, name="resch-guide-add1"),
	path('resch-guide-edit/<str:pk>/', resch_guide_edit, name="resch-guide-edit"),
	path('resch-guide-delete/<str:pk>/', resch_guide_delete, name="resch-guide-delete"),

    
    path('<user_id>/fellow-award-view', fellow_award_view, name="fellow-award-view"),
	path('fellow-award-add1/<str:pk>/', fellow_award_add1, name="fellow-award-add1"),
	path('fellow-award-edit/<str:pk>/', fellow_award_edit, name="fellow-award-edit"),
	path('fellow-award-delete/<str:pk>/', fellow_award_delete, name="fellow-award-delete"),

   
	path('lecture-paper-add1/<str:pk>/', lecture_paper_add1, name="lecture-paper-add1"),
	path('lecture-paper-edit/<str:pk>/', lecture_paper_edit, name="lecture-paper-edit"),
	path('lecture-paper-delete/<str:pk>/', lecture_paper_delete, name="lecture-paper-delete"),


	path('lecture-elearn-add1/<str:pk>/', lecture_elearn_add1, name="lecture-elearn-add1"),
	path('lecture-elearn-edit/<str:pk>/', lecture_elearn_edit, name="lecture-elearn-edit"),
	path('lecture-elearn-delete/<str:pk>/', lecture_elearn_delete, name="lecture-elearn-delete"),
    
    path('<user_id>/api-summary-view', api_summary_view, name="api-summary-view"),
     
    

]
