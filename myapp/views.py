from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io
import os
import traceback
import uuid 

# Load environment variables from .env file
load_dotenv()

# Configure Google generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Khởi tạo mô hình chỉ một lần
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
model_pro = genai.GenerativeModel(model_name="gemini-1.5-pro")

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES.get('image')
            p = request.POST.get('prompt')
            if not image_file:
                return JsonResponse({'status': 'error', 'message': 'No image provided'}, status=400)
       
            prompt = f"Dịch các đoạn bong bóng chat của ảnh sau sang tiếng việt theo thể loại truyện tranh {p}"

            # Đọc hình ảnh từ yêu cầu HTTP và chuyển đổi sang định dạng PIL
            image = Image.open(image_file)

            # # Tạo một tên file duy nhất bằng uuid để tránh ghi đè
            # unique_filename = f"{uuid.uuid4()}.png" 

            # # Lưu ảnh vào thư mục hiện tại với tên file duy nhất
            # image.save(unique_filename)

            # Tạo yêu cầu đến mô hình của Google
            response = model.generate_content([
                prompt,
                image
            ])

            # Trả về kết quả từ mô hình
            # print(response.text)
            return JsonResponse({'status': 'success', 'response': response.text})
        except Exception as e:
            # Log the full error traceback
            try:
                response = model_pro.generate_content([
                    prompt,
                    image
                ])
                return JsonResponse({'status': 'success', 'response': response.text + " (pro)"})
            except:
                 return JsonResponse({'status': 'error', 'message': 'Gemini 1.5 không nhận diện được, thử điểu chỉnh chiều cao của khung rồi dịch lại hoặc bỏ qua!'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)