from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse,HttpRequest
from django.forms import formset_factory
from django.test import tag
from . models import Jrnl_pub,Pub_other,Resch_proj,Resch_cons,Prj_outcm, Resch_guide,Fellow_Award,Lecture_Paper,E_Learning
from . forms import Jrnl_pubForm, Pub_otherForm,Resch_projForm,Prj_outcmForm, Resch_guideForm, Fellow_AwardForm,Lecture_PaperForm,E_LearningForm,Resch_consForm
from account.models import Account,ApiCatg_I,ApiCatg_II
from account.forms import AccountCasForm
from django.contrib import messages
from django.db.models import Avg,Min,Max,Sum
from django.views.generic import View

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa



# Create your views here.


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

def LetterView(request,*args, **kwargs):   
     
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    print (user_id)
    global pk_var
    pk_var = user_id    
    global user_var 
    user_var = user_id
     
    account = Account.objects.get(pk=user_id)
    form = AccountCasForm(instance=account)    
    context = {
                'account': account,
                'pk_var': pk_var,
                'user_var': user_var,
                'form':form,
                
            }
            
    
        
    return render(request, "catg_3/steps_for_final_submission.html", context)
    
   
    
class LetterPDF(View):
	def get(self, request, *args, **kwargs):
            user_id = kwargs.get("user_id")
            
            account = Account.objects.get(pk=user_id)
            user = request.user
            global pk_var 
            
            if account.is_admin:
                messages.success(request,"You can get PDF of your applicant's ! Pl.click on your member's row")
                
            if Account.is_admin:
                account = Account.objects.get(pk=user_id)
            else:
                account = Account.objects.get(pk=request.user.id)  
            
    
            context={}
    
    
            if account :
                        context['username'] = account.username.upper()                        
                        context['Department'] = account.Department                        
                        context['from_dsg'] = account.get_from_dsg_display
                        context['to_dsg'] = account.get_to_dsg_display
                         
                        pdf = render_to_pdf('catg_3/pdf_endoltr.html', context)
                        
                        return HttpResponse(pdf, content_type='application/pdf')





    

def jrnl_view(request,*args, **kwargs):
    
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
            form = Jrnl_pubForm()
        else:           
            try :                
                jrnl = Jrnl_pub.objects.get(pk=user_id)                
            except Jrnl_pub.DoesNotExist:                                    
                jrnl=Jrnl_pub.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Jrnl_pubForm(instance=jrnl)              
            jrnl = account.jrnl_pub_set.all()
            
            jrnl_count = jrnl.count()            
            
            context = {
                'form': form,
                'jrnl': jrnl,                            
                'jrnl_count': jrnl_count,
                'pk_var': pk_var,
                'user_var': user_var,
                
            }

        return render(request, "catg_3/jrnl_pub.html", context)

    else:
        if user_id == 0:
            form = Jrnl_pubForm(request.POST)
        else:
            jrnl = Jrnl_pub.objects.get(email_id=user_id)
            form = Jrnl_pubForm(request.POST, instance=jrnl)

        if form.is_valid():
            form.save()
        return redirect("account:home", user_id=jrnl.pk) 

def jrnl_edit(request, pk):
    jrnl = Jrnl_pub.objects.get(id=pk)
    
    form1 = Jrnl_pubForm(instance=jrnl)
    user_id=jrnl.email_id
    jrnl_id=jrnl.id
    
    if request.method == 'POST':
            form1 = Jrnl_pubForm(request.POST, request.FILES, instance=jrnl)
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
            
            # else:
                # messages.warning(request, "Invalid form")                
                # messages.error(request, form1.errors)
             
                
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'jrnl_id': jrnl_id,
        'jrnl':jrnl,
        
        }
    
    return render(request, 'catg_3/edit_jrnlpub.html', context)
    

