import time
from datetime import datetime
from django.db.models import Sum
import cloudinary.uploader
import cloudinary.api
from cloudinary.exceptions import Error

from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib import messages
from .models import Trash, TrashCompartment, TrashArea

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

API_KEY = 'f45150a8be4fd46f3857b22c96ce7053'

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)


            return redirect('home') 
        else:
            messages.error(request, "Tên người dùng hoặc mật khẩu không đúng.")
    
    return render(request, 'app/login.html')

@login_required
def logout(request):
    auth_logout(request)  
    return redirect('/api/login') 

@login_required
def home(request):
    trash_areas = TrashArea.objects.all()

    context = {
        'trash_areas': trash_areas
    }

    return render(request, 'app/home.html', context)

@api_view(['POST'])
def uploadImage(request):
    if request.method == 'POST':
        # Kiểm tra xem có file 'image' trong request.FILES không
        if 'image' in request.FILES:
            # Kiểm tra xem API key có hợp lệ không
            api_key = request.headers.get('api_key')
            if api_key != API_KEY:
                return JsonResponse({'status': 'error', 'message': 'Invalid API key'}, status=403)
            
            # Lấy dữ liệu từ request.POST
            image = request.FILES['image']
            trash_area_id = request.POST.get('trash_area_id')
            trash_compartment_label = request.POST.get('trash_compartment_label')

            # Kiểm tra nếu không có trash_area_id
            if not trash_area_id:
                return JsonResponse({'status': 'error', 'message': 'trash_area_id is required'}, status=400)
            else:
                # Lấy trash_area từ trash_area_id
                try:
                    trash_area = TrashArea.objects.get(id=trash_area_id)
                except TrashArea.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'TrashArea not found'}, status=404)

            # Kiểm tra nếu không có trash_compartment_label
            if not trash_compartment_label:
                return JsonResponse({'status': 'error', 'message': 'trash_compartment_label is required'}, status=400)
            else:
                # Lấy trash_compartment từ trash_area_id và trash_compartment_label
                try:
                    trash_compartment = TrashCompartment.objects.get(id_trash_area=trash_area, label=trash_compartment_label)
                except TrashCompartment.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'TrashCompartment not found'}, status=404)  
                
            
            # Tạo ra public_id từ trash_area_id, trash_compartment_label và timestamp
            public_id_value = f"{trash_area_id}_{trash_compartment_label}_{int(time.time())}"

            # Upload ảnh lên Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(
                    image,
                    public_id = public_id_value,
                    folder= "trash_images"  # Thư mục trên Cloudinary (tuỳ chọn)
                )
                
                # Lấy URL và public_id từ phản hồi của Cloudinary
                trash_img_url = upload_result['secure_url']
                trash_img_public_id = upload_result['public_id']

                # Tạo bản ghi mới trong mô hình Trash
                trash = Trash(
                    id_trash_area=trash_area,
                    id_trash_compartment=trash_compartment,
                    trash_img_url=trash_img_url,
                    trash_img_public_id=trash_img_public_id,
                    date=datetime.now(),
                    quantity=1
                )
                trash.save()

                return Response({"status": "success", "data": upload_result}, status=200)

            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)

        else:
            return JsonResponse({'status': 'error', 'message': 'Image not found in request'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@api_view(['GET'])
def getTrashData(request ,trash_area_id):
    trash_compartment = TrashCompartment.objects.filter(id_trash_area=trash_area_id).all()
    trash_data = Trash.objects.filter(id_trash_area=trash_area_id).all().order_by('-date') 
    
    data = {
        'trash_compartment': [
            {
                'id': compartment.id,
                'label': compartment.label
            } for compartment in trash_compartment
        ],
        'trash_data': [
            {
                'id': trash.id,
                'id_trash_compartment': trash.id_trash_compartment.id,
                'trash_img_url': trash.trash_img_url,
                'label': trash.id_trash_compartment.label,
                'date': trash.date.strftime('%d/%m/%Y %H:%M:%S'),
                'quantity': trash.quantity
            } for trash in trash_data
        ]

    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def getTrashProgess(request, trash_area_id):
    # Lấy tất cả TrashCompartment thuộc trash_area_id
    trash_compartments = TrashCompartment.objects.filter(id_trash_area=trash_area_id)

    # Khởi tạo danh sách dữ liệu trả về
    data = {
        'trash_compartments': []
    }

    # Duyệt qua từng TrashCompartment để tính tổng quantity và phần trăm
    for compartment in trash_compartments:
        total_quantity = Trash.objects.filter(
            id_trash_compartment=compartment
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0  # Sử dụng 0 nếu không có kết quả

        # Tính phần trăm dựa trên max_quantity của TrashCompartment
        total_capacity = compartment.max_quantity  
        percentage = (total_quantity / total_capacity) * 100 if total_capacity > 0 else 0

        # Thêm thông tin TrashCompartment vào dữ liệu trả về
        data['trash_compartments'].append({
            'id': compartment.id,
            'label': compartment.label,
            'max_quantity': compartment.max_quantity,
            'total_quantity': total_quantity,
            'percentage': round(percentage, 2),
        })

    return JsonResponse(data, safe=False)

@api_view(['GET'])
def resetProgress(request, trash_compartment_id):
    # Lấy TrashCompartment từ trash_compartment_id
    try:
        compartment = TrashCompartment.objects.get(id=trash_compartment_id)
    except TrashCompartment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'TrashCompartment not found'}, status=404)

    # Lấy tất cả Trash thuộc TrashCompartment
    trash_data = Trash.objects.filter(id_trash_compartment=compartment)

    # Lấy danh sách các public_id của ảnh cần xóa
    public_ids_to_delete = [trash.trash_img_public_id for trash in trash_data if trash.trash_img_public_id]

    if public_ids_to_delete:
        try:
            # Xóa nhiều ảnh trên Cloudinary cùng lúc
            cloudinary.api.delete_resources(public_ids_to_delete)
        except Error as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to delete images from Cloudinary: {str(e)}'}, status=500)

    # for public_id in public_ids_to_delete:
    #     try:
    #         cloudinary.api.delete_resources(public_id)
    #     except Error as e:
    #         print(f"Cloudinary error details: {str(e)}")  # Kiểm tra log để biết chi tiết lỗi
    #         return JsonResponse({'status': 'error', 'message': f'Failed to delete images from Cloudinary: {str(e)}'}, status=500)
        
    # Xóa tất cả Trash
    trash_data.delete()

    # Cập nhật empty_count của TrashCompartment về 1
    compartment.empty_count += 1
    compartment.save()

    return JsonResponse({'status': 'success', 'message': 'Trash data has been reset, images deleted from Cloudinary, and empty_count updated'}, status=200)

@api_view(['GET'])
def getTrashDataToChart(request, trash_area_id):
    # Lấy tất cả các TrashCompartment thuộc TrashArea với trash_area_id
    compartments = TrashCompartment.objects.filter(id_trash_area_id=trash_area_id)

    # Lưu trữ dữ liệu trả về cho biểu đồ
    labels = []  # Danh sách tên các ngăn rác
    data = []  # Danh sách số lượng rác tương ứng

    # Lặp qua các TrashCompartment và lấy số lượng rác trong mỗi ngăn
    for compartment in compartments:
        # Lấy tất cả các Trash trong TrashCompartment hiện tại
        trash_data = Trash.objects.filter(id_trash_compartment=compartment)

        # Tính tổng số lượng rác trong ngăn rác này
        total_trash = trash_data.aggregate(Sum('quantity'))['quantity__sum'] or 0  # Nếu không có rác thì lấy 0

        # Thêm tên ngăn rác và tổng số lượng vào dữ liệu trả về
        labels.append(compartment.label)
        data.append(total_trash)

    # Tính tổng số lượng rác không có TrashCompartment (id_trash_compartment = null)
    other_trash_data = Trash.objects.filter(id_trash_compartment__isnull=True, id_trash_area_id=trash_area_id)
    total_other_trash = other_trash_data.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Nếu có rác không thuộc bất kỳ TrashCompartment nào, thêm "Other" vào nhãn
    if total_other_trash > 0:
        labels.append("Other")
        data.append(total_other_trash)

    # Trả về dữ liệu dưới dạng JSON
    return JsonResponse({
        'labels': labels,
        'data': data  
    })

@api_view(['GET'])
def getTrashAreaDataForEsp32(request, trash_area_id):
    # Kiểm tra xem API key có hợp lệ không
    api_key = request.headers.get('api_key')
    if api_key != API_KEY:
        return JsonResponse({'status': 'error', 'message': 'Invalid API key'}, status=403)

    # Lấy tất cả TrashCompartment thuộc trash_area_id
    trash_compartments = TrashCompartment.objects.filter(id_trash_area=trash_area_id)

    # Khởi tạo danh sách dữ liệu trả về
    data = {}

    # Duyệt qua từng TrashCompartment để tính tổng quantity và phần trăm
    for compartment in trash_compartments:
        total_quantity = Trash.objects.filter(
            id_trash_compartment=compartment
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0  
        
        max_quantity = compartment.max_quantity  
        percentage = (total_quantity / max_quantity) * 100 if max_quantity > 0 else 0

        if percentage > 80:
            status = 'full'
        elif percentage > 60:
            status = 'warning'
        else:
            status = 'normal'

        # Thêm thông tin TrashCompartment vào dữ liệu trả về
        data[compartment.label] = {
            'max_quantity': compartment.max_quantity,
            'total_quantity': total_quantity,
            'percentage': round(percentage, 2),
            'status': status
        }

    return JsonResponse(data, safe=False)

