# from asyncio.windows_events import NULL
# from http.client import REQUEST_ENTITY_TOO_LARGE
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.conf import settings
from account.models import Account, Academic, Research, PriorPost,PresentPost,TeachingExp,Orientation,ApiCatg_I, ApiCatg_II 
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.views.generic import TemplateView, ListView, CreateView, View
from django.db.models import Sum,Min,Max,Avg
from django.contrib.auth.decorators import login_required

from catg_3.models import Jrnl_pub,Pub_other,Resch_proj,Resch_cons,Prj_outcm


import os
from pathlib import Path

from io import BytesIO
from django.template.loader import get_template
# from django.views import View

from xhtml2pdf import pisa

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, AccountEditForm, ApiCatg_IForm, ApiCatg_IIForm
from account.forms import AccountCasForm, AcademyForm, ResearchForm, PrestsForm, PresentPostForm,TeachingExpForm, OrientationForm

global pk_var


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class AboutView(TemplateView):
    template_name = "account/about.html"

class NoticeView(TemplateView):
    template_name = "account/notification.html"



class ViewPDF(View):
    
	def get(self, request, *args, **kwargs):
            user_id = kwargs.get("user_id")
            
            account = Account.objects.get(pk=user_id)
            
            user = request.user
           
            
            act = Account.objects.get(pk=request.user.id)    
            admin = act.is_admin
            
            
            if account.is_admin:
                messages.success(request,"You can get PDF of your applicant's ! Pl.click on your member's row")
                # return HttpResponse(messages,"You are already authenticated as " + str(user.email))                
               
                # return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
                # return render(self.request, 'account/cas_view.html',"account:home", user_id=user.id)
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                # return redirect("account:home", user_id=request.user.id)
                
                
                # html = "<html><body><div><h1>Hi &nbsp&nbsp&nbsp <br>Sorry, you are not the Applicant ! <br> Please select the applicant preview buttom <br>%s.</h1></div></body></html>" % user.email
                # return HttpResponse(html) 

                
            # messeges = ""
            
            
            if Account.is_admin:
                account = Account.objects.get(pk=user_id)
                
            else:
                account = Account.objects.get(pk=request.user.id)  
            
    
            academy = account.academic_set.all()
            research = account.research_set.all()
            prests = account.priorpost_set.all()
            curpost = account.presentpost_set.all()
            teach = account.teachingexp_set.all()
            orient = account.orientation_set.all()
            api1 = ApiCatg_I.objects.get(pk=user_id)
            api2 = ApiCatg_II.objects.get(pk=user_id)
            jrnl = account.jrnl_pub_set.all()
            pub = account.pub_other_set.all()
            res = account.resch_proj_set.all()
            cons = account.resch_cons_set.all()
            prj = account.prj_outcm_set.all()
            res_guide = account.resch_guide_set.all()
            fellow = account.fellow_award_set.all()
            lec = account.lecture_paper_set.all()
            elearn = account.e_learning_set.all()
            
            api_t=0
            
            api_1=(api1.self_api_dt+api1.self_api_ed+api1.self_api_it)
            api_2=(api2.self_api_fba+api2.self_api_clm+api2.self_api_pda)
            
                
            # Summary of API I Category
            
            if account.to_dsg == 'Stage 2' or account.to_dsg == 'Stage 3':
                api_factor = 7.50
                dt_marks=70
                
                if (api_1 < 80):                   
                    api_sts1 = "Min Score not attained"				
                else:			
                    api_sts1 = "Criteria Satisfied"
                    api_t=api_t+1
                    
            else :
                api_factor = 7.75
                dt_marks=60
                
                if account.to_dsg == 'Stage 4':
                    if (api_1 < 75):				
                        api_sts1 = "Min Score not attained"
                    else:
                        api_sts1 = "Criteria Satisfied"
                        api_t=api_t+1
                        
                if account.to_dsg == 'Stage 5':
                    if (api_1 < 70):				
                        api_sts1 = "Min Score not attained"
                    else:
                        api_sts1 = "Criteria Satisfied"
                        api_t=api_t+1
			   
                
            
            if account.to_dsg == 'Stage 2' or account.to_dsg == 'Stage 3' or account.to_dsg == 'Stage 4':
                ed_factor = 10
                ed_marks=20
            else :
                ed_factor = 10
                ed_marks=10     
            
            if account.to_dsg == 'Stage 2' or account.to_dsg == 'Stage 3':
                it_factor = 10
                it_marks = 10
            elif account.to_dsg == 'Stage 4':
                it_factor = 10
                it_marks = 15
            else:
                it_factor = 10
                it_marks = 20 
                
            # Summary of API II Category
            api_2a=0
            api_2a=api_2*account.ass_yr
            
            if (api_2a < 50):
                api2_sts = "Min Score not attained"
            else:        
                api2_sts = "Criteria Satisfied"
                api_t=api_t+1
                
                
            # API III-A.  Journal Publication
            tot_3a=0 
            tot_3=0    
            tot_3a=jrnl.aggregate(Sum('self_api_score'))
            val=list(tot_3a.values())
            tot_3=tot_3+val[0]
            
            # API III-B : Publications other than journal articles
            tot_3b=0   
            tot_3b=pub.aggregate(Sum('self_api_score'))
            val=list(tot_3b.values())
            tot_3=tot_3+val[0]
            
            
            # API III-C (i):  Sponsored Project            
            tot_3c=0   
            tot_3c=res.aggregate(Sum('self_api_score'))
            val=list(tot_3c.values())
            tot_3=tot_3+val[0]
            
            # API III-C (ii):  Consultancy Project            
            tot_3d=0   
            tot_3d=cons.aggregate(Sum('self_api_score'))
            val=list(tot_3d.values())
            tot_3=tot_3+val[0]
            
            # API III-C (iii):  Projects Outcome/Output            
            tot_3e=0   
            tot_3e=prj.aggregate(Sum('self_api_score'))
            val=list(tot_3e.values())
            tot_3=tot_3+val[0]
            
            
            # API III-D:  Research Guidance            
            tot_3f=0   
            tot_3f=res_guide.aggregate(Sum('self_api_score'))
            val=list(tot_3f.values())
            tot_3=tot_3+val[0]
            
            # API III-E : (i)  Fellowship / Award from Academic Bodies/Associations            
            tot_3g=0   
            tot_3g=fellow.aggregate(Sum('self_api_score'))
            val=list(tot_3g.values())
            tot_3=tot_3+val[0]
            
           
            # API III-E : (ii) Invited Lecture / Paper presented            
            tot_3h=0   
            tot_3h=lec.aggregate(Sum('self_api_score'))
            val=list(tot_3h.values())
            tot_3=tot_3+val[0]

            # API IIIE (iii) e-Learning Delivery Process/Material            
            tot_3i=0   
            tot_3i=elearn.aggregate(Sum('self_api_score'))
            val=list(tot_3i.values())
            tot_3=tot_3+val[0]
            
            tot_sts3=""
            
            # Summary of API III Category
            if account.to_dsg == 'Stage 2':
                if (tot_3 < 20) :
                    tot_sts3 = "Min Score not attained"
                else:
                    tot_sts3 = "Criteria Satisfied"
                    
            if account.to_dsg == 'Stage 3':
                if (tot_3 < 50) :
                    tot_sts3 = "Min Score not attained"
                else:
                    tot_sts3 = "Criteria Satisfied"
                    
            if account.to_dsg == 'Stage 4':
                if (tot_3 < 75) :
                    tot_sts3 = "Min Score not attained"
                else:
                    tot_sts3 = "Criteria Satisfied"
                    
            if account.to_dsg == 'Stage 5':
                if (tot_3 < 100) :
                    tot_sts3 = "Min Score not attained"
                else:
                    tot_sts3 = "Criteria Satisfied"
        
            tot_2_3=0        
            tot_2_3=api_2a+tot_3
            
            
            context={}            
    
            if account :   
                        context['id'] = account.id
                        context['emp_id'] = str(account.emp_id).zfill(6)                       
                        context['username'] = account.username.upper()
                        context['email'] = account.email
                        context['parent'] = account.parent
                        context['catg'] = account.get_catg_display
                        context['Department'] = account.Department
                        context['Designation'] = account.get_Designation_display
                        context['from_dsg'] = account.get_from_dsg_display
                        context['to_dsg'] = account.get_to_dsg_display
                        context['pan_no'] = account.pan_no
                        context['is_pwd'] = account.is_pwd
                        context['pwd_link'] = account.pwd_link
                        context['agp'] = account.get_agp_display
                        context['dt_last_promo'] = account.dt_last_promo
                        context['dt_eligibility'] = account.dt_eligibility
                        context['addr_corres'] = account.addr_corres
                        context['addr_perm'] = account.addr_perm
                        context['mobile'] = account.mobile
                        context['highest_quali'] = account.get_highest_quali_display
                        context['ass_yr'] = account.ass_yr
                        context['gender'] = account.get_gender_display
                        context['dt_ob'] = account.dt_ob
                        context['date_joined'] = account.date_joined
                        context['quali_year'] = account.quali_year
                        context['tot_experience'] = account.tot_experience
                        context['doc_link'] = account.doc_link                       
                        context['pdf'] = account.pdf
                        context['academy'] = academy
                        context['research'] = research
                        context['prests'] = prests
                        context['curpost'] = curpost
                        context['teach'] = teach
                        context['orient'] = orient
                        context['api1'] = api1
                        context['dt_marks'] = dt_marks
                        context['ed_marks'] = ed_marks
                        context['it_marks'] = it_marks
                        context['admin'] = admin
                        context['api2'] = api2
                        context['jrnl'] = jrnl
                        context['pub'] = pub
                        context['res'] = res
                        context['cons'] = cons
                        context['prj'] = prj
                        context['res_guide'] = res_guide
                        context['fellow'] = fellow
                        context['lec'] = lec
                        context['elearn'] = elearn
                        context['api_1'] = api_1
                        context['api_sts1'] = api_sts1
                        context['api_2'] = api_2
                        context['api_2a'] = api_2a
                        context['api2_sts'] = api2_sts                       
                        context['tot_3a'] = tot_3a
                        context['tot_3b'] = tot_3b
                        context['tot_3c'] = tot_3c
                        context['tot_3d'] = tot_3d
                        context['tot_3e'] = tot_3e
                        context['tot_3f'] = tot_3f
                        context['tot_3g'] = tot_3g
                        context['tot_3h'] = tot_3h
                        context['tot_3i'] = tot_3i
                        context['tot_3'] = tot_3
                        context['tot_sts3'] = tot_sts3
                        context['tot_2_3'] = tot_2_3
                        
                        pdf = render_to_pdf('account/pdf_template.html', context)
                        #resp = HttpResponse(content_type='application/pdf',context)
                        #result = generate_pdf('account/pdf_template.html', file_object=resp)
                        #return result
                        return HttpResponse(pdf, content_type='application/pdf')
                        


