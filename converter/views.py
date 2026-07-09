from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversionSerializer
from PIL import Image
import io
import pillow_avif
import base64

class ConvertImageView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ConversionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            image_file = validated_data['image']
            output_format = validated_data['output_format']
            quality = validated_data['quality']
            width = validated_data.get('width')
            height = validated_data.get('height')

            try:
                img = Image.open(image_file)

                # Handle RGBA to RGB for formats that don't support alpha
                if img.mode == 'RGBA' and output_format in ['jpeg']:
                    img = img.convert('RGB')

                if width and height:
                    img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
                elif width:
                    w_percent = (int(width) / float(img.size[0]))
                    h_size = int((float(img.size[1]) * float(w_percent)))
                    img = img.resize((int(width), h_size), Image.Resampling.LANCZOS)
                elif height:
                    h_percent = (int(height) / float(img.size[1]))
                    w_size = int((float(img.size[0]) * float(h_percent)))
                    img = img.resize((w_size, int(height)), Image.Resampling.LANCZOS)

                output_buffer = io.BytesIO()
                img.save(output_buffer, format=output_format, quality=quality)
                output_buffer.seek(0)

                image_base64 = base64.b64encode(output_buffer.read()).decode('utf-8')
                
                original_filename = image_file.name.rsplit('.', 1)[0]
                filename = f"{original_filename}.{output_format}"

                response_data = {
                    'image_data': image_base64,
                    'filename': filename
                }
                
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': f"Conversion failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
