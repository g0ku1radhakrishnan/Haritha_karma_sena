from django.shortcuts import render,redirect
from.models import*
from django.http import HttpResponse
from django.contrib import messages
from datetime import date
import datetime
from django.core.files.storage import FileSystemStorage




# Create your views here.
def home(request):
    return render(request,'home.html')


def login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['pswd']

        try:
            log=Login.objects.get(username=uname,password=password)
            request.session['login_id']=log.pk


            if log.usertype=='admin':
                 return HttpResponse("<script>alert('login success');window.location='/admin_home';</script>")
            if log.usertype=='user':
                user=User.objects.get(login_id=request.session['login_id'])
                if log:
                     request.session['user_id']=user.pk 
                return HttpResponse("<script>alert('login success');window.location='/user_home';</script>")
            if log.usertype=='it_officer':
                 return HttpResponse("<script>alert('login success');window.location='/it_officer_home';</script>")
            if log.usertype=='hks':
                hks=HKS.objects.get(login_id=request.session['login_id'])
                if log:
                    request.session['hks_id']=hks.pk
                if hks.type == 'normal':
                    # if log:
                    #     request.session['hks_id']=hks.pk 
                        return redirect('hks_normal_home')
                elif hks.type == 'custom':
                        return redirect('hks_custom_home')
                elif hks.type == 'delivery':
                        return redirect('hks_delivery_home')

                 

        except:
            return HttpResponse("<script>alert('login fail');window.location='/login';</script>")

    return render(request,'login.html')


def registration(request):
    if request.method=='POST':
        name=request.POST['name']
        building_number=request.POST['buildnumber']
        housename=request.POST['housename']
        place=request.POST['place']
        email=request.POST['email']
        phone=request.POST['phone']
        username=request.POST['uname']
        password=request.POST['pswd']
        wadid=request.POST['ward_id']
        
        wadid=Ward.objects.get(ward_id=wadid)


        x=Login(username=username,password=password,usertype='user')
        x.save()


        y=User( building_owner_name=name,building_number=building_number,housename=housename,place=place,email=email,ward_id=wadid,phone=phone,login_id_id=x.pk)
        y.save()
        return HttpResponse("<script>alert('Registration is completed');window.location='/login';</script>")
    x=Ward.objects.all()


    return render(request,'registration.html',{'wards': x})



    # ***ADMIN****


def adminhome(request):

    return render(request,'admin_home.html')

def admin_add_ward(request):
    if request.method=='POST':
        wardnumber=request.POST['wardno']

        x=Ward(ward_number=wardnumber)
        x.save()
        return redirect('addward')
    y=Ward.objects.all()


    return render(request,'admin_add_ward.html',{'y':y})

def admin_delete_ward(request,id):

    x=Ward.objects.get(ward_id=id)
    x.delete()
    messages.success(request, 'Ward deleted successfully.')
    return redirect('addward')



def admin_add_hks(request):
    if request.method == 'POST':
        name     = request.POST.get('name')
        place    = request.POST.get('place')
        phone    = request.POST.get('phone')
        email    = request.POST.get('email')
        hks_type = request.POST.get('type')
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        log=Login.objects.create(username=uname,password=pswd,usertype='hks')
        x=HKS(name=name,place=place,phone=phone,email=email,type=hks_type,login_id=log)
        x.save()
        messages.success(request, 'HKS member added successfully.')
        return redirect('admin_manage_hks')
    y=HKS.objects.all()

    return render(request,'admin_add_hks.html',{'y':y})


def admin_update_hks(request,id):
    x=HKS.objects.get(hks_id=id)
    if request.method == 'POST':
        x.name  = request.POST.get('name')
        x.place = request.POST.get('place')
        x.phone = request.POST.get('phone')
        x.email = request.POST.get('email')
        x.type  = request.POST.get('type')
        x.save()
        x.login_id.username=request.POST.get('uname')
        x.login_id.password=request.POST.get('pswd')
        x.login_id.save()
        messages.success(request, 'HKS member updated successfully.')
        return redirect('admin_manage_hks')
    hks_members = HKS.objects.all()
    return render(request, 'admin_add_hks.html', {
        'hks_members': hks_members,
        'update_data': x})


def admin_delete_hks(request, id):
    HKS.objects.get(hks_id=id).delete()
    messages.success(request, 'HKS member deleted successfully.')
    return redirect('admin_manage_hks')    

    
