from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Department,Academic,Orientation,ApiCatg_I



class AccountAdmin(UserAdmin):
	list_display = (
     'email','emp_id','username','date_joined','dt_ob', 
     'last_login','is_applicant','is_admin','is_hod','is_dean',
     'Department', 'Designation', 'faculty',
     'highest_quali','pan_no',
     'gender','quali_year',
     'tot_experience',     
     )
	search_fields = ('email','username')
	readonly_fields=('id','last_login')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()




admin.site.register(Account, AccountAdmin)
admin.site.register(Academic)
admin.site.register(Department)
admin.site.register(Orientation)
admin.site.register(ApiCatg_I)