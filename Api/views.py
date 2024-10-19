from django.shortcuts import render
from cloudinary.uploader import upload_image, destroy
from django.http import JsonResponse

def image_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        if not image:
            return JsonResponse(data={'error': 'No image provided'}, status=400)
        try:
            image = upload_image(image)
            context = {
                'url': image.build_url(),
                'public_id': image.public_id,
                'format': image.format
            }
            return render(request, 'upload_image.html', context)
        except Exception as e:
            return JsonResponse(data={'error': 'Image upload failed'}, status=400)
    else:
        return render(request, 'upload_image.html')