def admin_assign_ward(request):
    if request.method == 'POST':
        hks_id  = request.POST.get('hks_id')
        ward_id = request.POST.get('ward_id')

        hks  = HKS.objects.get(hks_id=hks_id)
        ward = Ward.objects.get(ward_id=ward_id)

        # check if already assigned
        if Assign_Ward.objects.filter(hks_id=hks, ward_id=ward).exists():
            messages.error(request, 'This HKS member is already assigned to this ward.')
            return redirect('admin_assign_ward')

        Assign_Ward.objects.create(
            hks_id=hks,
            ward_id=ward
        )
        messages.success(request, 'HKS member assigned to ward successfully.')
        return redirect('admin_assign_ward')

    hks_members  = HKS.objects.all()
    wards        = Ward.objects.all()
    assignments  = Assign_Ward.objects.all()

    return render(request, 'admin_assign_ward.html', {
        'hks_members': hks_members,
        'wards'      : wards,
        'assignments': assignments
    })


def admin_delete_assignment(request,id):
    Assign_Ward.objects.get(assign_id_id=id).delete()
    messages.success(request, 'Assignment removed successfully.')
    return redirect('admin_assign_ward')

def admin_add_itofficer(request):
    if request.method == 'POST':
        name     = request.POST.get('name')
        phone    = request.POST.get('phone')
        email    = request.POST.get('email')
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        log=Login.objects.create(username=uname,password=pswd,usertype='it_officer')
        x=IT_Officer(name=name,phone=phone,email=email,login_id=log)
        x.save()
        messages.success(request, 'it officer member added successfully.')
        return redirect('adminadd_itofficer')
    y=IT_Officer.objects.all()

    return render(request,'adminadd_itofficer.html',{'y':y})


def admin_update_itofficer(request,id):
    x=IT_Officer.objects.get(officer_id=id)
    if request.method=='POST':
        x.name  = request.POST.get('name')
        x.phone = request.POST.get('phone')
        x.email = request.POST.get('email')
        x.save()
        x.login_id.username=request.POST.get('uname')
        x.login_id.password=request.POST.get('pswd')
        x.login_id.save()
        messages.success(request, 'HKS member updated successfully.')
        return redirect('adminadd_itofficer')
    itofficer =IT_Officer.objects.all()
    return render(request, 'adminadd_itofficer.html', {
        'y': itofficer,
        'update_data': x})


def admin_delete_itofficer(request,id):
    IT_Officer.objects.get(officer_id=id).delete()
    messages.success(request, 'itofficer removed successfully.')
    return redirect('adminadd_itofficer')



def admin_view_user(request):
    x=User.objects.all()

    return render(request,'admin_view_user.html',{'x':x})

def admin_view_complaints(request):
    login_id = request.session.get('login_id')

    login_obj  = Login.objects.get(login_id=login_id)

    # ✅ only show complaints sent to this admin
    complaints = Complaints.objects.filter(receiver_id=login_obj)

    return render(request, 'admin_view_complaints.html', {'complaints': complaints})   

def admin_reply_complaint(request, id):
    complaint = Complaints.objects.get(complaints_id=id)

    if request.method == 'POST':
        reply = request.POST.get('reply')
        complaint.reply = reply
        complaint.save()
        messages.success(request, 'Reply sent successfully.')
        return redirect('admin_view_complaints')

    return render(request, 'admin_reply_complaint.html', {'complaint': complaint})



    # ***USER****

def User_home(request):

    return render(request,'user_home.html')



def user_add_waste(request):
    user_id = request.session.get('user_id')
    # if not user_id:
    #     return redirect('login')

    x = User.objects.get(user_id=user_id)

    if request.method == 'POST':
        My_Waste.objects.create(
            date=date.today(),
            status='pending',
            user_id=x          
        )
        messages.success(request, 'Waste added successfully.')
        return redirect('user_add_waste')  

    wastes = My_Waste.objects.filter(user_id=x)  # ✅ fetch waste history
    return render(request, 'user_add_waste.html', {'wastes': wastes})




def user_send_complaint(request):
    login_id = request.session.get('login_id')
    login_obj = Login.objects.get(login_id=login_id)


    if request.method == 'POST':
        description = request.POST.get('description')

        Complaints.objects.create(
            sender_id=login_obj,
            receiver_id=Login.objects.get(usertype='admin'),  # ✅ send to admin
            description=description,
            reply='',
            date=str(datetime.date.today())
        )
        messages.success(request, 'Complaint sent successfully.')
        return redirect('user_send_complaint')

    complaints = Complaints.objects.filter(sender_id=login_id)
    return render(request, 'user_send_complaint.html', {'complaints': complaints})


