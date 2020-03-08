from os import listdir
from os.path import isfile, join
import os
import shutil


class FileTypes:
    def __init__(self) -> None:
        self.Documents = [".doc", ".docx", ".pdf"]
        self.Installers = [".exe", ".msi"]
        self.Images = [".png", ".jpg", ".jpeg"]


def get_all_the_files(path: str) -> None:
    files = [f for f in listdir(path) if isfile(join(path, f))]
    filetypes = FileTypes()
    file_type_variation_list = []
    for key, value in filetypes.__dict__.items():
        # print(f"Key: {key}, Value : {value}")
        new_folder = path + '\\' + str(key)
        print(new_folder)

        for file in files:
            filename, file_extension = os.path.splitext(file)
            src_path = path + "/" + file
            if file_extension in value:
                src_path = path + "/" + file
                dest_path = new_folder + "/" + file
                if os.path.isdir(new_folder):  # folder exists
                    pass
                else:
                    os.mkdir(new_folder)
                shutil.move(src_path, dest_path)

            else:
                file_type_variation_list.append(file_extension)
                new_folder_name = mypath + '/' + file_extension + '_folder'
                # filetypes.__dict__[str(file_extension)] = str(new_folder_name)
                if os.path.isdir(new_folder_name):  # folder exist
                    pass
                else:
                    os.mkdir(new_folder_name)
                shutil.move(src_path, new_folder_name)


if __name__ == "__main__":
    mypath = r'C:\Users\AshunKothari\Downloads\Dummy'
    get_all_the_files(path=mypath)
