from django import forms
from django.forms import Field,widgets,ValidationError

#from django.utils.translation import ugettext_lazy




from . models import Jrnl_pub, Pub_other,Resch_proj,Resch_cons,Prj_outcm,Resch_guide,Fellow_Award,Lecture_Paper,E_Learning
  
class Jrnl_pubForm(forms.ModelForm):
    
    class Meta:
        model = Jrnl_pub
        fields = "__all__"
         
    
        widgets = {            
            'yr_pub'        : widgets.NumberInput(attrs={'class':'form-number form-control'}),                        
            'title_pub'     : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 5em;text-transform:uppercase',
                                               'rows': 3,'cols': 30}),
            'no_auth'       : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'check_other()'}),                        
            'role_appl'     : widgets.Select(attrs={                              
                              'class':'form-control',
                              'style': 'width:600px;height:3em;text-transform:uppercase',
                              'oninput': 'check_other()'
                               }),
            'jrnl_name'     : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
            'vl_pg'         : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
            'jrnl_type'     : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
            'imp_fac'       : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'check_impact()'}),                        
            'jrnl_url'      : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
            'jrnl_link'     : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
            'jrnl_oth'      : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            
            }
        
    def clean(self):
            cleaned_data = super(Jrnl_pubForm, self).clean()
            no_auth = cleaned_data.get('no_auth')
            jrnl_oth = cleaned_data.get('jrnl_oth')
            role_appl = cleaned_data.get('role_appl')
            imp_fac = cleaned_data.get('imp_fac')
            jrnl_url = cleaned_data.get('jrnl_url')
            
            if imp_fac > 0 :
                if not jrnl_url:
                    raise ValidationError(u'Please provide necessary document link against impact factor!')
            return cleaned_data
            
            if no_auth == 1 :
                if role_appl != "FC_A":
                    raise ValidationError(u'Please ensure no of authors against your Role!')
                    # self.add_error('role_appl', 'Role of applicant does not match with no of authors!')
                    # You can use ValidationError as well
                    # self.add_error('role_appl', form.ValidationError('Role of applicant does not match with no of authors!'))                     
                    # raise ValidationError(u'Role of applicant does not match with no of authors!')
            
            if role_appl == "O_A":
                
                #  if jrnl_oth == 0:
                #     raise ValidationError(u'Other no must be > 0')
                 
                 if jrnl_oth >= no_auth:
                    raise ValidationError(u'Other must be < No of authors')
                         
                
    def __init__(self, *args, **kwargs):
        super(Jrnl_pubForm,self).__init__(*args, **kwargs)
        self.fields['yr_pub'].widget.attrs['min'] = 1949
        self.fields['yr_pub'].widget.attrs['max'] = 2022
        self.fields['yr_pub'].required = True
        self.fields['no_auth'].widget.attrs['min'] = 1
        self.fields['no_auth'].widget.attrs['max'] = 10  
        self.fields['imp_fac'].widget.attrs['min'] = 0
        self.fields['imp_fac'].widget.attrs['max'] = 99
        self.fields['jrnl_oth'].widget.attrs['min'] = 0
        self.fields['jrnl_oth'].widget.attrs['max'] = 9
        

       



