from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
import tempfile
import os
import json

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = file.name

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name

            # Read file using pandas
            try:
                df = pd.read_excel(temp_path)
                data = df.head(10).replace({pd.NA: None}).to_dict(orient='records')
                data = json.loads(json.dumps(data, default=str))  # make it JSON serializable
            except Exception as e:
                data = {"error": str(e)}

            # Save info to DB
            try:
                UploadedFile.objects.create(file_name=file_name, file_data=data)
            except Exception as e:
                print("DB Save Error:", e)

            os.remove(temp_path)
            return render(request, 'main/upload_success.html', {'file_name': file_name})

    else:
        form = UploadFileForm()

    return render(request, 'main/upload.html', {'form': form})