def jrnl_add1(request, pk):
    jrnl = Jrnl_pub.objects.get(id=pk)    
    form1 = Jrnl_pubForm(instance=jrnl)
    user_id=jrnl.email_id
    jrnl_id=jrnl.id
    js=0
    jrnl_type=""
    imp_fac=0
    
    if request.method == 'POST':
         
            form1 = Jrnl_pubForm(request.POST, request.FILES, instance=jrnl)
            if form1.is_valid():                            
                # no_auth = form1.cleaned_data('no_auth')
                # role_appl = form1.cleaned_data('role_appl')
                        
                    
                form1.save()                
                messages.error(request,('Record has been added successfully!'))
                return redirect("jrnl-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
               
    
    context = {
        'form1': form1,
        'user_id': user_id,
        'jrnl_id': jrnl_id,           
              
        
        }
    
    return render(request, 'catg_3/jrnl_register1.html', context) #This is for adding new records


def jrnl_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
     
    jrnl=Jrnl_pub.objects.create(email_id=request.user.id)    
    jrnl.save()
    
    global id_var 
    id_var=jrnl.id
    global edit
    edit="Add"
    
    
    return redirect("catg_3:jrnl-add1", pk=jrnl.id)


def jrnl_cancel(request, *args, **kwargs):    
    jrnl=Jrnl_pub.objects.get(id=id_var)
    jrnl.delete()
    
    return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)

def jrnl_delete(request, pk):
    Jrnl = Jrnl_pub.objects.get(id=pk)
    
    if request.method == "POST":
        Jrnl.delete()
        return redirect("catg_3:jrnl-pub", user_id=Jrnl.email_id)
        
    context = {'item':Jrnl}
    return render(request, 'catg_3/jrnl_delete.html', context)


 #---------------IIIB Publications other than Journals-------------------


def jrnl_view(request,*args, **kwargs):
    
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
            form = Jrnl_pubForm()
        else:           
            try :                
                jrnl = Jrnl_pub.objects.get(pk=user_id)                
            except Jrnl_pub.DoesNotExist:                                    
                jrnl=Jrnl_pub.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Jrnl_pubForm(instance=jrnl)              
            jrnl = account.jrnl_pub_set.all()
            
            jrnl_count = jrnl.count()
               
            context = {
                'form': form,
                'jrnl': jrnl,                            
                'jrnl_count': jrnl_count,
                'pk_var': pk_var,
                'user_var': user_var,
            }

        return render(request, "catg_3/jrnl_pub.html", context)

    else:
        if user_id == 0:
            form = Jrnl_pubForm(request.POST)
        else:
            jrnl = Jrnl_pub.objects.get(email_id=user_id)
            form = Jrnl_pubForm(request.POST, instance=jrnl)

        if form.is_valid():
            form.save()
        return redirect("account:home", user_id=jrnl.pk) 




def pub_other_view(request,*args, **kwargs):
    
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
            form = Pub_otherForm()
        else:           
            try :                
                pub = Pub_other.objects.get(pk=user_id)                
            except Pub_other.DoesNotExist:                                    
                pub=Pub_other.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Pub_otherForm(instance=pub)              
            pub = account.pub_other_set.all()
            
            pub_count = pub.count()
               
            context = {
                'form': form,
                'pub': pub,                            
                'pub_count': pub_count,
                'pk_var': pk_var,
                'user_var': user_var,
            }

        return render(request, "catg_3/pub_other.html", context)

    else:
        if user_id == 0:
            form = Pub_otherForm(request.POST)
        else:
            pub = Pub_other.objects.get(email_id=user_id)
            form = Pub_otherForm(request.POST, instance=pub)

        if form.is_valid():
            form.save()
        return redirect("account:home", user_id=pub.pk) 

def pub_other_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
     
    pub=Pub_other.objects.create(email_id=request.user.id)    
    pub.save()
    
    global id_var 
    id_var=pub.id
    global edit
    edit="Add"
    
    # After adding a blank record and redirected to views for editing
    return redirect("catg_3:pub-add1", pk=pub.id)
   
def pub_add1(request, pk):

    pub = Pub_other.objects.get(id=pk)    
    form1 = Pub_otherForm(instance=pub)
    user_id=pub.email_id
    pub_id=pub.id
    
    
    if request.method == 'POST':
         
            form1 = Pub_otherForm(request.POST, request.FILES, instance=pub)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("pub-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
               
    
    context = {
        'form1': form1,
        'user_id': user_id,
        'pub_id': pub_id,           
              
        
        }
    return render(request, 'catg_3/pub_other_add.html', context)

def pub_edit(request, pk):
    pub = Pub_other.objects.get(id=pk)
    
    form1 = Pub_otherForm(instance=pub)
    user_id=pub.email_id
    pub_id=pub.id
    
    if request.method == 'POST':
            form1 = Pub_otherForm(request.POST, request.FILES, instance=pub)
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
           
                
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'pub_id': pub_id,
        'pub':pub,
        
        }
    
    return render(request, 'catg_3/edit_pub_other.html', context)


