from django.shortcuts import render
from cloudinary.uploader import upload_image
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def image_upload(request):
    context = {}
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        if not image:
            context['error'] = 'No image provided'
        else:
            try:
                image = upload_image(image)
                context = {
                    'url': image.build_url(),
                    'public_id': image.public_id,
                    'format': image.format
                }
            except Exception as e:
                context['error'] = 'Image upload failed'
    return render(request, 'upload_image.html', context)