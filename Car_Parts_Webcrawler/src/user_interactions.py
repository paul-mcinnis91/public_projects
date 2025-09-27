import sys



class User_Interface:
    def __init__(self):
        pass

    def user_input_matches(self, matches_list: list) -> int:
        """Function to have the user pick from a list of matches and returns the number they
        selected corresponding to the part"""

        if len(matches_list) == 0:
            sys.exit("No parts found, change your query and try again")
            
        print(matches_list)
        user_part_choice = input("Select your part by the number next to it. If your part is not present, type quit ").lower()

        if user_part_choice[0] == 'q':
            sys.exit("No part selected")
        
        try: 
            return int(user_part_choice)
        
        except ValueError:
            sys.exit("Invalid user input")