id_var = 0 


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("logout")    
        #return HttpResponse("You are already authenticated as " + str(user.email))
        
    
    context={}
    
    if request.POST:
        form = RegistrationForm(request.POST)        
        if form.is_valid():
            form.save()            
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')            
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            # destination = get_redirect_if_exists(request)
            destination = kwargs.get("next")
            
            if destination:
                return redirect(destination)
            messages.success(request,'You have successfully signed up!')
            
            subject = 'Welcome to  JU CAS Application'
            message = 'You have successfully registered to Jadavpur University CAS Application software!'

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [account.email],
                fail_silently=False,
            )
            return redirect("account:home", user_id=request.user.id)
            
            
        else:
            context['registration_form'] = form
                   
            #return redirect(request.path) 
           

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/new_login.html', context)


def logout_view(request):
    logout(request)
    return redirect("register")


def login_view(request, *args, **kwargs):
    context = {}
    	
    user = request.user
    
   
        
    if user.is_authenticated:
        return redirect("account:home", user_id=request.user.id)
   
        
    destination=get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("account:home", user_id=request.user.id)
        else:
            #return HttpResponse("Login is not valid try again")
            return render(request, "account/login_error.html")  
            #return redirect("register")
        
        
        
    else:
        form = AccountAuthenticationForm()
	
 
    context['login_form'] = form
    
    return render(request, "account/new_login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def account_view(request, *args, **kwargs):
    """
    - Logic here is kind of tricky
            is_self (boolean)
                    is_friend (boolean)
                            -1: NO_REQUEST_SENT
                            0: THEM_SENT_TO_YOU
                            1: YOU_SENT_TO_THEM
    """
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        pass
        # account = Account.objects.all()
        # return HttpResponse("Something went wrong line-102 ???.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
        context['last_login'] = account.last_login
        context['Department'] = account.Department
        context['Designation'] = account.get_Designation_display
        context['pan_no'] = account.pan_no
        context['highest_quali'] = account.highest_quali
        context['gender'] = account.get_gender_display
        context['dt_ob'] = account.dt_ob
        context['date_joined'] = account.date_joined
        context['quali_year'] = account.quali_year
        context['tot_experience'] = account.tot_experience
        context['pdf'] = account.pdf
        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "account/account.html", context)


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)

    if request.method == "GET":
        if user_id == 0:
            form = AccountUpdateForm()
        else:
            account = Account.objects.get(pk=user_id)
            form = AccountUpdateForm(instance=account)
        return render(request, "account/edit2_account.html", {'form': form})

    else:
        if user_id == 0:
            form = AccountUpdateForm(request.POST)
        else:
            account = Account.objects.get(pk=user_id)
            form = AccountUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
        # return redirect("account:view", pk=account.id)
        return redirect("account:view", user_id=account.pk)