def pub_other_cancel(request, *args, **kwargs):    
    pub=Pub_other.objects.get(id=id_var)
    pub.delete()
    
    return redirect("catg_3:pub-other", user_id=pub.email_id)


def pub_delete(request, pk):
    pub = Pub_other.objects.get(id=pk)
    
    if request.method == "POST":
        pub.delete()
        return redirect("catg_3:pub-other", user_id=pub.email_id)
        
    context = {'item':pub}
    return render(request, 'catg_3/pub_delete.html', context)



def resch_proj_view(request,*args, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
   
    global pk_var
    pk_var = user_id    
    global user_var
    user_var = user_id
    global prj_tg
    prj_tg="abc"
    
    
    account = Account.objects.get(pk=user_id)    
     

    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = Resch_projForm()
        else:           
            try :                
                res = Resch_proj.objects.get(pk=user_id)                
            except Resch_proj.DoesNotExist:                                    
                res = Resch_proj.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Resch_projForm(instance=res)              
            res = account.resch_proj_set.all()
            cons = account.resch_cons_set.all()
            prj = account.prj_outcm_set.all()
            res_count = res.count()
                 
            context = {
                'form': form,
                'res': res,
                'cons':cons,                
                'res_count': res_count,
                'pk_var': pk_var,
                'user_var': user_var,
                'prj':prj_tg,
                'prj': prj,
                
            }
        
        return render(request, "catg_3/resch_proj.html", context)


def resch_sponsor_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
        
    res=Resch_proj.objects.create(email_id=request.user.id,proj_tag="spon")    
    res.save()
    
    global id_var 
    id_var=res.id
    global edit
    edit="spon"
   
    
    
    # After adding a blank record and redirected to views for editing
    return redirect("catg_3:resch-add1", pk=res.id)

def resch_cons_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_id = kwargs.get("user_id")
    
        
    cons=Resch_cons.objects.create(email_id=request.user.id,proj_tag="cons")    
    cons.save()
    
    global id_var 
    id_var=cons.id
    global edit
    edit="cons"
    
    # After adding a blank record and redirected to views for editing
    return redirect("catg_3:resch-cons-add1", pk=cons.id)
     
def resch_add1(request, pk):

    res = Resch_proj.objects.get(id=pk)    
    form1 = Resch_projForm(instance=res)
    user_id=res.email_id
    res_id=res.id
    
    global edit
    
    if request.method == 'POST':
         
            form1 = Resch_projForm(request.POST, request.FILES, instance=res)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("resch-sponsor-add")
              
    
    context = {
        'form1': form1,
        'user_id': user_id,
        'res_id': res_id,
        
        'res': res,
        
        }
    return render(request, 'catg_3/resch_proj_add.html', context)
    
     
def resch_cons_add1(request, pk):

    cons = Resch_cons.objects.get(id=pk)    
    form1 = Resch_consForm(instance=cons)
    user_id=cons.email_id
    cons_id=cons.id
    
    global edit
    
    if request.method == 'POST':
         
            form1 = Resch_consForm(request.POST, request.FILES, instance=cons)
            if form1.is_valid():
                form1.save()
                messages.success(request,('Record has been added successfully!'))                
                return redirect("resch-cons-add")
                    
              
    
    context = {
        'form1': form1,
        'user_id': user_id,
        'cons_id': cons_id,               
        'cons': cons,
        }
    
    return render(request, 'catg_3/resch_cons_add.html', context)
      
    
    

def resch_edit(request, pk):
    res = Resch_proj.objects.get(id=pk)
    
    form1 = Resch_projForm(instance=res)
    user_id=res.email_id
    res_id=res.id
    
    if request.method == 'POST':
            form1 = Resch_projForm(request.POST, request.FILES, instance=res)
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
            
                
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'res_id': res_id,
        'res':res,
        
        }
    
    return render(request, 'catg_3/edit_resch_proj.html', context)
    
    