class Pub_otherForm(forms.ModelForm):
    
    class Meta:
        model = Pub_other
        fields = "__all__"

        widgets = {            
                    'yr_pub'         : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'limit_input()'}),                        
                    'pub_type'       : widgets.Select(attrs={
                                                        'class':'form-control',
                                                        'style': 'width:600px;height:3em;text-transform:uppercase',
                                                        'oninput': 'check_other()'}),
                    'chap_title'     : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                                                    'rows': 3,'cols': 40}),
                    'bk_title'       : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                                                    'rows': 3,'cols': 40}),
                    'no_auth'        : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'check_other()'}), 
                    'name_pub'       : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
                    'sts_pub'        : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
                    'isbn_no'        : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
                    'pub_url'        : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),    
                    
                    
                    
                    }
        
    def clean(self):
            cleaned_data = super(Pub_otherForm, self).clean()
            no_auth = cleaned_data.get('no_auth')
            pub_type = cleaned_data.get('pub_type')
            
            chp_title = cleaned_data.get('chap_title')
            sts_pub = cleaned_data.get('sts_pub')
            
            if pub_type == 'BK_CHAP':
               if not chp_title:
                  print(pub_type)
                  raise ValidationError(u'Please Fill the Title of the Chapter')
            return cleaned_data
            
                       
    def __init__(self, *args, **kwargs):
        super(Pub_otherForm,self).__init__(*args, **kwargs)
        
        self.fields['yr_pub'].widget.attrs['min'] = 1990
        self.fields['yr_pub'].widget.attrs['max'] = 2022 # check current year
        self.fields['yr_pub'].required = True
        self.fields['no_auth'].widget.attrs['min'] = 1
        self.fields['no_auth'].widget.attrs['max'] = 10
        self.fields['pub_type'].required = True
        #self.fields['chap_title'].required = True
        self.fields['bk_title'].required = True
        self.fields['no_auth'].required = True
        self.fields['name_pub'].required = True        
        self.fields['sts_pub'].required = True
        self.fields['isbn_no'].required = True
        self.fields['pub_url'].required = True
                






        
        
class Resch_projForm(forms.ModelForm):
     
    class Meta:
        model = Resch_proj
        fields = "__all__"
        
        error_messages = {
            'name': {
                'prj_amt': "Check the value",
            },
        }
     
        widgets = {
            'faculty_app'  : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
            'proj_title'   : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
            'fund_agnc'    : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                              'rows': 3,'cols': 40}),                       
            'no_yrs'       : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'prj_amt'      : widgets.NumberInput(attrs={
                                'class':'form-number form-control',
                                'oninput': 'limit_input()'                                
                                }),
            'prj_url'      : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),           
        }
        
        
    def clean(self):
            cleaned_data = super(Resch_projForm, self).clean()
            prj_tg = cleaned_data.get('proj_tag')
            prj_amt = cleaned_data.get('prj_amt')
            faculty_app = cleaned_data.get('faculty_app')
            
            # validating the proj_tag
            
            if prj_tg == 'cons':
                if faculty_app == 'ARTS':
                    if prj_amt < 2 :
                       raise ValidationError(u'Check the amount!')
                else:
                    if prj_amt < 10 :
                       raise ValidationError(u'Check the amount!')
                
                 
                       
                
    def __init__(self, *args, **kwargs):
            super(Resch_projForm,self).__init__(*args, **kwargs)            
            self.fields['prj_amt'].widget.attrs['max'] = 999.99 

class Resch_consForm(forms.ModelForm):
  
    class Meta:
        model = Resch_cons
        fields = "__all__" 
        #fields = ('email','proj_tag','faculty_app','proj_title','fund_agnc','no_yrs','prj_amt','prj_url','prj_pdf','self_api_score','veri_api_score')  
        
        widgets = {
            'faculty_app'  : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase',}),
            'proj_title'   : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
            'fund_agnc'    : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                              'rows': 3,'cols': 40}),                       
            'no_yrs'       : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'prj_amt'      : widgets.NumberInput(attrs={
                                'class':'form-number form-control',                               
                                'oninput': 'limit_input()',                               
                                }),
                               
                         
            'prj_url'      : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),           
        }
        
        
    def clean(self):
            cleaned_data = super(Resch_consForm, self).clean()           
            prj_tg = cleaned_data.get('proj_tag')
            prj_amt = cleaned_data.get('prj_amt')
            faculty_app = cleaned_data.get('faculty_app')
            
            
                
            # validating the proj_tag
            #if prj_amt :
                #if prj_tg == 'cons':
                    #if faculty_app == 'ARTS':
                        #if prj_amt < 2 :
                            #raise ValidationError(u'Check the min amount for "Arts"!')
                    #else:
                        #if prj_amt < 10 :
                            #raise ValidationError(u'Check the min amount other than Arts!')
            #else:
                #raise ValidationError('Amount Mobilized (Rs.in Lacs) Max(999.99) !')
                
                
           
    def __init__(self, *args, **kwargs):
            super(Resch_consForm,self).__init__(*args, **kwargs)
            #self.fields['faculty_app'].error_messages = {'required': 'FAS:DJFASKL:DJF'}
            #self.fields['faculty_app'].error_messages['required'] = 'Please let us know what is your area of work!'     
            #self.fields['faculty_app'].required = True
            #self.fields['faculty_app'].error_messages['required'] = 'Please let us know what is your area of work!'
            #self.fields['faculty_app'].error_messages = {'required': 'Please let us know what is your area of work!'}
            #self.fields['faculty_app'].error_messages['required'] = 'Please let us know what is your area of work!'     
            self.fields['prj_amt'].validators = [max_range]
            
            
 
