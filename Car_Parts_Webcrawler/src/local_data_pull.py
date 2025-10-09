import os


def get_top_level_directories() -> dict:
    """Returns dictionary of all top level directories in module.
    
    Args: None
    
    Returns: dictionary of all top level modules.
            Keys: 
                bin: bin path,
                geckodriver: geckodriver path
                src: src path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    child_dir_list = os.listdir(parent_dir)

    top_level_directories = {}
    top_level_directories["parent_directory"] = parent_dir
    
    for top_level_dir in child_dir_list:
        dir_path_test = os.path.join(parent_dir, top_level_dir)
        if os.path.isdir(dir_path_test):
            top_level_directories[top_level_dir] = dir_path_test
    
    return top_level_directories

def parse_query_display(table_name: str) -> str:
    """Parses out query display information for easier readability for end user
    
    Args: Table_name: csv file name without the path or extension information
          Table name format: YYYY-MM-DD_car-year_car-make_car-model_car-part

    Returns: Reformatted name
             Display format: Car-Part for Car-Year Car-Make Car-Model """
    
    table_name_list = table_name.split("_")
    table_string = f"""{table_name_list[-1]} for {table_name_list[1]} {table_name_list[2]} {table_name_list[3]}"""
    return table_string

def package_records_keeping() -> dict:
    """Function to package the files and their file paths for 
    user_interactions.user_input_matches
    
    Args: None
    
    Returns: dictionary of the tables and their file paths"""

    records_keeping_dir = get_top_level_directories().get("records_keeping")
    file_list = [file for file in os.listdir(records_keeping_dir) if os.path.isfile(file)]
    file_path_dict = dict()

    for file_info in file_list:
        file_name = os.path.split(file_info)
        file_wo_ext = os.path.splitext(file_name)
        display_name = parse_query_display(file_wo_ext)
        file_path_dict[display_name] = file_info
    
    return file_path_dict
        