def resch_cons_edit(request, pk):
    cons = Resch_cons.objects.get(id=pk)
    
    form1 = Resch_consForm(instance=cons)
    user_id=cons.email_id
    cons_id=cons.id
    
    if request.method == 'POST':
            form1 = Resch_consForm(request.POST, request.FILES, instance=cons)
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
            
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'cons_id': cons_id,
        'cons':cons,
        
        }
    
    return render(request, 'catg_3/edit_resch_cons.html', context)    

def resch_cancel(request, *args, **kwargs):    
    res=Resch_proj.objects.get(id=id_var)
    res.delete()
    
    return redirect("catg_3:resch-view", user_id=res.email_id)
    

def resch_cons_cancel(request, *args, **kwargs):    
    res=Resch_cons.objects.get(id=id_var)
    res.delete()
    
    return redirect("catg_3:resch-view", user_id=res.email_id)    

def resch_delete(request, pk):
    res = Resch_proj.objects.get(id=pk)
    
    if request.method == "POST":
        res.delete()
        return redirect("catg_3:resch-view", user_id=res.email_id)
        
    context = {'item':res}
    return render(request, 'catg_3/resch_delete.html', context)
    
def resch_cons_delete(request, pk):
    res = Resch_cons.objects.get(id=pk)
    
    if request.method == "POST":
        res.delete()
        return redirect("catg_3:resch-view", user_id=res.email_id)
        
    context = {'item':res}
    return render(request, 'catg_3/resch_cons_delete.html', context)    