def max_range(value):
    if value < 0 or value > 999.99:
       raise ValidationError(u'Rs. in Lacs only!!!!!')    
       
       
 
class Prj_outcmForm(forms.ModelForm):
     
    class Meta:
        model = Prj_outcm
        fields = "__all__"
                    
        widgets = {
             'faculty_app'  : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_type'     : widgets.Select(attrs={
                                'class':'form-control',
                                'style': 'width:600px;height:3em;text-transform:uppercase',
                                'oninput': 'check_other()'
                                }),
             'proj_title'   : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'prj_lvl'      : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'ref_no'       : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'ptnt_sts'     : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_url'      : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        
        
        }
        
    def clean(self):
            cleaned_data = super(Prj_outcmForm, self).clean()
            prj_type = cleaned_data.get('prj_type')
            ptnt_sts = cleaned_data.get('ptnt_sts')
            prj_lvl = cleaned_data.get('prj_lvl')
            
            if prj_type == 'PTNT':
                if not cleaned_data['ptnt_sts']:
                    raise forms.ValidationError(u'Please select Patent Status!')           
                    
            if prj_lvl == "None":
                raise forms.ValidationError(u'Please select Level!')
            
            
            
    def __init__(self, *args, **kwargs):
            super(Prj_outcmForm,self).__init__(*args, **kwargs)
            self.fields['prj_lvl'].required = True
            
class Resch_guideForm(forms.ModelForm):
     
    class Meta:
        model = Resch_guide
        fields = "__all__"
                    
        widgets = {
             'student_name' : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'degree'       : widgets.Select(attrs={
                                'class':'form-control',
                                'style': 'width:600px;height:3em;text-transform:uppercase',
                                'oninput': 'check_option()'
                                }),             
             'title_thesis' : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'status'       : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_url'      : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        
        }

    def clean(self):
            cleaned_data = super(Resch_guideForm, self).clean()
            sts          = cleaned_data.get('status')
            degree       = cleaned_data.get('degree')
            
            
            # validating the status
            
            if degree != 'PHD':
                if sts == 'THES':                  
                   raise ValidationError(u'Check the degree please!')
               
  
    def __init__(self, *args, **kwargs):
        super(Resch_guideForm,self).__init__(*args, **kwargs)
        
        
class Fellow_AwardForm(forms.ModelForm):
     
    class Meta:
        model = Fellow_Award
        fields = "__all__"
                    
        widgets = {
             'fellow_type' : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'name_fellow' : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'name_body'   : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_lvl'     : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),             
             'prj_url'     : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Fellow_AwardForm,self).__init__(*args, **kwargs)
        
        
class Lecture_PaperForm(forms.ModelForm):
     
    class Meta:
        model = Lecture_Paper
        fields = "__all__"
                    
        widgets = {
             'invitation_type' : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'title_lecture'   : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'seminer'         : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'organizer'       : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'venue'           : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'duration'        : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_lvl'         : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),             
             'prj_url'         : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Lecture_PaperForm,self).__init__(*args, **kwargs)

class E_LearningForm(forms.ModelForm):
     
    class Meta:
        model = E_Learning
        fields = "__all__"
                    
        widgets = {
             'model_name'      : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'course_name'         : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'program_name'       : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_url'         : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(E_LearningForm,self).__init__(*args, **kwargs)

                           