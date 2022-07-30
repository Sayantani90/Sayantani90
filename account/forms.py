from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from django.forms.widgets import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError
from django.http import HttpResponse



import uuid
from account.models import Academic, Account,Department,Research,PriorPost,PresentPost,TeachingExp,Orientation
from account.models import ApiCatg_I, ApiCatg_II 

from datetime import datetime



class RegistrationForm(UserCreationForm):
	# email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('username','emp_id','Department','Designation','email','faculty','gender','password1','password2',
                  'is_hod','is_applicant','frm_submitted','frm_approved','frm_resubmission','frm_rejected')
    

		widgets =  {           
            'emp_id'      : widgets.NumberInput(attrs={
                                'class': 'form-control',                                                  
                                
                                'default': 'blank',                   
                                'oninput': 'limit_input()'
                            }),            
            'username'    : widgets.TextInput(attrs={}),
            'Department'  : widgets.Select(attrs={'style': 'width:100%;height:40px;border: 1px solid lightgrey;border-radius: 5px;border-bottom-width: 2px;'}),
            'Designation' : widgets.Select(attrs={'style': 'width:100%;height:40px;border: 1px solid lightgrey;border-radius: 5px;border-bottom-width: 2px;'}),
            'email'       : widgets.TextInput(attrs={}),
            'faculty'     : widgets.Select(attrs={'style': 'width:100%;height:40px;border: 1px solid lightgrey;border-radius: 5px;border-bottom-width: 2px;'}),
            'gender'      : widgets.Select(attrs={}),
            'password1'   : widgets.PasswordInput(attrs={'style': 'width:100%;height:40px;border: 1px solid lightgrey;border-radius: 5px;'}),
            'password2'   : widgets.PasswordInput(attrs={}),
        }
   
		labels =  {
            'emp_id':'Employee Id',        
            'username':'Full Name',
            'email' : 'Email account',
            'Department':'Department',
            'faculty':'Faculty',
            'gender': 'Gender',
            'Designation' : 'Designation',
        }
        
	def clean_password2(self):
        # Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")
		return password2


    
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		if "@jadavpuruniversity.in" not in email:
			raise forms.ValidationError ("Email must contain @jadavpuruniversity.in!")
		return email   
        
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)           
		except Account.DoesNotExist:
			return email
		#raise forms.ValidationError('Email "%s" is already in use.' % account)
		raise forms.ValidationError('The above email address is already registered.')
        
        
	def clean_empid(self):
		emp_id = self.cleaned_data['emp_id']
		if Account.objects.filter(emp_id=emp_id).count() > 0:
			raise forms.ValidationError('This emp_id is already  in use.')
		return emp_id  
       
        
	def __init__(self, *args, **kwargs):
            super(RegistrationForm,self).__init__(*args, **kwargs)
            self.fields['emp_id'].widget.attrs['placeholder'] = 'Employee Id'                
            self.fields['username'].widget.attrs['autofocus'] = True
            self.fields['username'].widget.attrs['placeholder'] = 'FULL NAME (as in university record)'
            self.fields['email'].widget.attrs['placeholder'] = 'email@jadavpuruniversity.com'            
            self.fields['Department'].empty_label = "Select Department/School"              
            self.fields['Department'].required = True            
            self.fields['Designation'].required = True            
            self.fields['faculty'].required = True
            
            #self.fields['gender'].required = True
            #self.fields['is_applicant'].widget.attrs['disabled'] = True


