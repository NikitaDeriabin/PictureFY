import pandas as pd
import io
import zipfile
import rarfile
import os


class FileHandler:

    def to_jpeg_filename(self, path):
        file_name_with_extension = os.path.basename(path)
        file_name_without_extension = os.path.splitext(file_name_with_extension)[0]

        return file_name_without_extension + ".jpeg"

    def to_csv(self, data):
        df = pd.DataFrame(data=data)
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        return buffer

    def to_zip_buffer(self, data):
        with io.BytesIO() as archive_buffer:
            with zipfile.ZipFile(archive_buffer, 'w') as res_zip:
                for i in data:
                    res_zip.writestr(i[0], self.to_jpeg(i[1]))

            buffer_content = archive_buffer.getvalue()

        return buffer_content

    def clear_buffer(self, buffer):
        buffer.seek(0)
        buffer.truncate()

    def __get_archive_class(self, archive):
        return zipfile.ZipFile if str(archive).endswith("zip") else rarfile.RarFile

    def get_files_from_archive(self, archive):
        archive_cls = self.__get_archive_class(archive)

        with archive_cls(archive, 'r') as arc:
            filenames = arc.namelist()
            for filename in filenames:
                if filename.endswith("/"):
                    continue
                with arc.open(filename, 'r') as file:
                    yield file

    def to_jpeg(self, file):
        with io.BytesIO() as buffer:
            file.save(buffer, format='JPEG')
            jpg_data = buffer.getvalue()

        return jpg_data

    def check_archives_file_amount(self, archive1, archive2):
        archive1_cls = self.__get_archive_class(archive1)
        archive2_cls = self.__get_archive_class(archive2)

        with archive1_cls(archive1, 'r') as archive:
            archive1_files_amount = len(archive.namelist())

        with archive2_cls(archive2, 'r') as archive:
            archive2_files_amount = len(archive.namelist())

        return archive1_files_amount == archive2_files_amount



