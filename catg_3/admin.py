from django.contrib import admin
from catg_3.models import Jrnl_pub, Pub_other, Resch_proj,Prj_outcm


# Register your models here.

class Jrnl_pubAdmin(admin.ModelAdmin):
	list_display = (
     'email','yr_pub','title_pub','no_auth','role_appl','jrnl_name','vl_pg','jrnl_type','imp_fac','jrnl_url','jrnl_link'
     )
 
 
admin.site.register(Jrnl_pub,Jrnl_pubAdmin)

#--------------------------------

class Pub_otherAdmin(admin.ModelAdmin):
	list_display = (
     'email','yr_pub','pub_type','chap_title','bk_title','no_auth','name_pub','sts_pub','isbn_no','pub_url','pub_pdf'
     )
 
 
admin.site.register(Pub_other,Pub_otherAdmin)

#--------------------------------

class Resch_projAdmin(admin.ModelAdmin):
	list_display = (
     'email','faculty_app','proj_title','fund_agnc','no_yrs','prj_amt','prj_url','prj_pdf'
     )
 
 
admin.site.register(Resch_proj,Resch_projAdmin)

#--------------------------------

#--------------------------------

class Prj_outcmAdmin(admin.ModelAdmin):
	list_display = (
     'email','faculty_app','prj_type','proj_title','prj_lvl','ref_no','ptnt_sts','prj_url','prj_pdf'
     )
 
 
admin.site.register(Prj_outcm,Prj_outcmAdmin)