def user_view_notification(request):
    notifications = IT_Notification.objects.all().order_by('-it_notification_id')

    return render(request, 'user_view_notification.html', {
        'notifications': notifications
    })
def user_view_hks_notification(request):
    x=HKS_Notification.objects.all()

    return render(request,'user_view_hks_notiication.html',{'x':x})




def user_view_recycle_product(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # ✅ filter by type
    bio_products     = Products.objects.filter(product_type='bio')
    plastic_products = Products.objects.filter(product_type='plastic')

    return render(request, 'user_view_recycle_product.html', {
        'bio_products'    : bio_products,
        'plastic_products': plastic_products
    })


def add_to_cart(request,id):
    user_id = request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    product = Products.objects.get(products_id=id)


    order=Order_Master.objects.filter(user_id=user,status='pending').first()
    if not order:
        order=Order_Master.objects.create(user_id=user,total_amount='o',date=date.today(),status='pending')
    existing=Order_Child.objects.filter(om_id=order,product_id=product).first()
    if existing:
        existing.quantity=str(int(existing.quantity)+1)
        existing.amount=str(int(existing.quantity)*float(product.amount))
        existing.save()
    else:
        Order_Child.objects.create(om_id=order,product_id=product,quantity='1',amount=product.amount)
    
    order_items=Order_Child.objects.filter(om_id=order)
    total=sum(float(i.amount) for i  in order_items)
    order.total_amount=str(total)
    order.save()
    messages.success(request, f'{product.product_name} added to cart.')
    return redirect('user_view_recycle_product')

def user_view_cart(request):
    user_id=request.session.get('user_id')
    user=User.objects.get(user_id=user_id)

    order=Order_Master.objects.filter(user_id=user,status='pending').first()
    cart_items=[]
    if order:
        cart_items=Order_Child.objects.filter(om_id=order)
    
    return render(request,'user_view_cart.html',{'cart_items':cart_items,'order':order})
def remove_cart(request,id):
    user_id=request.session.get('user_id')
    item=Order_Child.objects.get(oc_id=id)
    order=item.om_id
    item.delete()
        # update total after removing
    order_items        = Order_Child.objects.filter(om_id=order)
    total              = sum(float(i.amount) for i in order_items)
    order.total_amount = str(total)
    order.save()

    # delete order if cart is empty
    if order_items.count() == 0:
        order.delete()

    messages.success(request, 'Item removed from cart.')
    return redirect('user_view_cart')

def make_payment(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user  = User.objects.get(user_id=user_id)
    order = Order_Master.objects.get(om_id=id)

    if request.method == 'POST':
        # save payment
        OD_Payment.objects.create(
            om_id=order,
            amount=order.total_amount,
            date=str(datetime.date.today()),
            status='paid'
        )

        # update order status
        order.status = 'ordered'
        order.save()

        # reduce stock for each product
        order_items = Order_Child.objects.filter(om_id=order)
        for item in order_items:
            product       = item.product_id
            product.stock = str(int(product.stock) - int(item.quantity))
            product.save()

        messages.success(request, 'Payment successful.')
        return redirect('user_order_history')

    # get cart items for display
    cart_items = Order_Child.objects.filter(om_id=order)
    return render(request, 'make_payment.html', {
        'order'     : order,
        'cart_items': cart_items
    })

def user_order_history(request):
    user_id = request.session.get('user_id')


    user   = User.objects.get(user_id=user_id)
    orders = Order_Master.objects.filter(
        user_id=user
    ).exclude(status='pending')

    return render(request, 'user_order_history.html', {'orders': orders})


def user_send_custom_waste_request(request):
    user_id = request.session.get('user_id')
    user   = User.objects.get(user_id=user_id)
    if request.method=='POST':
        Custom_Waste_Request.objects.create(user_id=user,date=date.today(),total_amount='o',status='pending')
        messages.success(request, 'Custom waste request sent successfully.')
        return redirect('user_send_custom_waste')
    requests = Custom_Waste_Request.objects.filter(
        user_id=user
    ).order_by('-custom_waste_request_id')

    return render(request, 'user_send_custom_waste.html', {
        'requests': requests
    })

def user_custom_waste_payment(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    custom_request = Custom_Waste_Request.objects.get(
        custom_waste_request_id=id
    )

    if request.method == 'POST':
        Cust_Payment.objects.create(
            custom_waste_request_id=custom_request,
            amount=custom_request.total_amount,
            date=str(datetime.date.today()),
            status='paid'
        )

        # update request status
        custom_request.status = 'completed'
        custom_request.save()

        messages.success(request, 'Payment successful.')
        return redirect('user_send_custom_waste')

    # get status details
    try:
        waste_status = Custom_Waste_Status.objects.get(
            custom_waste_request_id=custom_request
        )
    except:
        waste_status = None

    return render(request, 'user_custom_waste_payment.html', {
        'custom_request': custom_request,
        'waste_status'  : waste_status
    })



def user_send_public_waste(request):
    x=User.objects.get(user_id=request.session.get('user_id'))
    if request.method=='POST':
        title=request.POST['title']
        photo=request.FILES['photo']


        fs=FileSystemStorage()
        image=fs.save(photo.name,photo)
        y=Public_Waste(title=title,image=image,status='pending',user_id=x)
        y.save()
        return redirect('user_send_publicwaste')
    view=Public_Waste.objects.filter(user_id=x)
    return render(request,'user_send_publicwaste.html',{'view':view})

# ********IT OFFICER******

def it_officer_home(request):
    
    return render(request,'it_officer_home.html')


# def it_send_notification(request):
#     if request.method == 'POST':
#         title       = request.POST.get('title')
#         description = request.POST.get('description')
#         send_to     = request.POST.get('send_to')  # 'users', 'hks', 'specific_hks'
#         hks_id      = request.POST.get('hks_id')   # only if specific hks selected
#         today       = str(datetime.date.today())

#         if send_to == 'users':
#             # ✅ send to all users — save in IT_Notification
#             IT_Notification.objects.create(
#                 title=title,
#                 description=description,
#                 date=today
#             )
#             messages.success(request, 'Notification sent to all users.')

#         elif send_to == 'hks':
#             # ✅ send to all HKS members
#             hks_members = HKS.objects.all()
#             for hks in hks_members:
#                 HKS_Notification.objects.create(
#                     hks_id=hks,
#                     title=title,
#                     description=description,
#                     date=today
#                 )
#             messages.success(request, 'Notification sent to all HKS members.')

#         # elif send_to == 'specific_hks':
#         #     # ✅ send to specific HKS member
#         #     hks = HKS.objects.get(hks_id=hks_id)
#         #     HKS_Notification.objects.create(
#         #         hks_id=hks,
#         #         title=title,
#         #         description=description,
#         #         date=today
#         #     )
#         #     messages.success(request, f'Notification sent to {hks.name}.')

#         return redirect('it_send_notification')

#     hks_members         = HKS.objects.all()
#     it_notifications    = IT_Notification.objects.all().order_by('-it_notification_id')
#     hks_notifications   = HKS_Notification.objects.all().order_by('-hks_notification_id')

#     return render(request, 'it_send_notification.html', {
#         'hks_members'      : hks_members,
#         'it_notifications' : it_notifications,
#         'hks_notifications': hks_notifications
#     })

def it_send_notification(request):
    if request.method=='POST':
        title       = request.POST.get('title')
        description = request.POST.get('description')
        x=IT_Notification(title=title,description=description,date=date.today())
        x.save()
        messages.success(request, 'Notification sent to all users.')
        return redirect('it_send_notification')
    y=IT_Notification.objects.all()
    return render(request,'it_send_notification.html',{'y':y})


def itofficer_wastereport(request):
    x=Public_Waste.objects.all()
    y=Custom_Waste_Status.objects.all()

    return render(request,'itofficer_wastereport.html',{'x':x,'y':y})






def it_office_view_hks(request):
    x=HKS.objects.all()

    return render(request,'it_office_view_hks.html',{'x':x})


def it_officer_view_complaints(request):
    login_id = request.session.get('login_id')

    login_obj  = Login.objects.get(login_id=login_id)

    # ✅ only show complaints sent to this 
    complaints = Complaints.objects.filter(receiver_id=login_obj)

    return render(request, 'it_officer_view_complaints.html', {'complaints': complaints})  



def it_officer_reply_complaint(request, id):
    complaint = Complaints.objects.get(complaints_id=id)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        complaint.reply = reply
        complaint.save()
        messages.success(request, 'Reply sent successfully.')
        return redirect('it_officer_view_complaints')

    return render(request, 'it_officer_reply_complaints.html', {'complaint': complaint})

def it_manage_products(request):
    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        product_name = request.POST.get('product_name')
        description  = request.POST.get('description')
        stock        = request.POST.get('stock')
        amount       = request.POST.get('amount')
        image        = request.FILES.get('image')

        fs    = FileSystemStorage()
        image = fs.save(image.name, image)

        Products.objects.create(
            product_type=product_type,
            product_name=product_name,
            description=description,
            stock=stock,
            amount=amount,
            image=image
        )
        messages.success(request, 'Product added successfully.')
        return redirect('it_manage_products')

    # filter by type
    bio_products     = Products.objects.filter(product_type='bio')
    plastic_products = Products.objects.filter(product_type='plastic')

    return render(request, 'it_manage_products.html', {
        'bio_products'    : bio_products,
        'plastic_products': plastic_products
    })


def it_delete_product(request, id):
    Products.objects.get(products_id=id).delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('it_manage_products')


def it_update_product(request, id):
    product = Products.objects.get(products_id=id)

    if request.method == 'POST':
        product.product_type = request.POST.get('product_type')
        product.product_name = request.POST.get('product_name')
        product.description  = request.POST.get('description')
        product.stock        = request.POST.get('stock')
        product.amount       = request.POST.get('amount')

        if request.FILES.get('image'):
            fs             = FileSystemStorage()
            product.image  = fs.save(
                request.FILES['image'].name,
                request.FILES['image']
            )

        product.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('it_manage_products')

    bio_products     = Products.objects.filter(product_type='bio')
    plastic_products = Products.objects.filter(product_type='plastic')

    return render(request, 'it_manage_products.html', {
        'bio_products'    : bio_products,
        'plastic_products': plastic_products,
        'update_data'     : product
    })


def itofficer_payment(request):
    z=OD_Payment.objects.all()
    total      = sum(float(p.amount) for p in z)
    confirmed  = OD_Payment.objects.filter(status='confirmed').count()

    return render(request,'itofficer_payment.html',{'z':z,'total':total,'confirmed':confirmed})

    # ***HKS_officer****

def hks_home_normal(request):

    return render(request,'hks_normal_home.html') 


def hks_home_custom(request):
    
    return render(request,'hks_custom_home.html') 
def hks_home_delivery(request):
    
    return render(request,'hks_delivery_home.html') 


def hks_normal_send_complaint(request):
    login_id = request.session.get('login_id')
    login_obj = Login.objects.get(login_id=login_id)


    if request.method == 'POST':
        description = request.POST.get('description')

        Complaints.objects.create(
            sender_id=login_obj,
            receiver_id=Login.objects.get(usertype='it_officer'),  # ✅ send to it_officer
            description=description,
            reply='',
            date=str(datetime.date.today())
        )
        messages.success(request, 'Complaint sent successfully.')
        return redirect('hks_normal_send_complaint')

    complaints = Complaints.objects.filter(sender_id=login_id)
    return render(request, 'hks_normal_send_complaint.html', {'complaints': complaints})

def hks_custom_send_complaint(request):
    login_id = request.session.get('login_id')
    login_obj = Login.objects.get(login_id=login_id)


    if request.method == 'POST':
        description = request.POST.get('description')

        Complaints.objects.create(
            sender_id=login_obj,
            receiver_id=Login.objects.get(usertype='it_officer'),  # ✅ send to it_officer
            description=description,
            reply='',
            date=str(datetime.date.today())
        )
        messages.success(request, 'Complaint sent successfully.')
        return redirect('hks_custom_send_complaint')

    complaints = Complaints.objects.filter(sender_id=login_id)
    return render(request, 'hks_custom_send_complaint.html', {'complaints': complaints})


def hks_delivery_send_complaint(request):
    login_id = request.session.get('login_id')
    login_obj = Login.objects.get(login_id=login_id)


    if request.method == 'POST':
        description = request.POST.get('description')

        Complaints.objects.create(
            sender_id=login_obj,
            receiver_id=Login.objects.get(usertype='it_officer'),  # ✅ send to it_officer
            description=description,
            reply='',
            date=str(datetime.date.today())
        )
        messages.success(request, 'Complaint sent successfully.')
        return redirect('hks_delivery_send_complaint')

    complaints = Complaints.objects.filter(sender_id=login_id)
    return render(request, 'hks_delivery_send_complaint.html', {'complaints': complaints})    




def hks_custom_view_custom_waste(request):
    pending=Custom_Waste_Request.objects.filter(status='pending')
    approved=Custom_Waste_Request.objects.filter(status='approved')
    completed=Custom_Waste_Request.objects.filter(status='completed')

    return render(request,'hks_view_custom_requests.html',{'pending':pending,'approved':approved,'completed':completed})


def hks_custom_view_public_waste(request):
    x=Public_Waste.objects.all()

    return render(request,'hks_view_public_waste.html',{'x':x})

def hks_custom_approve_public_waste(request,id):
    waste=Public_Waste.objects.get(public_waste_id=id)
    if request.method=='POST':
        waste.status='verified'
        waste.save()
        messages.success(request, 'Waste verified and reward given.')
        return redirect('hks_view_public_waste')
    return render(request, 'hks_verify_public_waste.html', {'waste': waste})


def hks_Custom_view_notification(request):
    notifications = IT_Notification.objects.all()

    return render(request, 'hks_Custom_view_notification.html', {
        'notifications': notifications
    })
    
    
def hks_view_notification_it(request):
    x=IT_Notification.objects.all()
    return render(request,'hks_view_notification_it.html',{'x':x})



def hks_update_custom_waste(request,id):
    custom_request=Custom_Waste_Request.objects.get(custom_waste_request_id=id)
    if request.method=='POST':
        plastic_quantity=request.POST['plastic_quantity']
        plastic_amount   =request.POST['plastic_amount']
        bio_quantity=request.POST['bio_quantity']
        bio_amount=request.POST['bio_amount']
        x=Custom_Waste_Status(custom_waste_request_id=custom_request,
            plastic_quantity=plastic_quantity,
            plastic_amount=plastic_amount,
            bio_quantity=bio_quantity,
            bio_amount=bio_amount)
      
        total=float(plastic_amount)+float(bio_amount)
        custom_request.total_amount=str(total)
        custom_request.status='approved'
        custom_request.save()
        messages.success(request, 'Status updated successfully.')
        return redirect('hks_view_custom_requests')

    return render(request, 'hks_update_custom_status.html', {
        'custom_request': custom_request
    })




def hks_delivery_view_order(request):
    x=Order_Master.objects.filter(status__in=['ordered','delivered'])

    return render(request,'hks_delivery_view_order.html',{'x':x})


def hks_delivery_payment_confirmation(request, id):
    hks_id = request.session.get('hks_id')


    # get payment for this order
    payment = OD_Payment.objects.get(om_id=id)
    order   = Order_Master.objects.get(om_id=id)

    if request.method == 'POST':
        payment.status = 'confirmed'  # ✅ confirm payment
        payment.save()
        messages.success(request, 'Payment confirmed successfully.')
        return redirect('hks_delivery_view_order')

    # get order items
    order_items = Order_Child.objects.filter(om_id=order)

    return render(request, 'hks_delivery_payment_confirmation.html', {
        'payment'    : payment,
        'order'      : order,
        'order_items': order_items
    })
def hks_delivery_update_order(request,id):
    x=Order_Master.objects.get(om_id=id)
    if request.method=='POST':
        x.status='delivered'
        x.save()
        
        messages.success(request, 'Order marked as delivered.')
        return redirect('hks_delivery_view_order')
    y=Order_Child.objects.filter(om_id=x)
    return render(request, 'hks_delivery_update_order.html', {
        'x'      : x,
        'y': y
    })

def hks_custom_send_notification(request):
    x=HKS.objects.get(hks_id=request.session['hks_id'])
    if request.method=='POST':
        title=request.POST['title']
        description=request.POST['desc']
        y=HKS_Notification(title=title,description=description,date=date.today(),hks_id=x)
        y.save()
        return redirect('hks_custom_send_notification')
    view=HKS_Notification.objects.all()
    return render(request,'hks_custom_send_notification.html',{'view':view})


def hks_view_waste(request):
    x=My_Waste.objects.all()

    return render(request,'hks_view_waste.html',{'x':x})

def hks_update_waste(request,id):
    x=My_Waste.objects.get(my_waste_id=id)
    if request.method=='POST':
        x.status='collected'
        x.save()
        messages.success(request, 'Status updated successfully.')
        return redirect('hks_view_waste')

    return render(request,'hks_view_waste.html',{'x':x})

def hks_payment_confirmation(request,id):
    x=OD_Payment.objects.get(om_id=id)
    if request.method=='POST':
        x.status='verified'
        x.save()
        return redirect('')


        
