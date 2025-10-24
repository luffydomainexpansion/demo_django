from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
import os
import traceback
import logging

logger = logging.getLogger(__name__)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = file.name
            temp_path = f"/tmp/{file_name}"

            try:
                with open(temp_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                import pandas as pd
                df = pd.read_excel(temp_path)
                data = df.head(10).to_dict(orient='records')

                # ✅ This is where it may crash (DB save)
                from .models import UploadedFile
                UploadedFile.objects.create(file_name=file_name, file_data=data)

                os.remove(temp_path)
                return render(request, 'main/upload_success.html', {'file_name': file_name})

            except Exception as e:
                logger.error("Upload failed", exc_info=True)
                return render(request, 'main/upload.html', {
                    'form': form,
                    'error': str(e)
                })