class AccountAuthenticationForm(forms.ModelForm):
	# email = forms.EmailField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'Ime'}))
    email = forms.EmailField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'Ime'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ('email', 'password')
        
    def clean(self):
     if self.is_valid():
         email = self.cleaned_data['email']
         password = self.cleaned_data['password']
         if not authenticate(email=email, password=password):
             raise forms.ValidationError("Invalid login, error in(email or pwd)")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        # fields = "__all__"
        fields = ('username', 'email', 'Department', 'Designation',
                  'highest_quali', 'pan_no','gender','highest_quali',
                  'dt_ob','date_joined','quali_year','tot_experience',
                  'pdf'
                  
                  )
        
        widgets = {         
            'username' :widgets.TextInput(attrs={'size':'30'}),
            'Department' : widgets.Select(attrs={'style': 'width:330px'}),
            'Designation' : widgets.Select(attrs={'style': 'width:330px'}),            
            'dt_ob': widgets.DateInput(attrs={'type': 'date'}),
            'date_joined': widgets.DateInput(attrs={'type': 'date'}),
            'email': widgets.TextInput(attrs={'size':'30'}),            
            'pan_no': widgets.TextInput(attrs={'size':'12'}),
            'highest_quali':widgets.TextInput(attrs={'size':'33'}),
            'quali_year' : widgets.TextInput(attrs={'size':'4'}), 
            'tot_experience':widgets.TextInput(attrs={'size':'2'}),
        }
        
        labels = {        
            'username':'Full Name',
            'email' : 'Email account',
            'Department':'Name of the Department',
            'pan_no' :'PAN No.',
            'gender' : 'Gender',
            'Designation' : 'Designation',
            'highest_quali' : 'Highest Qualification',
            'dt_ob' : 'Date of Birth',
            'date_joined' : 'Date of joining',
            'quali_year' : 'Qualifying Year',
            'tot_experience' : 'Experiences'
            
        }
        
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm,self).__init__(*args, **kwargs)
        self.fields['Department'].empty_label = "Select"
        self.fields['Department'].required = True
        self.fields['Designation'].empty_label = "Select"
        self.fields['Designation'].required = True        
        self.fields['gender'].required = True        
        self.fields['email'].widget.attrs['readonly'] = True


