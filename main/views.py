from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
import os

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = file.name

            # Save uploaded file temporarily
            temp_path = f"/tmp/{file_name}"
            with open(temp_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Read file using pandas
            try:
                df = pd.read_excel(temp_path)
                data = df.head(10).to_dict(orient='records')  # Preview first 10 rows
            except Exception as e:
                data = {"error": str(e)}

            # Save info to DB
            UploadedFile.objects.create(file_name=file_name, file_data=data)

            os.remove(temp_path)
            return render(request, 'main/upload_success.html', {'file_name': file_name})

    else:
        form = UploadFileForm()

    return render(request, 'main/upload.html', {'form': form})
