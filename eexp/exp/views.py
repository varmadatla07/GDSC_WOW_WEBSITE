from django.shortcuts import render , redirect
from .models import student
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
import math, random
import http.client
from datetime import datetime
import razorpay
from django.template.loader import get_template
# from .forms import UserImage
from django.core.mail import EmailMultiAlternatives
import hashlib



class GDSC(TemplateView):

    m_otp = ""

    
    # id = ''
    first_name =  ''
    last_name = ''
    ph_number = 0
    email = ''
    college = ''
    member =  ''
    address =  ''
    img =  ''
    branch = ''


    def home(request):
        return render(request,"register.html")
    




    def send_otp(request):
        if request.method=="POST":
            # GDSC.id = datetime.now()
            GDSC.first_name = request.POST.get('fname')
            GDSC.last_name = request.POST.get('lname')
            GDSC.ph_number = request.POST.get('phone')
            GDSC.email = request.POST.get('mail')
            GDSC.college = request.POST.get('college')
            GDSC.branch = request.POST.get('branch')
            GDSC.member = request.POST.get('member')
            if GDSC.member == 'on':
                GDSC.member = True    
            else:
                GDSC.member = False             
            GDSC.address = request.POST.get('address') 
  
            # ph_number = request.POST.get('phone')
            # conn = http.client.HTTPSConnection("api.msg91.com")
            # authkey = settings.AUTH_KEY
            # headers = { 'content-type': "application/json" }
            # ph_otp=generateOTP()
            # url = "http://control.msg91.com/api/sendotp.php?otp="+m_otp+"&message="+"Your otp is "+m_otp +"&mobile="+ph_number+"&authkey="+authkey+"&country=91"
            # conn.request("GET", url , headers=headers)
            # res = conn.getresponse()
            # data = res.read()
            # print(data)
            host_email = settings.EMAIL_HOST_USER
            sub = 'OTP request'
            print(GDSC.email)
            
            digits = "0123456789"
            OTP = ""
            for i in range(4) :
                OTP += digits[math.floor(random.random() * 10)]
            GDSC.m_otp = OTP

            htmlgen = f'<p>Your OTP is <strong>{GDSC.m_otp}</strong></p>'
            # send_mail(sub,GDSC.m_otp,host_email,[GDSC.email], fail_silently=False, html_message=htmlgen)
            print(GDSC.m_otp)
            # return HttpResponse()
        print(GDSC.m_otp)
        return render(request,"otpver.html")
    
    def otp_generation(self) :
        digits = "0123456789"
        OTP = ""
        for i in range(4) :
            OTP += digits[math.floor(random.random() * 10)]
        return OTP 
    

    def otp_validation(request):
        # id = GDSC.id  
        first_name =  GDSC.first_name
        last_name = GDSC.last_name
        ph_number = GDSC.ph_number
        email = GDSC.email
        branch = GDSC.branch
        college = GDSC.college
        member =  GDSC.member
        address =  GDSC.address
        img =  GDSC.img

        print(first_name)

        mail_otp_front = request.POST.get('email')

        if GDSC.m_otp == mail_otp_front:
            en = student(first_name=first_name,last_name=last_name,ph_number=ph_number,email=email,branch=branch,college=college,member=member,address=address,img=img)
            en.save()
            client = razorpay.Client(auth=(settings.KEY_ID, settings.SECRET))
            data = { "amount": 100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            en.razor_pay_order_id = payment['id']
            en.save()
            return render(request,"home.html",{'payment': payment})
        else:
            return render(request,"otpver.html",{'error': 'wrong otp!!'})
        


    def ticket(request):
        fullname = GDSC.first_name +" "+ GDSC.last_name
        return render(request,"ticket.html",{'name':fullname})
    def success(request):
        order_id = request.GET.get('razorpay_order_id')
        print(order_id)
        signature = request.GET.get('razorpay_signature')
        payment_id = request.GET.get('razorpay_payment_id')
        user = student.objects.get(razor_pay_order_id=order_id )
        qrhash = hashlib.md5(order_id.encode())
        print(qrhash.hexdigest())
        user.qr_hash = qrhash.hexdigest()

        user.is_paid = True
        user.razor_pay_payment_id = payment_id 
        user.razor_pay_payment_signature = signature
        user.save()
        u = student.objects.filter(razor_pay_order_id = order_id ).values()
        
        fullname = user.first_name+" "+user.last_name
        print(fullname)
        email_confirmation(user.email ,fullname,user.qr_hash)
        return render(request,"success.html",{'payment_id':payment_id,'fullname':fullname,'status':user.is_paid})


def email_confirmation(mail,fullname,qr_hash):
    mail = mail
    sub = 'payment_sucess'
    fullname = 'siddarth'
    host_email = settings.EMAIL_HOST_USER
    subject, from_email, to = sub , host_email, mail
    html_content = get_template('ticket.html').render({'name':fullname,'qr_hash':qr_hash})
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = 'html'
    # msg.send()


            

    