class AccountCasForm(forms.ModelForm):
  
    class Meta:
        model = Account
        # fields = "__all__"
        fields = ('username', 'parent', 'dt_ob', 'catg','Department','Designation',
                  'agp', 'dt_last_promo','dt_eligibility','addr_corres', 'addr_perm',
                  'mobile','email', 'from_dsg', 'to_dsg','is_carry','pdf',
                  'is_admin','doc_link','highest_quali','ass_yr','is_pwd','pwd_link','fwd_link'
                  )
    
        
        widgets = {
            'username'      : widgets.TextInput(attrs={'class': 'form-control','style': 'width:400px;text-transform:uppercase'}),                        
            'parent'        : widgets.TextInput(attrs={'class': 'form-control','style': 'width:400px;text-transform:uppercase'}),
            'dt_ob'         : widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'ass_yr'        : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'Department'    : widgets.Select(attrs={'class': 'form-control','style': 'width:400px;height:35px;text-transform:uppercase'}),
            'Designation'   : widgets.Select(attrs={'class': 'form-control','style': 'width:400px;height:35px;text-transform:uppercase'}),
            'catg'          : widgets.Select(attrs={
                                'class': 'form-control',
                                'style': 'height:35px;width:72px;font-weight:bold;',                                
                                'oninput': 'check_other()'
                                }),                 
            'addr_corres'   : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'id': 'addr_corres','style': 'text-transform:uppercase' }),            
            'addr_perm'     : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'agp'           : widgets.Select(attrs={'class': 'form-control','style': 'height:35px'}),
            'highest_quali' : widgets.Select(attrs={
                                'class': 'form-control',
                                'style': 'width:400px;height:35px;text-transform:uppercase'                                
                                }),
            'dt_last_promo' : widgets.DateInput(attrs={
                                'class': 'form-control',
                                'type': 'date'                               
                                }),
            'dt_eligibility': widgets.DateInput(attrs={
                                'class': 'form-control',
                                'type': 'date'                               
                                }),
            
            'mobile': widgets.NumberInput(attrs={
                    'class': 'form-control',
                    'id': 'number_field',                    
                    'style': 'width:130px',
                    'default': 'blank',                   
                    'oninput': 'limit_input()'
                }),
            
            'addr_perm'     : widgets.Textarea(attrs={
                              'class': 'form-control',  
                              'class': 'form-control', 'rows': 3,
                              'style': 'text-transform:uppercase',
                              'id': 'addr_perm'
                              }),
            'is_carry' :    widgets.CheckboxInput(attrs={                               
                              'id': 'chk_box',
                              'style': 'height:30px',
                              'oninput': 'check_box()'
                              }),         
            'is_pwd' :    widgets.CheckboxInput(attrs={                               
                              'id': 'chk_pwd',
                              'style': 'height:30px;width:30px;',
                              'oninput': 'check_pwd()'  
                              }), 
            'email'        : widgets.TextInput(attrs={'class': 'form-control','style': 'width:400px'}),
            'doc_link'     : widgets.TextInput(attrs={'class': 'form-control','class':'form-control','style': 'width:400px;height:3em;'}),
            'pwd_link'     : widgets.TextInput(attrs={'class': 'form-control','class':'form-control','style': 'width:400px;height:3em;'}),
            'fwd_link'     : widgets.TextInput(attrs={
                                'class': 'form-control',
                                'class':'form-control',
                                'style': 'width:500px;height:3em;',
                                'oninput': 'check_fwd()'}),

        
        }
        
        labels = {
            'username':'Name (in Block letter)',
            'parent' : "Father's Name/Mother's Name (in Uppercase)",
            'dt_ob':'Date of Birth',
            'catg' :'Category',
            'pdf' : 'PDF',
            'Department' : 'Department/School',
            'Designation' : 'Current Designation',
            'agp' : 'Academic Grade Pay (AGP)',
            'dt_last_promo' : 'Date of last Promotion, if any',
            'dt_eligibility' : 'Date of eligibility for Promotion',
            'addr_corres' : 'Address for correspondence (with PIN)',
            'addr_perm' : 'Permanent Address (with PIN)',
            'mobile' : 'Mobile No.',
            'email' : 'E-mail Id'
            
        }
    
    # def clean_pwd(self):
    #     cleaned_data = super(AccountCasForm, self).clean()
    #     is_pwd = cleaned_data.get('is_pwd')
    #     pwd_link = cleaned_data.get('pwd_link')
        
    #     if cleaned_data['is_pwd']:
    #         if not cleaned_data['pwd_link']:
    #             raise forms.ValidationError(u'Please provide document link!')
    #         return cleaned_data
        
    # def clean_catg(self):
    #     cleaned_data = super(AccountCasForm, self).clean()
    #     catg = cleaned_data.get('catg')
    #     doc_link = cleaned_data.get('doc_link')
                
    #     if cleaned_data['catg'] != 'cast-5':
    #         if not cleaned_data['doc_link']:
    #             raise forms.ValidationError(u'Please provide document link!') 
    #         return cleaned_data 
        
    
    def clean(self):
            cleaned_data = super(AccountCasForm, self).clean()
            is_pwd = cleaned_data.get('is_pwd')
            pwd_link = cleaned_data.get('pwd_link')
            catg = cleaned_data.get('catg')
            doc_link = cleaned_data.get('doc_link')
           
            if cleaned_data['is_pwd']:
                if not cleaned_data['pwd_link']:
                    raise forms.ValidationError(u'Please provide document link!')
                #return cleaned_data
                
            if cleaned_data['catg'] != 'cast-5':
                if not cleaned_data['doc_link']:
                    raise forms.ValidationError(u'Please provide document link!') 
                #return cleaned_data 

                
       
    def __init__(self, *args, **kwargs):
        super(AccountCasForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        
        
        if self.fields['is_admin'] == True:
           self.fields['parent'].widget.attrs['readonly'] = True
           
        #self.fields['pwd_link'].required = True
        
        #if self.fields['is_pwd'] == False:
           #self.fields['pwd_link'].required = False
        self.fields['fwd_link'].widget.attrs['placeholder'] = 'URL for scan copy of signed endorsement form'    
        self.fields['from_dsg'].widget.attrs['readonly'] = True
        self.fields['to_dsg'].required = True
        self.fields['parent'].required = True
        self.fields['catg'].required = True
        self.fields['Department'].required = True
        self.fields['Department'].empty_label = "Select"
        self.fields['Designation'].required = True
        self.fields['agp'].required = True
        self.fields['highest_quali'].required = True
        self.fields['dt_ob'].required = True
        self.fields['addr_corres'].required = True
        self.fields['addr_perm'].required = True        
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['mobile'].value = 0        
       

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academic
        fields= '__all__'
        
        
        widgets = {
            'degree'                : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase;height:7px', 'initial':'Blank' }),
            'name_board_university' : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'div_class_grade'       : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'subject'               : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'year_passing'          : widgets.NumberInput(attrs={
                    'id': 'pass_out', 
                    'class': 'form-control',                   
                    'style': 'width:90px; text-align: center;',
                    'oninput': 'max_input()'
                }),
            'marks_obtained': widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width:90px','oninput': 'max_marks()'}), 
            'doc_link'     : widgets.TextInput(attrs={'class':'form-control','style': 'width:400px;height:3em;'}),
        }
      
    def __init__(self,*args,**kwargs):
        super (AcademyForm,self ).__init__(*args,**kwargs)
        self.fields['marks_obtained'].validators = [marks_range]
        self.fields['year_passing'].validators = [year_range]
 
def marks_range(value):
    if value < 0 or value > 100:
       raise ValidationError(u'Max is 100') 
          
def year_range(value):
    if value < 1950 or value > 2023:
       raise ValidationError(u'Check the year') 


   
class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields= '__all__' 
        
        widgets = {
            'degree'           : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase;height:7px' }),
            'thesis'           : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'dt_award'         : widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),  
            'institute'        : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'url_link'         : widgets.TextInput(attrs={'class':'form-control','style': 'width:400px;height:3em;'}),
        }
        
    def __init__(self,*args,**kwargs):
        super (ResearchForm,self ).__init__(*args,**kwargs)

