import os, glob, json
encodeJSON = json.JSONEncoder().encode
decodeJSON = json.JSONDecoder().decode

class Path:
    join          = os.path.join
    directoryName = os.path.dirname

    @staticmethod
    def exists(path:str) -> bool:
        'check if `path` exists. returns True/False'
        return os.path.exists(path)

    @staticmethod
    def isDirectory(path:str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def isFile(path:str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def createDirectory(path:str) -> dict[str,bool|str]:
        '''
        attempt to create a directory provided in `path`. 
        
        NB: if any intermediate directories dont exist, they will be created as well

        returns the standard dict with `status` and `log`
        '''
        reply = {'status':False, 'log':''}
        if os.system(f"mkdir -p '{path}' 2> /dev/null"):
            reply['log'] = 'failed to create directory. please review your permissions'
            return reply
        
        reply['status'] = True
        return reply
    
    @staticmethod
    def createShortcut(source:str, destination:str) -> dict[str,bool|str]:
        '''
        attempt to create a shortcut.

        @arg `source`: the path we want to create a shortcut to
        @arg `destination`: the path to the shortcut 

        returns the standard dict with `status` and `log`
        '''
        reply = {'status':False, 'log':''}

        if not Path.exists(source):
            reply['log'] = 'the source path does not exist'
            return reply

        if Path.exists(destination):
            reply['log'] = 'the destination path already exists'
            return reply

        if os.system(f"ln -s -T '{source}' '{destination}' 2> /dev/null"):
            reply['log'] = 'failed to create the shortcut. please confirm that all necessary paths are valid and exist'
            return reply
        
        reply['status'] = True
        return reply

    @staticmethod
    def delete(path:str) -> dict[str,bool|str]:
        '''
        attempt to delete `path`.

        if the path is a directory, it will NOT be deleted if its empty 

        returns the standard dict with `status` and `log`
        '''
        reply = {'status':False, 'log':''}

        if not Path.exists(path):
            reply['log'] = 'path does not exist'
            return reply

        if Path.isDirectory(path) and os.listdir(path):
            reply['log'] = 'can not delete a non-empty directory'
            return reply

        if Path.isFile(path):
            if os.system(f"rm '{path}' 2> /dev/null"):
                reply['log'] = 'failed to delete the file. please ensure you have the right permissions'
                return reply
        else:
            if os.system(f"rmdir '{path}' 2> /dev/null"):
                reply['log'] = 'failed to delete the directory. please ensure you have the right permissions'
                return reply
        
        reply['status'] = True
        return reply

    @staticmethod
    def copy(source:str, destination:str) -> dict[str,bool|str]:
        '''
        attempt to copy a file/directory

        @arg `source`: the path we want to copy
        @arg `destination`: the path to the new copy of the file/directory 

        returns the standard dict with `status` and `log`
        '''
        reply = {'status':False, 'log':''}

        if not Path.exists(source):
            reply['log'] = 'the source path does not exist'
            return reply

        if Path.exists(destination):
            reply['log'] = 'the destination path already exists'
            return reply

        if os.system(f"cp -rfHpu '{source}' '{destination}' 2> /dev/null"):
            reply['log'] = 'failed to copy the source. please confirm that all necessary paths are valid and exist'
            return reply
        
        reply['status'] = True
        return reply

    @staticmethod
    def listDirectory(path:str) -> dict[str,bool|str]:
        '''
        attempt to list the contents of a directory

        @arg `path`: the path to the directory we want to list

        returns the standard dict with `status` and `log` along with `contents:list`

        the returned `contents` list is a list of ABSOLUTE paths
        '''
        reply = {'status':False, 'log':'', 'contents':[]}

        if not Path.isDirectory(path):
            reply['log'] = 'the path given is not a directory'
            return reply

        path += '/*'
        contents = [os.path.abspath(f) for f in glob.glob(path)]

        reply['contents'] = contents
        reply['status'] = True
        return reply

if __name__=='__main__':
    pass