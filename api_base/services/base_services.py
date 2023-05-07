from django.core.files.storage import FileSystemStorage
from datetime import datetime


class BaseService:

    @classmethod
    def upload_file(cls, file):
        fs = FileSystemStorage()
        current_date = datetime.now()
        file_name = fs.save(name=current_date.strftime("%m_%d_%Y,%H_%M_%S_") + file.name, content=file)
        print("aa")
        return fs.url(file_name)