class PrestsForm(forms.ModelForm):
    class Meta:
        model = PriorPost
        fields= '__all__' 
        
        widgets = {
            'designation'           : widgets.TextInput(attrs={'class': 'form-control','style': 'width:400px;text-transform:uppercase'}),
            'employer'              : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'dt_join'               : widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),  
            'dt_leav'               : widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),  
            'gross_salary'          : widgets.NumberInput(attrs={'class': 'form-control'}),
            'reason_leaving'        : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase;' }),
        }
        
    def __init__(self,*args,**kwargs):
        super (PrestsForm,self ).__init__(*args,**kwargs)
                        
class PresentPostForm(forms.ModelForm):
    # faculty_txt = forms.CharField(max_length=30)
    
    
    
    class Meta: 
        model = PresentPost
        fields= '__all__' 
        
        widgets = {
            'department'        : widgets.Select(attrs={'style': 'width:250px;height:40px'}),
            'designation'       : widgets.Select(attrs={'style': 'width:250px;height:40px'}),
            'period_from'       : widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),  
            'period_to'         : widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),  
            'pay_scale'         : widgets.TextInput(attrs={'class': 'form-control','style': 'width:180px;text-transform:uppercase'}),
            'agp'               : widgets.Select(attrs={'style': 'width:100px;height:35px'}),
        }
    
        
    def __init__(self,*args,**kwargs):
        super (PresentPostForm,self ).__init__(*args,**kwargs)
        self.fields['department'].empty_label = "Select"   


        
class TeachingExpForm(forms.ModelForm):
    
    
    class Meta:
        model = TeachingExp
        fields= '__all__' 
        
        widgets = {
            'pg_class'        : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'ug_class'        : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'doc_yrs'         : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'postdoc_yrs'     : widgets.NumberInput(attrs={'class':'form-number form-control'}),            
            'specialisation'  : widgets.Textarea(attrs={'class': 'form-control', 'rows': 2,'style': 'text-transform:uppercase;width:500px;height:100px;' }),
            'url_link'        : widgets.TextInput(attrs={'class':'form-control'}),
        }
        
    def __init__(self,*args,**kwargs):
        super (TeachingExpForm,self ).__init__(*args,**kwargs)
           
class OrientationForm(forms.ModelForm):
    
    
    class Meta:
        model = Orientation
        fields= '__all__' 
        
        widgets = {
            'title'              : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'place'              : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'duration'           : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'period'             : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
   
        }
        
    def __init__(self,*args,**kwargs):
        super (OrientationForm,self ).__init__(*args,**kwargs)
           
class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        # fields = "__all__"
        fields = ('pdf',) 
                        
    myfile = forms.FileField(required=False)
    
    def __init__(self,*args,**kwargs):
        super (AccountEditForm,self ).__init__(*args,**kwargs)

