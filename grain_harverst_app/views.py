from django.shortcuts import render, redirect
from django.apps import apps
from grain_harverst_app.models import UsersTable
from .forms import ImageUploadForm
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import io
from PIL import Image
import joblib
import os
import pandas as pd
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Views for User Authentication

def index(request):
    return render(request, 'grain_harverst_app/index.html', {})

def dash(request):
    return render(request, 'grain_harverst_app/dashboard.html', {})

def insertt(request):
    return render(request, 'grain_harverst_app/signup.html', {})

def NewUser(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST.get('role', 'farmer')

        users = UsersTable(user_name=name, pass_word=password, user_email=email, role=role)
        users.save()

        return redirect('login')
    else:
        return render(request, 'grain_harverst_app/signup.html', {})

def RetrieveUser(request, user_id):
    try:
        user = UsersTable.objects.get(pk=user_id)
        context = {'user': user}
        return render(request, 'grain_harverst_app/user_detail.html', context)
    except UsersTable.DoesNotExist:
        return HttpResponseNotFound('User not found')

def UpdateUser(request, user_id):
    try:
        user = UsersTable.objects.get(pk=user_id)
        if request.method == 'POST':
            user.user_name = request.POST['username']
            user.pass_word = request.POST['password']
            user.user_email = request.POST['email']
            user.role = request.POST.get('role', 'farmer')
            user.save()
            return redirect('admin_portal')
        else:
            context = {'user': user}
            return render(request, 'grain_harverst_app/update_user.html', context)
    except UsersTable.DoesNotExist:
        return HttpResponseNotFound('User not found')
        
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = UsersTable.objects.get(user_name=username, pass_word=password)
            
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.user_name
            request.session['role'] = user.role 
            
            if user.role == 'farmer':
                return redirect('dashboardd')
            elif user.role == 'supplier':
                return redirect('chat_message_list')
            elif user.role == 'stockkeeper':
                return redirect('stockkeeper_dashboard')
            elif user.role == 'admin':
                return redirect('admin_portal')
            else:
                return redirect('index')

        except UsersTable.DoesNotExist:
            return render(request, 'grain_harverst_app/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'grain_harverst_app/login.html', {})

def logout(request):
    auth_logout(request)
    return redirect('login')

# Views for Image Classification
from django.shortcuts import render
from django.apps import apps
from .forms import ImageUploadForm
from PIL import Image
import numpy as np
import io
from tensorflow.keras.preprocessing.image import img_to_array

def predict_rice_quality(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']

            # Convert InMemoryUploadedFile to a file-like object
            image = Image.open(io.BytesIO(image_file.read()))
            image = image.resize((150, 150))  # Resize image to match model input
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image /= 255.0  # Rescale the image

            # Access the rice model from AppConfig
            app_config = apps.get_app_config('grain_harverst_app')
            model = app_config.rice_model
            if model:
                prediction = model.predict(image)
                predicted_class = np.argmax(prediction, axis=1)

                class_names = ['Arborio', 'Basmati', 'Ipsala', 'Jasmine', 'Karacadag']
                result = class_names[predicted_class[0]]
                return render(request, 'grain_harverst_app/predict_rice_quality.html', {'form': form, 'result': result})
            else:
                return render(request, 'grain_harverst_app/predict_rice_quality.html', {'form': form, 'error': 'Model not loaded. Check server logs.'})

    else:
        form = ImageUploadForm()
    return render(request, 'grain_harverst_app/predict_rice_quality.html', {'form': form})



def predict_maize_quality(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']

            image = Image.open(io.BytesIO(image_file.read()))
            image = image.resize((150, 150))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image /= 255.0

            # Access the maize model from AppConfig
            app_config = apps.get_app_config('grain_harverst_app')
            model = app_config.maize_model
            if model:
                prediction = model.predict(image)
                predicted_class = np.argmax(prediction, axis=1)

                class_names = ['Bad', 'Good']
                result = class_names[predicted_class[0]]
                return render(request, 'grain_harverst_app/predict_maize_quality.html', {'form': form, 'result': result})
            else:
                return render(request, 'grain_harverst_app/predict_maize_quality.html', {'form': form, 'error': 'Model not loaded. Check server logs.'})

    else:
        form = ImageUploadForm()
    return render(request, 'grain_harverst_app/predict_maize_quality.html', {'form': form})

def predict_wheat_quality(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']

            image = Image.open(io.BytesIO(image_file.read()))
            image = image.resize((150, 150))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image /= 255.0

            # Access the maize model from AppConfig
            app_config = apps.get_app_config('grain_harverst_app')
            model = app_config.maize_model
            if model:
                prediction = model.predict(image)
                predicted_class = np.argmax(prediction, axis=1)

                class_names = ['Good', 'Bad']
                result = class_names[predicted_class[0]]
                return render(request, 'grain_harverst_app/predict_wheat_quality.html', {'form': form, 'result': result})
            else:
                return render(request, 'grain_harverst_app/predict_wheat_quality.html', {'form': form, 'error': 'Model not loaded. Check server logs.'})

    else:
        form = ImageUploadForm()
    return render(request, 'grain_harverst_app/predict_wheat_quality.html', {'form': form})



# Views for Grain Stock Prediction

def load_model(model_filename):
    model_path = os.path.join(BASE_DIR, 'grain_harverst_app', model_filename)
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise Http404(f"The specified model file was not found: {model_path}")
    return model


def store_rice(request):
    model = load_model('Rice_stocking_prediction33.pkl')

    if request.method == 'POST':
        try:
            MaxT = float(request.POST.get('MaxT'))
            MinT = float(request.POST.get('MinT'))
            RH1 = float(request.POST.get('RH1'))
            RH2 = float(request.POST.get('RH2'))
            RF = float(request.POST.get('RF'))
            WS = float(request.POST.get('WS'))
            SSH = float(request.POST.get('SSH'))

            input_data = pd.DataFrame({
                'MaxT': [MaxT], 'MinT': [MinT], 'RH1(%)': [RH1], 'RH2(%)': [RH2],
                'RF(mm)': [RF], 'WS(kmph)': [WS], 'SSH(hrs)': [SSH]
            })

            prediction = model.predict(input_data)[0]
            return render(request, 'grain_harverst_app/store_rice_result.html', {'prediction': prediction})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'grain_harverst_app/store_rice.html')


def store_maize(request):
    model = load_model('maize_stocking_prediction33.pkl')

    if request.method == 'POST':
        try:
            MaxT = float(request.POST.get('MaxT'))
            MinT = float(request.POST.get('MinT'))
            RH1 = float(request.POST.get('RH1'))
            RH2 = float(request.POST.get('RH2'))
            RF = float(request.POST.get('RF'))
            WS = float(request.POST.get('WS'))
            SSH = float(request.POST.get('SSH'))

            input_data = pd.DataFrame({
                'MaxT': [MaxT], 'MinT': [MinT], 'RH1(%)': [RH1], 'RH2(%)': [RH2],
                'RF(mm)': [RF], 'WS(kmph)': [WS], 'SSH(hrs)': [SSH]
            })

            prediction = model.predict(input_data)[0]
            return render(request, 'grain_harverst_app/store_maize_result.html', {'prediction': prediction})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'grain_harverst_app/store_maize.html')


def store_wheat(request):
    model = load_model('wheat_stocking_prediction33.pkl')

    if request.method == 'POST':
        try:
            MaxT = float(request.POST.get('MaxT'))
            MinT = float(request.POST.get('MinT'))
            RH1 = float(request.POST.get('RH1'))
            RH2 = float(request.POST.get('RH2'))
            RF = float(request.POST.get('RF'))
            WS = float(request.POST.get('WS'))
            SSH = float(request.POST.get('SSH'))

            input_data = pd.DataFrame({
                'MaxT': [MaxT], 'MinT': [MinT], 'RH1(%)': [RH1], 'RH2(%)': [RH2],
                'RF(mm)': [RF], 'WS(kmph)': [WS], 'SSH(hrs)': [SSH]
            })

            prediction = model.predict(input_data)[0]
            return render(request, 'grain_harverst_app/store_wheat_result.html', {'prediction': prediction})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'grain_harverst_app/store_wheat.html')

def stockkeeper_dashboard(request):
    id = request.session.get('user_id')     
    user_detail = UsersTable.objects.filter(user_id=id).first()  


    return render(request, 'grain_harverst_app/stockkeeper_dashboard.html', {'user_detail':user_detail})

def send_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Assuming you have a way to identify the sender (John or Jane)
            sender = request.user.username
            
            # Here, you can handle saving the location data or broadcasting it to other users
            # Example: Save to database or send to other users in the chat room
            
            return JsonResponse({'status': 'Location shared successfully'})
        
        except json.JSONDecodeError as e:
            return HttpResponseBadRequest('Invalid JSON format')
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')
    

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Inventory, UsersTable
from django.db.utils import IntegrityError

# @login_required
def inventory_create(request):
    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        sent_quantity = request.POST.get('sent_quantity')
        supplier_id = request.POST.get('supplier_id')
        storekeeper_id = request.POST.get('storekeeper_id')
        
        user_id = request.session.get('user_id')
        role = request.session.get('role')
        
        if not user_id or not role:
            return render(request, 'grain_harverst_app/inventory_form.html', {
                'role': role, 
                'error': "User ID or role not found in session."
            })

        try:
            # Ensure that the farmer ID exists
            farmer = UsersTable.objects.get(user_id=user_id, role=UsersTable.FARMER)

            # Ensure that the supplier and storekeeper IDs exist
            supplier = UsersTable.objects.get(user_id=supplier_id, role=UsersTable.SUPPLIER)
            storekeeper = UsersTable.objects.get(user_id=storekeeper_id, role=UsersTable.STOCKKEEPER)

            # Create and save the inventory record
            inventory = Inventory(
                product_type=product_type,
                sent_quantity=sent_quantity,
                supplier=supplier,
                storekeeper=storekeeper,
                farmer=farmer  # Save farmer as a ForeignKey
            )
            inventory.save()

            return redirect('inventory_list')

        except UsersTable.DoesNotExist as e:
            return render(request, 'grain_harverst_app/inventory_form.html', {
                'role': role, 
                'error': f"User not found: {str(e)}"
            })
        except IntegrityError:
            return render(request, 'grain_harverst_app/inventory_form.html', {
                'role': role, 
                'error': "Integrity error occurred while saving inventory."
            })

    return render(request, 'grain_harverst_app/inventory_form.html', {'role': request.session['role']})



def inventory_update(request, pk):
    role = request.session.get('role')
    user_id = request.session.get('user_id')

    # Retrieve the inventory item
    inventory = get_object_or_404(Inventory, pk=pk)

    # Check if the current user has permission to update this inventory item
    if role == 'farmer' and inventory.farmer.user_id == user_id:
        if request.method == 'POST':
            product_type = request.POST.get('product_type')
            sent_quantity = request.POST.get('sent_quantity')
            supplier_id = request.POST.get('supplier_id')
            storekeeper_id = request.POST.get('storekeeper_id')

            try:
                # Fetch the supplier and storekeeper for validation
                supplier = UsersTable.objects.get(user_id=supplier_id, role=UsersTable.SUPPLIER)
                storekeeper = UsersTable.objects.get(user_id=storekeeper_id, role=UsersTable.STOCKKEEPER)
            except UsersTable.DoesNotExist:
                return render(request, 'grain_harverst_app/inventory_update.html', {
                    'role': role,
                    'error': "Supplier or Storekeeper not found."
                })

            # Update inventory fields
            inventory.product_type = product_type
            inventory.sent_quantity = sent_quantity
            inventory.supplier = supplier
            inventory.storekeeper = storekeeper

            try:
                inventory.save()
                return redirect('inventory_list')
            except IntegrityError:
                return render(request, 'grain_harverst_app/inventory_update.html', {
                    'role': role,
                    'error': "Integrity error occurred while saving inventory."
                })

        return render(request, 'grain_harverst_app/inventory_update.html', {
            'inventory': inventory,
            'role': role
        })
    else:
        return redirect('inventory_list')
# @login_required
# views.py

def inventory_update_recieved(request, pk):
    if request.session['role'] != 'stockkeeper':
        return redirect('inventory_list')  # Redirect non-storekeepers to the list view
    
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        received_quantity = request.POST.get('received_quantity')  # Update received_quantity
        inventory.received_quantity = received_quantity
        inventory.save()
        return redirect('inventory_list_storekeeper')
    
    return render(request, 'grain_harverst_app/storekeeper_receive.html', {'inventory': inventory, 'role': 'stockkeeper'})
from django.shortcuts import render
from .models import Inventory, UsersTable

def inventory_list(request):
    role = request.session.get('role')
    user_id = request.session.get('user_id')

    print(f"Role: {role}, User ID: {user_id}")  # Debugging output

    if role == 'farmer':
        try:
            farmer = UsersTable.objects.get(user_id=user_id, role=UsersTable.FARMER)
            inventories = Inventory.objects.filter(farmer=farmer)
        except UsersTable.DoesNotExist:
            inventories = []
    elif role == 'stockkeeper':
        try:
            stockkeeper = UsersTable.objects.get(user_id=user_id, role=UsersTable.STOCKKEEPER)
            inventories = Inventory.objects.filter(storekeeper=stockkeeper)
        except UsersTable.DoesNotExist:
            inventories = []
    else:
        inventories = Inventory.objects.all()  # or handle other roles as needed

    print(f"Inventories: {inventories}")  # Debugging output

    context = {'inventories': inventories, 'role': role}
    return render(request, 'grain_harverst_app/inventory_list.html', context)

def inventory_list_storekeeper(request):
    role = request.session.get('role')
    user_id = request.session.get('user_id')

    print(f"Role: {role}, User ID: {user_id}")  # Debugging output

    if role == 'stockkeeper':
        try:
            stockkeeper = UsersTable.objects.get(user_id=user_id, role=UsersTable.STOCKKEEPER)
            inventories = Inventory.objects.filter(storekeeper=stockkeeper)
        except UsersTable.DoesNotExist:
            inventories = []
    else:
        inventories = Inventory.objects.all()  # or handle other roles as needed

    print(f"Inventories: {inventories}")  # Debugging output

    context = {'inventories': inventories, 'role': role}
    return render(request, 'grain_harverst_app/inventory_list_storekeeper.html', context)

# @login_required
def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventory_list')
    
    return render(request, 'grain_harverst_app/inventory_confirm_delete.html', {'inventory': inventory})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import UsersTable
import logging
from .forms import ChatMessageForm

logger = logging.getLogger(__name__)

def get_user_name(request, user_id, role):
    logger.info(f"Fetching user with ID: {user_id} and role: {role}")
    try:
        user = get_object_or_404(UsersTable, user_id=user_id, role=role)
        logger.info(f"Found user: {user.user_name}")
        return JsonResponse({'user_name': user.user_name})
    except UsersTable.DoesNotExist:
        logger.error(f"User not found with ID: {user_id} and role: {role}")
        return JsonResponse({'error': 'User not found'}, status=404)
def admin_portal(request):
    users = UsersTable.objects.all()
    return render(request, 'grain_harverst_app/admin_portal.html', {'users': users})


def supplier_dashboard(request):
    return render(request, 'grain_harverst_app/supplier_dashboard.html', {})


from django.shortcuts import render, get_object_or_404
from .models import ChatMessage  # Adjust import as per your actual model

def chat_message_detail(request, pk):
    print("PK received:", pk)  # Check if PK is correctly received
    message = get_object_or_404(ChatMessage, pk=pk)
    print("Message:", message)  # Check the retrieved message object
    return render(request, 'grain_harverst_app/chatmessage_detail.html', {'message': message})


from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import ChatMessage

def chat_message_list(request):
    user_name = request.session.get('user_name')
    if user_name:
        # Filter messages where the user is either the sender or the recipient and order by timestamp
        messages = ChatMessage.objects.filter(sender__user_name=user_name) | ChatMessage.objects.filter(recipient__user_name=user_name)
        messages = messages.order_by('-timestamp')  # Order by timestamp in descending order

        # Implement pagination
        paginator = Paginator(messages, 10)  # Show 10 messages per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'grain_harverst_app/chatmessage_list.html', {'page_obj': page_obj})
    else:
        # Handle case where user_name is not found in session
        # Redirect to login page or show an error message
        return redirect('login')

 

def chat_message_create(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            user_name = request.session.get('user_name', None)
            if user_name:
                chat_message.sender = UsersTable.objects.get(user_name=user_name)  # Fetch sender using user_name from session
                chat_message.save()
                return redirect('chat_message_list')  # Replace with your actual redirect URL
            else:
                
                return redirect('login')  # Replace with your login URL
    else:
        form = ChatMessageForm()
    return render(request, 'grain_harverst_app/chatmessage_form.html', {'form': form})

def chat_message_update(request, pk):
    message = get_object_or_404(ChatMessage, pk=pk)
    if request.method == 'POST':
        form = ChatMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_message_list')  # Correct the redirect name if necessary
    else:
        form = ChatMessageForm(instance=message)
    return render(request, 'grain_harverst_app/chatmessage_form.html', {'form': form})


def chat_message_list_farmer(request):
    user_name = request.session.get('user_name')
    if user_name:
        # Filter messages where the user is either the sender or the recipient
        messages = ChatMessage.objects.filter(sender__user_name=user_name) | ChatMessage.objects.filter(recipient__user_name=user_name)
        messages = messages.order_by('-timestamp')
       
        # Implement pagination
        paginator = Paginator(messages, 10)  # Show 10 messages per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'grain_harverst_app/chatmessage_list_farmer.html', {'page_obj': page_obj})
    else:
        # Handle case where user_name is not found in session
        # Redirect to login page or show an error message
        return redirect('login')

def chat_message_create_farmer(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            user_name = request.session.get('user_name', None)
            if user_name:
                chat_message.sender = UsersTable.objects.get(user_name=user_name)  # Fetch sender using user_name from session
                chat_message.save()
                return redirect('chat_message_list_farmer')  # Replace with your actual redirect URL
            else:
                
                return redirect('login')  # Replace with your login URL
    else:
        form = ChatMessageForm()
    return render(request, 'grain_harverst_app/chatmessage_form_farmer.html', {'form': form})

def chat_message_update_famer(request, pk):
    message = get_object_or_404(ChatMessage, pk=pk)
    if request.method == 'POST':
        form = ChatMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_message_list_farmer')  # Correct the redirect name if necessary
    else:
        form = ChatMessageForm(instance=message)
    return render(request, 'grain_harverst_app/chatmessage_form_farmer.html', {'form': form})

from .models import Contact

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        phone = request.POST.get('Phone')
        message = request.POST.get('Message')
        
        if name and email and phone and message:
            Contact.objects.create(name=name, email=email, phone=phone, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'grain_harverst_app/index.html')


def success_view(request):
    contacts = Contact.objects.all()
    return render(request, 'grain_harverst_app/success.html', {'contacts': contacts})