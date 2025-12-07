def get_files_info(working_directory , directory=None):
    import os
    
    def get_directory_size(path):
        """Recursively calculate the total size of a directory"""
        total_size = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file(follow_symlinks=False):
                    total_size += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total_size += get_directory_size(entry.path)
        except PermissionError:
            pass
        return total_size
    
    final_response = ""

    abs_working_directory = os.path.abspath(working_directory)
    
    if directory is None:
        abs_directory = abs_working_directory
    else:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    
    if not abs_directory.startswith(abs_working_directory):
        return f"Error: The directory {abs_directory} is outside the working directory {abs_working_directory}."
    
    contents = os.listdir(abs_directory)

    for item in contents:
        content_path = os.path.join(abs_directory, item)
        is_dir = os.path.isdir(content_path)
        
        if is_dir:
            size = get_directory_size(content_path)
        else:
            size = os.path.getsize(content_path)
            
        final_response += f"Name: {item}, Is Directory: {is_dir}, Size: {size} bytes\n"
    
    return final_response