def cas_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    
     
    
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id
    	
    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = AccountCasForm()
        else:
            accounts = Account.objects.get(pk=user_id)
            form = AccountCasForm(instance=account)

            academy = accounts.academic_set.all()
            
            context['pdf'] = account.pdf
                        
            context = {
                'form': form,
                'academy': academy,
                'pk_var': pk_var,
                'user_var': user_var,
                'accounts' : accounts,
                   
            }
        
        return render(request, "account/cas_register.html", context)

    else:
        if user_id == 0:
            form = AccountCasForm(request.POST)
        else:
            account = Account.objects.get(pk=user_id)
            form = AccountCasForm(request.POST, request.FILES, instance=account)

        if form.is_valid():
            account.frm_general_info = True
            print(form.cleaned_data["is_pwd"])            
            form.save()
            messages.success(request,('Record has been saved successfully!'))
       
                
        return redirect(request.path)
        #return redirect("account:academy", user_id=account.id)
    
@login_required
def self_view(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
    
    account = Account.objects.get(pk=user_id)
    user = request.user
    
    if user != account.id:
        HttpResponseForbidden('You cannot view what is not yours') #Or however you want to handle this
 
    global pk_var     
    pk_var=user_id
      
    
    context = {}
    context['pk_var'] = pk_var
    context['username'] = account.username
    context['email'] = account.email
    context['Department'] = account.Department    
    context['Designation'] = account.get_Designation_display()
    context['faculty'] = account.get_faculty_display()
    context['is_hod'] = account.is_hod 
    context['is_applicant'] = account.is_applicant
    
    try:
        if not user.is_applicant:
            account = Account.objects.all()
            context = {'account': account}
            context['pk_var'] = pk_var

        else:
            account = Account.objects.get(pk=user_id)
            academy = Academic.objects.get(pk=user_id)
            if account:
                context['pk_var'] = pk_var
                context['id'] = account.id
                context['username'] = account.username
                context['email'] = account.email
                context['Department'] = account.Department                
                context['Designation'] = account.get_Designation_display()                
                context['faculty'] = account.get_faculty_display()

                if academy:
                    context['email_id'] = academy.id
                    context['degree'] = academy.degree
                    context['name_board_university'] = academy.name_board_university
    except:
        account = Account.objects.get(pk=user_id)
        academy=Academic.objects.create(pk=user_id,email_id=user_id).save()
        if academy:
            context['email_id'] = academy.id
            context['degree'] = academy.degree
            context['name_board_university'] = academy.name_board_university
            return render(request, 'account/cas_view.html', context)
        
        
        
        
        # return HttpResponse("Something went wro???.")
    
    return render(request, "account/cas_view.html", context)


def academy_view(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id
     
    account = Account.objects.get(pk=user_id)
    
    c=0
    
    context = {}
    
    
    
    if request.method == "GET":
        if user_id == 0:
            form = AcademyForm()
        else:
           
            try :
                
                academy = Academic.objects.get(pk=user_id)
               
                
            except Academic.DoesNotExist:                                    
                academy=Academic.objects.create(pk=user_id,email_id=user_id).save()
                
            else:
                pass        
               
                    
            form = AcademyForm(instance=academy)
              
            acad = account.academic_set.all()
            
            research = account.research_set.all()
            
            if research.count() == 0:
               research=Research.objects.create(pk=user_id,email_id=user_id).save()  
               research = account.research_set.all() 
            
            acad_count = acad.count()
               
            context = {
                'form': form,
                'acad': acad,
                'research': research,               
                'acad_count': acad_count,
                'pk_var': pk_var,
                'user_var': user_var,
            }

        return render(request, "account/next_register.html", context)

    else:
        if user_id == 0:
            form = AcademyForm(request.POST)
        else:
            academy = Academic.objects.get(email_id=user_id)
            form = AcademyForm(request.POST, instance=academy)

        if form.is_valid():
            form.save()
        return redirect("account:home", user_id=academy.pk)


def academy_edit(request, pk):
    academy = Academic.objects.get(id=pk)
    
    form1 = AcademyForm(instance=academy)
    user_id=academy.email_id
    acad_id=academy.id
  
           
    
    if request.method == 'POST':
         
            form1 = AcademyForm(request.POST, request.FILES, instance=academy)
            if form1.is_valid():
                form1.save() 
                #messages.success(request,('Record has been added successfully!'))                
                #return redirect(request.path)                
                return redirect("account:academy", user_id=academy.email_id)
               
    
    context = {
        'form1': form1,
        'user_id': user_id,
        'acadid': acad_id,
        
        }
    
    return render(request, 'account/next_register1.html', context)


def academy_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
    
    academy=Academic.objects.create(email_id=request.user.id)    
    academy.save()
    
    global id_var 
    id_var=academy.id
    global edit
    edit="Add"
    
       
    return redirect("account:academy-edit", pk=academy.id)


def academy_delete(request, pk):
    academy = Academic.objects.get(id=pk)
    
    if request.method == "POST":
        academy.delete()
        return redirect("account:academy", user_id=academy.email_id)
    
    context = {'item':academy}
    return render(request, 'account/delete.html', context)


def academy_cancel(request, *args, **kwargs):
    
    academy=Academic.objects.get(id=id_var)
    academy.delete()
    
    return redirect("account:academy", user_id=academy.email_id)

def research_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
    research=Research.objects.create(email_id=request.user.id)    
    research.save()
    global id_var 
    id_var=research.id
        
    return redirect("account:research-edit", pk=research.id)

def research_edit(request, pk):
    research = Research.objects.get(id=pk)
    
    form2 = ResearchForm(instance=research)
    user_id=research.email_id
    
    if request.method == 'POST':
            form2 = ResearchForm(request.POST,request.FILES, instance=research)
            if form2.is_valid():
                form2.save()
                return redirect("account:academy", user_id=research.email_id)
                
    context = {
        'form2': form2,
        'user_id': user_id,
        }
    return render(request, 'account/next_register2.html', context)

def research_cancel(request, *args, **kwargs):
   
    research=Research.objects.get(id=id_var)
    research.delete() 
    
    return redirect("account:academy", user_id=research.email_id)


def academy_edit1(request, pk):
    academy = Academic.objects.get(id=pk)
    
    form1 = AcademyForm(instance=academy)
    user_id=academy.email_id
    acad_id=academy.id
    
    if request.method == 'POST':
            form1 = AcademyForm(request.POST, request.FILES, instance=academy)
            if form1.is_valid():
                form1.save()
                messages.success(request,('Record has been modified successfully!'))
                return redirect("account:academy", user_id=academy.email_id)
               
    
    context = {
        'form1': form1,
        'user_id': user_id,
        'acadid': acad_id,
        'academy': academy,
        
        }
    
    return render(request, 'account/edit_register.html', context)

def research_edit1(request, pk):
    research = Research.objects.get(id=pk)
    
    form2 = ResearchForm(instance=research)
    user_id=research.email_id
    
    if request.method == 'POST':
            form2 = ResearchForm(request.POST,request.FILES, instance=research)
            if form2.is_valid():
                form2.save()
                messages.success(request,('Record has been modified successfully!'))
                return redirect("account:academy", user_id=research.email_id)
                
    context = {
        'form2': form2,
        'user_id': user_id,
        }
    return render(request, 'account/edit_research.html', context)

def research_delete(request, pk):
    research = Research.objects.get(id=pk)
    
    if request.method == "POST":
        research.delete()
        return redirect("account:academy", user_id=research.email_id)
    
    context = {'item':research}
    return render(request, 'account/research_delete.html', context)

def prests_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
    prests=PriorPost.objects.create(email_id=request.user.id)    
    prests.save()
    
    global id_var 
    id_var=prests.id
        
    return redirect("account:prests-edit", pk=prests.id)

def prests_edit(request, pk):
    prests = PriorPost.objects.get(id=pk)
    
    form3 = PrestsForm(instance=prests)
    user_id=prests.email_id
    
    if request.method == 'POST':
            form3 = PrestsForm(request.POST,request.FILES, instance=prests)
            if form3.is_valid():
                form3.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("account:professional", user_id=prests.email_id)
                
    context = {
        'form3': form3,
        'user_id': user_id,
        }
    return render(request, 'account/next_register3.html', context)

def prests_edit1(request, pk):
    prests = PriorPost.objects.get(id=pk)
    
    form3 = PrestsForm(instance=prests)
    user_id=prests.email_id
    
    if request.method == 'POST':
            form3 = PrestsForm(request.POST,request.FILES, instance=prests)
            if form3.is_valid():
                form3.save()
                messages.success(request,('Record has been modified successfully!'))
                return redirect("account:professional", user_id=prests.email_id)
                
    context = {
        'form3': form3,
        'user_id': user_id,
        }
    return render(request, 'account/edit_prests.html', context)

def prests_delete(request, pk):
    prests = PriorPost.objects.get(id=pk)
    
    if request.method == "POST":
        prests.delete()
        return redirect("account:professional", user_id=prests.email_id)
    
    context = {'item':prests}
    return render(request, 'account/prests_delete.html', context)


def prests_cancel(request, *args, **kwargs):
   
    prests=PriorPost.objects.get(id=id_var)
    prests.delete() 
    
    return redirect("account:professional", user_id=prests.email_id)

def professional_view(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
   
    account = Account.objects.get(pk=user_id)
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
   
    context = {}
    
    prests = account.priorpost_set.all()
    
    
    if prests.count() == 0:
        prests=PriorPost.objects.create(pk=user_id,email_id=user_id).save()  
        prests = account.priorpost_set.all()
           
    curpost = account.presentpost_set.all()
    
    if curpost.count() == 0:
        curpost=PresentPost.objects.create(pk=user_id,email_id=user_id).save()  
        curpost = account.presentpost_set.all()
   
    context = {              
                'prests'  : prests,
                'curpost' : curpost,
                'pk_var': pk_var,
                'user_var': user_var,               
            }
    
    return render(request, "account/professional_register.html", context)


def curpost_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
    curpost=PresentPost.objects.create(email_id=request.user.id)    
    curpost.save()
    
    global id_var 
    id_var=curpost.id
        
    return redirect("account:curpost-edit", pk=curpost.id)

def curpost_edit(request, pk):
    curpost = PresentPost.objects.get(id=pk)
    
    form4 = PresentPostForm(instance=curpost)
    user_id=curpost.email_id
    
    
    if request.method == 'POST':
            form4 = PresentPostForm(request.POST,request.FILES, instance=curpost)
            if form4.is_valid():
                form4.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("account:professional", user_id=curpost.email_id)
                
    context = {
        'form4': form4,
        'user_id': user_id,
        
        }
    return render(request, 'account/next_register4.html', context)

def curpost_edit1(request, pk):
    curpost = PresentPost.objects.get(id=pk)
    
    form4 = PresentPostForm(instance=curpost)
    user_id=curpost.email_id
   
    
    if request.method == 'POST':
            form4 = PresentPostForm(request.POST,request.FILES, instance=curpost)
            if form4.is_valid():
                form4.save()
                messages.success(request,('Record has been modified successfully!'))
                return redirect("account:professional", user_id=curpost.email_id)
                
    context = {
        'form4': form4,
        'user_id': user_id,
        
        }
    return render(request, 'account/edit_curpost.html', context)

def curpost_delete(request, pk):
    curpost = PresentPost.objects.get(id=pk)
    
    if request.method == "POST":
        curpost.delete()
        return redirect("account:professional", user_id=curpost.email_id)
    
    context = {'item':curpost}
    return render(request, 'account/curpost_delete.html', context)


def curpost_cancel(request, *args, **kwargs):
   
    curpost=PresentPost.objects.get(id=id_var)
    curpost.delete() 
    
    return redirect("account:professional", user_id=curpost.email_id)

def teaching_view(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
    
    account = Account.objects.get(pk=user_id)
    
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
    
    teach = account.teachingexp_set.all()
    
    if teach.count() == 0:
        teach=TeachingExp.objects.create(pk=user_id,email_id=user_id).save()  
        teach = account.teachingexp_set.all()
    
    
    context = {}
    
    
     
    if request.method == "GET":
        if user_id == 0:
            form5 = TeachingExpForm()
        else:
            teach = TeachingExp.objects.get(pk=user_id)
            form5 = TeachingExpForm(instance=teach)
                        
            context = {
                'form5': form5,                
                'pk_var': pk_var,
                'user_var': user_var,
                'account' : account,
                'teach': teach,  
            }
        
        return render(request, "account/teaching_register.html", context)

    else:
        if user_id == 0:
            form5 = TeachingExpForm(request.POST)
        else:
            teach = TeachingExp.objects.get(pk=user_id)
            form5 = TeachingExpForm(request.POST, request.FILES, instance=teach)

        if form5.is_valid():            
            form5.save()
            messages.success(request,('Record has been saved successfully!'))
        else:
            messages.warning(request, "Invalid form")                
            messages.error(request, form5.errors) 
            
        return redirect(request.path)
        #return redirect("account:academy", user_id=account.id)



def teach_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
    teach=TeachingExp.objects.create(email_id=request.user.id)    
    teach.save()
    
    global id_var 
    id_var=teach.id
        
    return redirect("account:teach-edit", pk=teach.id)

def teach_edit(request, pk):
    teach = TeachingExp.objects.get(id=pk)
    
    form5 = TeachingExpForm(instance=teach)
    user_id=teach.email_id
    
    if request.method == 'POST':
            form5 = TeachingExpForm(request.POST,request.FILES, instance=teach)
            if form5.is_valid():
                form5.save()
                return redirect("account:teaching", user_id=teach.email_id)
                
    context = {
        'form5': form5,
        'user_id': user_id,
        }
    return render(request, 'account/next_register5.html', context)

def teach_edit1(request, pk):
    teach = TeachingExp.objects.get(id=pk)
    
    form5 = TeachingExpForm(instance=teach)
    user_id=teach.email_id
    
    if request.method == 'POST':
            form5 = TeachingExpForm(request.POST,request.FILES, instance=teach)
            if form5.is_valid():
                form5.save()
                return redirect("account:teaching", user_id=teach.email_id)
                
    context = {
        'form5': form5,
        'user_id': user_id,
        }
    return render(request, 'account/edit_teach.html', context)

def teach_delete(request, pk):
    teach = TeachingExp.objects.get(id=pk)
    
    if request.method == "POST":
        teach.delete()
        return redirect("account:teaching", user_id=teach.email_id)
    
    context = {'item':teach}
    return render(request, 'account/teach_delete.html', context)


def teach_cancel(request, *args, **kwargs):
   
    teach=TeachingExp.objects.get(id=id_var)
    teach.delete() 
    
    return redirect("account:teaching", user_id=teach.email_id)

def orient_view(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
   
    account = Account.objects.get(pk=user_id)
   
    
    global pk_var
    pk_var = user_id
     
    global user_var
    user_var = user_id 
    
    
    context = {}
          
    orient = account.orientation_set.all()
    
    if orient.count() == 0:
        orient = Orientation.objects.create(pk=user_id,email_id=user_id).save()  
        orient = account.orientation_set.all()
   
    context = {              
                'orient'  : orient,
                'pk_var'  : pk_var,
                'user_var' : user_var,                              
            }
    
    return render(request, "account/orientation_register.html", context)


def orient_edit(request, pk):
    orient = Orientation.objects.get(id=pk)
    
    form6 = OrientationForm(instance=orient)
    user_id=orient.email_id
    
    if request.method == 'POST':
            form6 = OrientationForm(request.POST,request.FILES, instance=orient)
            if form6.is_valid():
                form6.save()
                return redirect("account:orient", user_id=orient.email_id)
                
    context = {
        'form6': form6,
        'user_id': user_id,
        }
    return render(request, 'account/next_register6.html', context)


def orient_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
    orient = Orientation.objects.create(email_id=request.user.id)    
    orient.save()
    
    global id_var 
    id_var=orient.id
        
    return redirect("account:orient-edit", pk=orient.id)


def orient_cancel(request, *args, **kwargs):
   
    orient = Orientation.objects.get(id=id_var)
    orient.delete() 
    
    return redirect("account:orient", user_id=orient.email_id)

def orient_delete(request, pk):
    orient = Orientation.objects.get(id=pk)
    
    if request.method == "POST":
        orient.delete()
        return redirect("account:orient", user_id=orient.email_id)
    
    context = {'item':orient}
    return render(request, 'account/orient_delete.html', context)

def orient_edit1(request, pk):
    orient = Orientation.objects.get(id=pk)
    
    form6 = OrientationForm(instance=orient)
    user_id=orient.email_id
    
    if request.method == 'POST':
            form6 = OrientationForm(request.POST,request.FILES, instance=orient)
            if form6.is_valid():
                form6.save()
                return redirect("account:orient", user_id=orient.email_id)
                
    context = {
        'form6': form6,
        'user_id': user_id,
        }
    return render(request, 'account/edit_orient.html', context)


def cas_edit(request, pk):
    account = Account.objects.get(id=pk)
    
    form7 = AccountCasForm(instance=account)
    user_id=account.email
    
    if request.method == 'POST':
            form7 = AccountCasForm(request.POST,request.FILES, instance=account)
            if form7.is_valid():
                form7.save()
                return redirect("account:cas", user_id=account.id)
    context = {
        'form7': form7,
        'user_id': user_id,
        }
    return render(request, 'account/general_register.html', context)

def cas_edit1(request,pk):
    
    account = Account.objects.get(id=pk)
    
    form8 = AccountEditForm(instance=account)
    user_id=account.id
    pdf_url=account.pdf
   
    pdffile=account.pdf

    file= pdffile.filepath

    fullfilepath= "media/" + str(file)

    filesize= os.path.getsize(fullfilepath)

    form8 = AccountEditForm(request.POST)
    
    if request.method == 'POST':
            form8 = AccountEditForm(request.POST,request.FILES, instance=account)
            if form8.is_valid():               
                form8.save()
                return redirect("account:cas", user_id=account.id)
            else:
                return HttpResponse(form8.errors.values())  # Validation failed
                
    context={'pdf':account.pdf}
                     
    context = {
        'form8': form8,
        'user_id': user_id,
        'pdf_url':pdf_url,
        'account':account,
        'filesize': filesize,
        'file': file,
        }
    
    return render(request, 'account/edit_general.html', context)

def api1_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    try:
        api1 = ApiCatg_I.objects.get(pk=user_id)
    except ApiCatg_I.DoesNotExist:
        api1=ApiCatg_I.objects.create(pk=user_id,email_id=user_id).save()  
        #pass
        # account = Account.objects.all()
        #return HttpResponse("Something went wrong line-1063 ???.")
        return redirect(request.path)
        
      
    account = Account.objects.get(pk=user_id) # applicant row
    act = Account.objects.get(pk=request.user.id) # admin row
    admin=act.is_admin
   
    
    if account.to_dsg == 'Stage 2' or account.to_dsg == 'Stage 3':
        api_factor = 7.50
        dt_marks=70
    else :
        api_factor = 7.75
        dt_marks=60 
    
    if account.to_dsg == 'Stage 2' or account.to_dsg == 'Stage 3' or account.to_dsg == 'Stage 4':
        ed_factor = 10
        ed_marks=20
    else :
        ed_factor = 10
        ed_marks=10     
    
    if account.to_dsg == 'Stage 2' or account.to_dsg == 'Stage 3':
        it_factor = 10
        it_marks = 10
    elif account.to_dsg == 'Stage 4':
        it_factor = 10
        it_marks = 15
    else:
        it_factor = 10
        it_marks = 20 
    
    tot_marks = dt_marks + ed_marks + it_marks
    tot_self_api = 0
    tot_veri_api = 0
    
    if api1.self_api_dt :
        tot_self_api = api1.self_api_dt 
   
    if api1.self_api_ed :
        tot_self_api += api1.self_api_ed
        
    if api1.self_api_it :    
        tot_self_api += api1.self_api_it 
       
    
    if api1.veri_api_dt:
        tot_veri_api = api1.veri_api_dt 
    if api1.veri_api_ed :
        tot_veri_api += api1.veri_api_ed
    if api1.veri_api_it :    
        tot_veri_api += api1.veri_api_it 
    
    
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id
    	
    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = ApiCatg_IForm()
        else:
            api1 = ApiCatg_I.objects.get(pk=user_id)
            form = ApiCatg_IForm(instance=api1)

                        
            context = {
                'form': form,
                'pk_var': pk_var,
                'user_var': user_var,
                'account' : account,
                'api_factor':api_factor,
                'dt_marks': dt_marks,
                'api1':api1,
                'ed_factor':ed_factor,
                'ed_marks':ed_marks,
                'it_factor':it_factor,
                'it_marks':it_marks,
                'tot_marks':tot_marks,
                'tot_self_api' : tot_self_api,
                'tot_veri_api' : tot_veri_api,
                'admin':admin
            }
        
        return render(request, "account/api_catg1.html", context)

    else:
        if user_id == 0:
            form = ApiCatg_IForm(request.POST)
        else:
            api1 = ApiCatg_I.objects.get(pk=user_id)
            form = ApiCatg_IForm(request.POST, request.FILES, instance=api1)

        if form.is_valid():
           form.save()
           messages.success(request,('Record has been modified successfully!'))
        return redirect(request.path)
        #return redirect("account:home", user_id=api1.id)
        


def api2_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    try:
        api2 = ApiCatg_II.objects.get(pk=user_id)
    except ApiCatg_II.DoesNotExist:
        api2=ApiCatg_II.objects.create(pk=user_id,email_id=user_id).save()  
        pass
        # account = Account.objects.all()
        #return HttpResponse("Go Back and Try again!")
        return redirect(request.path)
      
    account = Account.objects.get(pk=user_id)
    act = Account.objects.get(pk=request.user.id) # admin row
    admin=act.is_admin
    
    api_factor = 10
    fba_marks=15
    clm_marks=15
    pda_marks=15
    
    tot_marks = fba_marks + clm_marks + pda_marks
    tot_self_api = 0
    tot_veri_api = 0
    
    if api2.veri_api_fba:
        tot_veri_api = api2.veri_api_fba 
    if api2.veri_api_clm :
        tot_veri_api += api2.veri_api_clm
    if api2.veri_api_pda :    
        tot_veri_api += api2.veri_api_pda 
    
    if api2.self_api_fba:
        tot_self_api = api2.self_api_fba 
    if api2.self_api_clm :
        tot_self_api += api2.self_api_clm
    if api2.self_api_pda :    
        tot_self_api += api2.self_api_pda 
    
    
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id
    	
    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = ApiCatg_IIForm()
        else:
            api2 = ApiCatg_II.objects.get(pk=user_id)
            form = ApiCatg_IIForm(instance=api2)

                        
            context = {
                'form': form,
                'pk_var': pk_var,
                'user_var': user_var,
                'account' : account,
                'api_factor':api_factor,
                'fba_marks': fba_marks,
                'api2':api2,                
                'clm_marks':clm_marks,                
                'pda_marks':pda_marks,
                'tot_marks':tot_marks,
                'tot_self_api' : tot_self_api,
                'tot_veri_api' : tot_veri_api,
                'admin':admin,
            }
        
        return render(request, "account/api_catg2.html", context)

    else:
        if user_id == 0:
            form = ApiCatg_IIForm(request.POST)
        else:
            api1 = ApiCatg_II.objects.get(pk=user_id)
            form = ApiCatg_IIForm(request.POST, request.FILES, instance=api2)

        if form.is_valid():
           form.save()
        return redirect(request.path)
        #return redirect("account:home", user_id=api2.id)

       