class ApiCatg_IForm(forms.ModelForm):
    
    class Meta:
        model = ApiCatg_I
        fields = "__all__"
    
        widgets = {            
            'direct_teaching'   : widgets.NumberInput(attrs={
                'id': 'dt_hrs',
                'class': 'form-control',
                'style': 'width:70px;',
                'default': 0 ,
                'oninput': 'limit_input()'
                }),
            
            'actl_api_dt'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
            'self_api_dt'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
            'veri_api_dt'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
           
            'exam_duties'         : widgets.NumberInput(attrs={
                'id': 'ed_hrs',
                'class': 'form-control',
                'style': 'width:70px;',
                'default': 0 ,
                'oninput': 'limit_input()'
                }),
           
            'actl_api_ed'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
            'self_api_ed'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
            'veri_api_ed'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
           
           
            'innovating_teaching'    : widgets.NumberInput(attrs={
                'id': 'it_hrs',
                'class': 'form-control',
                'style': 'width:70px;',
                'default': 0 ,
                'oninput': 'limit_input()'
                }),
           
            'actl_api_it'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
            'self_api_it'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
            'veri_api_it'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:100px;'}),
           
           
           
           
            }
    
    def __init__(self,*args,**kwargs):
        super (ApiCatg_IForm,self ).__init__(*args,**kwargs)
        self.fields['direct_teaching'].validators = [min_range]
        self.fields['actl_api_dt'].widget.attrs['readonly'] = True
        self.fields['self_api_dt'].widget.attrs['readonly'] = True
        self.fields['veri_api_dt'].widget.attrs['readonly'] = True

        self.fields['exam_duties'].validators = [min_range]
        self.fields['actl_api_ed'].widget.attrs['readonly'] = True
        self.fields['self_api_ed'].widget.attrs['readonly'] = True
        self.fields['veri_api_ed'].widget.attrs['readonly'] = True


        self.fields['innovating_teaching'].validators = [min_range]
        self.fields['actl_api_it'].widget.attrs['readonly'] = True
        self.fields['self_api_it'].widget.attrs['readonly'] = True
        self.fields['veri_api_it'].widget.attrs['readonly'] = True
        
def min_range(value):
    if value < 100 :
       raise ValidationError(u'Check the hours')         
   
   
class ApiCatg_IIForm(forms.ModelForm):
    
    class Meta:
        model = ApiCatg_II
        fields = "__all__"

        widgets = {            
            'field_based_activities'   : widgets.NumberInput(attrs={
                'id': 'fba_hrs',
                'class': 'form-control',
                'style': 'width:70px',
                'default': 0 ,
                'oninput': 'limit_input1()'
                }),
            
            'actl_api_fba'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
            'self_api_fba'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
            'veri_api_fba'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
           
            'corp_life_management' : widgets.NumberInput(attrs={
                'id': 'clm_hrs',
                'class': 'form-control',
                'style': 'width:70px;',
                'default': 0 ,
                'oninput': 'limit_input2()'
                }),
           
            'actl_api_clm'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
            'self_api_clm'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
            'veri_api_clm'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
           
           
            'prof_dev_activity'    : widgets.NumberInput(attrs={
                'id': 'pda_hrs',
                'class': 'form-control',
                'style': 'width:70px;',
                'default': 0 ,
                'oninput': 'limit_input3()'
                }),
           
            'actl_api_pda'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
            'self_api_pda'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
            'veri_api_pda'         : widgets.NumberInput(attrs={'class': 'form-control','style': 'width:80px;'}),
                      
            }
    
    def __init__(self,*args,**kwargs):
        super (ApiCatg_IIForm,self ).__init__(*args,**kwargs)
        self.fields['field_based_activities'].validators = [min_range]
        self.fields['actl_api_fba'].widget.attrs['readonly'] = True
        self.fields['self_api_fba'].widget.attrs['readonly'] = True
        self.fields['veri_api_fba'].widget.attrs['readonly'] = True

        self.fields['corp_life_management'].validators = [min_range]
        self.fields['actl_api_clm'].widget.attrs['readonly'] = True
        self.fields['self_api_clm'].widget.attrs['readonly'] = True
        self.fields['veri_api_clm'].widget.attrs['readonly'] = True


        self.fields['prof_dev_activity'].validators = [min_range]
        self.fields['actl_api_pda'].widget.attrs['readonly'] = True
        self.fields['self_api_pda'].widget.attrs['readonly'] = True
        self.fields['veri_api_pda'].widget.attrs['readonly'] = True
        
def min_range(value):
    if value < 100 :
       raise ValidationError(u'Check the hours')         
   
    