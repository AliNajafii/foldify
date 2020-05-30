import os
import pathlib

class FileHandler:

    def __init__(self,path,*args,**kwarg):
        self.path = str(path)
        self.path_size = 0
        self.files = []
        self.folders =[]
        self.files_dir = {} #{file: C://path/to/file}
        self.folders_dir = {}
        # self.reper_dict --->
        #{
            #folder1 : {
                #         file1 :size
                            #...
                  #...      #}
                #}
        self._reper_dict = {} 
        self._folders_by_size = {} # {size:folder}
        self._files_by_size = {} #{size:file}

    def __str__(self):
        return f'< class {self.__class__.__name__}  {self.path} >'

    def setup(self):
        """
        this method runs sizing and representation and instanciating properties.
        """
        self.walk()
        self.__set_files_by_size()
        self.__set_folders_by_size()
        self.__set_path_size()

    def walk(self):
        for dirpath,folders,files in os.walk(self.path):
            for file in files:
                self.files.append(file)
                self.files_dir.update({
                    file:os.path.join(dirpath,file)
                    })

            for folder in folders:
                self.folders.append(folder)
                self.folders_dir.update({
                    folder: os.path.join(dirpath,folder)
                })

    def get_files_number(self):
        return len(self.files)

    def get_folder_number(self):
        return len(self.folders)


    def get_folder_size(self,folder):
        return os.path.getsize(self.get_folder_path(folder))

    def get_folder_path(self,folder):
        try:
            return self.folders_dir[folder]
        except KeyError:
            raise FolderNotFound(f'This Folder Not exists in {self.path} directories ')

    def get_file_size(self,filename):
        file_dir = self.get_file_path(filename)
        return os.path.getsize(file_dir)


    def get_file_path(self,filename):

        try:
            file_dir = self.files_dir[filename]
            return file_dir
        except KeyError:
            raise FileNotFoundError(f'This file does not exists in {self.path} and its directories.')

    def __set_files_by_size(self):
        for file in self.files:
            file_path = self.get_file_path(file)
            self._files_by_size.update({
                self.get_file_size(file):file
                })
    
    def __set_folders_by_size(self):
        for folder in self.folders :
            folder_path = self.get_folder_path(folder)
            self._folders_by_size.update({
                os.path.getsize(folder_path):folder
            })

        
    def __set_path_size(self):
        self.path_size = sum(self._files_by_size.keys())


    def get_full_size(self):
        self.__set_path_size()
        return self.path_size

    def get_largest_file(self):
        return self._files_by_size[max(self._files_by_size.keys())]
    
    def get_largest_folder(self):
        return self._folders_by_size[max(self._folders_by_size.keys())]

    def __get_indent(self,level):
        return ' '*4*(level)

    def show_folder_childs(self,*args,**kwargs):
        folder = kwargs.get('folder')
        folderpath = kwargs.get('path')
        show_files = kwargs.get('show_files')
        if folder :
            abs_path = self.get_folder_path(folder)
            for root,dirs,files in os.walk(abs_path):
                level = root.replace(abs_path, '').count(os.sep)
                print('~{}{}/'.format(self.__get_indent(level), os.path.basename(root)))
                subindent = ' ' * 4 * (level + 1)
                if show_files:
                    for f in files:
                        print('|{}{}'.format(subindent, f))

        elif folderpath:
            for roots,dirs,files in os.walk(folderpath):
                level = root.replace(folderpath).count(os.sep)
                print('~{}{}/'.format(self.__get_indent(level), os.path.basename(root)))
                subindent = ' ' * 4 * (level + 1)
                if show_files:
                    for f in files:
                        print('|{}{}'.format(subindent, f))

        else:
            raise ValueError('no valid variables')

         
       
        
		
class FileManager:
    def __init__(self,path,file_handler=FileHandler,*args,**kwargs):
        self.path = path
        self.handler = file_handler(self.path)

    def get_info(self,show_folder_childs=False,show_folder_childs_file=False):

        self.handler.setup()
        print(f"""
                total files : {self.handler.get_files_number()}
                total folders : {self.handler.get_folder_number()}
                largest file : {self.handler.get_file_path(self.handler.get_largest_file())} --> {self.show_size(self.handler.get_file_size(self.handler.get_largest_file()))}
                largest folder : {self.handler.get_folder_path(self.handler.get_largest_folder())} --> {self.show_size(self.handler.get_folder_size(self.handler.get_largest_folder()))}
        """)

        if show_folder_childs:
            if show_folder_childs_file:
                self.handler.show_folder_childs(path=self.path,show_files=True)
            else:
                self.handler.show_folder_childs(path=self.path)

    def show_size(self,size):
        """
        this method show size in byte, kb,mb or gb and return string
        """
        if size<1000 :
            return f"{size} Bytes"
        elif 1000<= size <= 999999 :
            return f'{size/1000} KB'
        elif 10**6 <= size < 999999999:
            return f'{size/10**6} MB'

        else :
            return f'{size/10**9} GB'





    

class FolderNotFound(Exception):
    def __init__(self,*args):
        super().__init__(*args)


fm = FileManager(path='E:\\Computer engineering\\Projects\\RealProjects')
fm.get_info()