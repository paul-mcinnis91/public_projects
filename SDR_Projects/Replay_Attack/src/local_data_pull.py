import os


def get_top_level_directories() -> dict:
    """Returns dictionary of all top level directories in module.
    
    Args: None
    
    Returns: dictionary of all top level modules.
            Keys: 
                bin: bin path,
                record_keeping: record_keeping path
                src: src path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    child_dir_list = os.listdir(parent_dir)

    top_level_directories = {}
    top_level_directories["parent_dir"] = parent_dir
    
    for top_level_dir in child_dir_list:
        dir_path_test = os.path.join(parent_dir, top_level_dir)
        if os.path.isdir(dir_path_test):
            top_level_directories[top_level_dir] = dir_path_test
    
    return top_level_directories