def prj_outcm_view(request,*args, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
   
    global pk_var
    pk_var = user_id    
    global user_var
    user_var = user_id
    
    account = Account.objects.get(pk=user_id)    
    

    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = Prj_outcmForm()
        else:           
            try :                
                prj = Prj_outcm.objects.get(pk=user_id)                
            except Prj_outcm.DoesNotExist:                                    
                prj = Prj_outcm.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Prj_outcmForm(instance=prj)              
            prj = account.prj_outcm_set.all()
            
            prj_count = prj.count()
               
            context = {
                'form': form,
                'prj': prj,                            
                'prj_count': prj_count,
                'pk_var': pk_var,
                'user_var': user_var,
                
            }

        return render(request, "catg_3/resch_proj.html", context)

    else:
        if user_id == 0:
            form = Prj_outcmForm(request.POST)
        else:
            prj = Prj_outcm.objects.get(email_id=user_id)
            form = Prj_outcmForm(request.POST, instance=prj)

        if form.is_valid():
            form.save()
        return redirect("account:home", user_id=prj.pk) 


def prj_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    prj=Prj_outcm.objects.create(email_id=request.user.id)    
    prj.save()
    
    global id_var 
    id_var=prj.id
    
    # After adding a blank record and redirected to views for editing
    
    return redirect("catg_3:prj-add1", pk=prj.id)

def prj_add1(request, pk):

    prj = Prj_outcm.objects.get(id=pk)    
    form1 = Prj_outcmForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    
    if request.method == 'POST':
         
            form1 = Prj_outcmForm(request.POST, request.FILES, instance=prj)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("prj-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
        
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj': prj,
        
        }
    return render(request, 'catg_3/prj_add.html', context)

def prj_cancel(request, *args, **kwargs):    
    prj=Prj_outcm.objects.get(id=id_var)
    prj.delete()
    
    return redirect("catg_3:resch-view", user_id=prj.email_id)

def prj_delete(request, pk):
    prj = Prj_outcm.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:resch-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/prj_delete.html', context)


def prj_edit(request, pk):
    prj = Prj_outcm.objects.get(id=pk)
    
    form1 = Prj_outcmForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Prj_outcmForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.success(request,('Record has been modified succesfully!')) 
                #return redirect("catg_3:resch-view", user_id=prj.email_id)                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_prj_outcm.html', context)
    
    
def resch_guide_view(request,*args, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
   
    global pk_var
    pk_var = user_id    
    global user_var
    user_var = user_id
    
    account = Account.objects.get(pk=user_id)    
    

    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = Resch_guideForm()
        else:           
            try :                
                prj = Resch_guide.objects.get(pk=user_id)                
            except Resch_guide.DoesNotExist:                                    
                prj = Resch_guide.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Resch_guideForm(instance=prj)              
            prj = account.resch_guide_set.all()
            
            prj_count = prj.count()
               
            context = {
                'form': form,
                'prj': prj,                            
                'prj_count': prj_count,
                'pk_var': pk_var,
                'user_var': user_var,
                
            }

        return render(request, "catg_3/resch_guide.html", context)

    else:
        if user_id == 0:
            form = Resch_guideForm(request.POST)
        else:
            prj = Resch_guide.objects.get(email_id=user_id)
            form = Resch_guideForm(request.POST, instance=prj)

        if form.is_valid():
            form.save()
        return redirect("account:home", user_id=prj.pk)


def resch_guide_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    prj=Resch_guide.objects.create(email_id=request.user.id)    
    prj.save()
    
    global id_var 
    id_var=prj.id
    
    # After adding a blank record and redirected to views for editing
    
    return redirect("catg_3:resch-guide-add1", pk=prj.id)        


def resch_guide_add1(request, pk):

    prj = Resch_guide.objects.get(id=pk)    
    form1 = Resch_guideForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    
    if request.method == 'POST':
         
            form1 = Resch_guideForm(request.POST, request.FILES, instance=prj)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("resch-guide-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
        
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj': prj,
        
        }
    return render(request, 'catg_3/resch_guide_add.html', context) 

def resch_guide_cancel(request, *args, **kwargs):    
    prj=Resch_guide.objects.get(id=id_var)
    prj.delete()
    
    return redirect("catg_3:resch-guide-view", user_id=prj.email_id)
    
def resch_guide_delete(request, pk):
    prj = Resch_guide.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:resch-guide-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/resch_guide_delete.html', context)
    
    
def resch_guide_edit(request, pk):
    prj = Resch_guide.objects.get(id=pk)
    
    form1 = Resch_guideForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Resch_guideForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_resch_guide.html', context)    
    

    
def fellow_award_view(request,*args, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
   
    global pk_var
    pk_var = user_id    
    global user_var
    user_var = user_id
    
    account = Account.objects.get(pk=user_id) 

    if account.to_dsg == 'Stage 2':
        api_cap = 4        
    elif account.to_dsg == 'Stage 3':
        api_cap = 10 
    elif account.to_dsg == 'Stage 4':
        api_cap = 15     
    elif account.to_dsg == 'Stage 5':
        api_cap = 20 
    

    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = Fellow_AwardForm()
        else:           
            try :                
                prj = Fellow_Award.objects.get(pk=user_id)                
            except Fellow_Award.DoesNotExist:                                    
                prj = Fellow_Award.objects.create(pk=user_id,email_id=user_id).save()                
            
            
            form = Fellow_AwardForm(instance=prj)              
            prj = account.fellow_award_set.all()
            lec = account.lecture_paper_set.all()
            elearn = account.e_learning_set.all()
            
            prj_count = prj.count()
            lec_count = lec.count()
            elearn_count = elearn.count()
            
            context = {
                'form': form,
                'prj': prj,
                'lec': lec,    
                'prj_count': prj_count,
                'lec_count': lec_count,
                'pk_var': pk_var,
                'user_var': user_var,
                'elearn' : elearn,
                'elearn_count' : elearn_count,
                'account' : account,
                'api_cap' : api_cap,
            }

        return render(request, "catg_3/fellow_award_view.html", context)

        

def fellow_award_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    prj=Fellow_Award.objects.create(email_id=request.user.id)    
    prj.save()
    
    global id_var 
    id_var=prj.id
    
    # After adding a blank record and redirected to views for editing
    
    return redirect("catg_3:fellow-award-add1", pk=prj.id)        


def fellow_award_add1(request, pk):

    prj = Fellow_Award.objects.get(id=pk)    
    form1 = Fellow_AwardForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    
    if request.method == 'POST':
         
            form1 = Fellow_AwardForm(request.POST, request.FILES, instance=prj)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("fellow-award-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
        
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj': prj,
        
        }
    return render(request, 'catg_3/fellow_award_add.html', context)
    
def fellow_award_cancel(request, *args, **kwargs):    
    prj=Fellow_Award.objects.get(id=id_var)
    prj.delete()
    
    return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
    
def fellow_award_delete(request, pk):
    prj = Fellow_Award.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/fellow_award_delete.html', context) 

def fellow_award_edit(request, pk):
    prj = Fellow_Award.objects.get(id=pk)
    
    form1 = Fellow_AwardForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Fellow_AwardForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_fellow_award.html', context)  

 
def lecture_paper_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    prj=Lecture_Paper.objects.create(email_id=request.user.id)    
    prj.save()
    
    global id_var 
    id_var=prj.id
    
    # After adding a blank record and redirected to views for editing
    
    return redirect("catg_3:lecture-paper-add1", pk=prj.id)        


def lecture_paper_add1(request, pk):

    prj = Lecture_Paper.objects.get(id=pk)    
    form1 = Lecture_PaperForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    
    if request.method == 'POST':
         
            form1 = Lecture_PaperForm(request.POST, request.FILES, instance=prj)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("lecture-paper-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
        
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj': prj,
        
        }
    return render(request, 'catg_3/lecture_paper_add.html', context)
    
def lecture_paper_cancel(request, *args, **kwargs):    
    prj=Lecture_Paper.objects.get(id=id_var)
    prj.delete()
    
    return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
    
def lecture_paper_delete(request, pk):
    prj = Lecture_Paper.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/lecture_paper_delete.html', context) 
        
        

def lecture_paper_edit(request, pk):
    prj = Lecture_Paper.objects.get(id=pk)
    
    form1 = Lecture_PaperForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Lecture_PaperForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_lecture_paper.html', context)  


def lecture_elearn_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    
    prj=E_Learning.objects.create(email_id=request.user.id)    
    prj.save()
    
    global id_var 
    id_var=prj.id
    
    # After adding a blank record and redirected to views for editing
    
    return redirect("catg_3:lecture-elearn-add1", pk=prj.id)        


def lecture_elearn_add1(request, pk):

    prj = E_Learning.objects.get(id=pk)    
    form1 = E_LearningForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    
    if request.method == 'POST':
         
            form1 = E_LearningForm(request.POST, request.FILES, instance=prj)
            if form1.is_valid():                            
                 
                form1.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("lecture-elearn-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
        
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj': prj,
        
        }
    return render(request, 'catg_3/lecture_elearn_add.html', context)
    
def lecture_elearn_cancel(request, *args, **kwargs):    
    prj=E_Learning.objects.get(id=id_var)
    prj.delete()
    
    return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
    
def lecture_elearn_delete(request, pk):
    prj = E_Learning.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/lecture_elearn_delete.html', context) 
        
        

def lecture_elearn_edit(request, pk):
    prj = E_Learning.objects.get(id=pk)
    
    form1 = E_LearningForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = E_LearningForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_lecture_elearn.html', context)  

    

def api_summary_view(request,*args, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
   
    global pk_var
    pk_var = user_id    
    global user_var
    user_var = user_id
    
    account = Account.objects.get(pk=user_id)
    
    api1 = ApiCatg_I.objects.get(pk=user_id)
    api2 = ApiCatg_II.objects.get(pk=user_id)
    
    jrnl = account.jrnl_pub_set.all()
    pub = account.pub_other_set.all()
    res = account.resch_proj_set.all()
    cons = account.resch_cons_set.all()
    out = account.prj_outcm_set.all()
    guide = account.resch_guide_set.all()
    
    
    fell = account.fellow_award_set.all()
    lec = account.lecture_paper_set.all()
    elearn = account.e_learning_set.all()
    

    context = {}
    
    context = {
                'account': account,
                
                'api1':api1,
                'api2':api2,
                
                'jrnl': jrnl,
                'pub': pub,
                'res' : res,
                'cons': cons,
                'out' : out,
                'guide': guide,
                'fell': fell,
                'lec': lec,
                'elearn' : elearn,
                
              
                
                'pk_var': pk_var,
                'user_var': user_var,               
                
    }
    
    return render(request, "catg_3/api_summary_view.html", context)
    