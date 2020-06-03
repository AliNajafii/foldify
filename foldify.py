import os
import pathlib
import copy

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
            for root,dirs,files in os.walk(folderpath):
                level = root.replace(folderpath,'').count(os.sep)
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
        info = f"""
                total files : {self.handler.get_files_number()}
                total folders : {self.handler.get_folder_number()}
                largest file : {self.handler.get_file_path(self.handler.get_largest_file())} --> {self.show_size(self.handler.get_file_size(self.handler.get_largest_file()))}
                largest folder : {self.handler.get_folder_path(self.handler.get_largest_folder())} --> {self.show_size(self.handler.get_folder_size(self.handler.get_largest_folder()))}
        """
        print(info)

        if show_folder_childs:
            if show_folder_childs_file:
                print('files and folders :')
                self.handler.show_folder_childs(path=self.path,show_files=True)
            else:
                print('folders:')
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

class Handler(FileHandler):
    
    """
    this is File Handler class wich has memory performance.
    using iter tools and function to use less memory for larg directories
    note: it migth less speed!
    """

    def __init__(self,path,*args,**kwargs):
        super().__init__(path,*args,**kwargs)
        
    
    def setup(self):
        super().setup()
        self.set_files_performed(self.files) 
        self.set_folders_perforemd(self.folders) 
        self.set_folders_by_size_perforemd(self._folders_by_size)
        self.set_files_by_size_performed(self._files_by_size)
        self.set_files_dir_performed(self.files_dir)
        self.set_folders_dir_performed(self.folders_dir)
        
    def bluh(self):
        pass
    def set_files_performed(self,files):
        """
        this method make list of self.files to iter obj
        """
        self.files = iter(files)

        

    def set_folders_perforemd(self,folders):
        """
        this method make list of self.folders to iter obj
        """
        self.folders = iter(folders)

    def set_folders_by_size_perforemd(self,folder_dic):
        """
        this method make list of self.folders_by_size to zip obj
        exp : next(self.folders_by_size) --> (folder_name,size)
        """

        self._folders_by_size = zip(folder_dic.keys(),folder_dic.values())

    def set_files_by_size_performed(self,files_dic):
        """
        this method make list of self._files_by_size to zip obj
        exp : next(self._files_by_size) --> (file_name,size)
        """

        self._files_by_size = zip(files_dic.keys(),files_dic.values())

    def set_files_dir_performed(self,files_dic):
        """
        this method make list of self.files_dir to zip obj
        exp : next(self.files_dir) --> (file_name,path)
        """
        self.files_dir = zip(files_dic.keys(),files_dic.values())


    def set_folders_dir_performed(self,folders_dic):
        """
        this method make list of self.folders_dir to zip obj
        exp : next(self.folder_dir) --> (folder_name,path)
        """
        self.folders_dir = zip(folders_dic.keys(),folders_dic.values())

    def get_files(self):
        return copy.deepcopy(self.files)
    
    def get_folders(self):
        return copy.deepcopy(self.folders)

    def get_files_by_size(self):
        return copy.deepcopy(self._files_by_size)
    
    def get_folder_by_size(self):
        return copy.deepcopy(self._folders_by_size)

    def get_files_dir(self):
        return copy.deepcopy(self.files_dir)
    
    def get_folders_dir(self):
        return copy.deepcopy(self.folders_dir)

    def get_file_path(self,file):
        dirs = self.get_files_dir()
        if isinstance(dirs,dict):
            return super().get_file_path(file)
        while True :
            try:
                file_path = next(dirs)
            except StopIteration:
                raise FileNotFoundError(f'{file} not found in {self.path} sub directories')
            if file_path[0] == file: 
                return file_path[1] # returns the path
    
    def get_folder_path(self,folder):
        dirs = self.get_folders_dir()
        if isinstance(dirs,dict):
            return super().get_folder_path(folder)
        while True:
            try:
                folder_path = next(dirs)
            except StopIteration :
                raise FolderNotFound(f'{folder} not found in {self.path} sub directories')
            if folder_path[0] == folder:
                return folder_path[1]

    def get_files_number(self):
        files = self.get_files()
        counter = 0
        while True:
            try:
                f = next(files)
                counter+=1
                del(f)
            except StopIteration:
                return counter

    def get_folders_number(self):
        folders = self.get_folders()
        counter = 0 
        while True:
            try:
                fol = next(folders)
                counter+=1
                del(fol)
            except StopIteration:
                return counter

    def get_largest_file(self):
        size_file = self.get_files_by_size()
        max_size = 0
        while True:
            try:
                s = next(size_file)[0] # get size from tuple
            except StopIteration:
                return max_size

            if s > max_size:
                max_size=s

    
class FolderNotFound(Exception):
    def __init__(self,*args):
        super().__init__(*args)

# d = input('Please enter a directory:\t')
# # fm = FileManager(path=d)
# # fm.get_info()
# h = Handler(d)
# h.setup()
# print('folder number :',h.get_folders_number())
# print('file number :',h.get_files_number())

