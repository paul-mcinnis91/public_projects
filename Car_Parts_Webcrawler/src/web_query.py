

class query_webpages():

    def __init__():
        pass

    def help_info(self):
        """Prints out helpful information for the user"""
        help_text = f"""Filter and Sort Queries available are related to these columns:
Options: 
-Sort == Sort results based upon column of choice. 
         Defaults to Ascending unless Descending is supplied as an option
-Filter == Filter results based upon column(s) of choice (boolean search allowed)
-Save == Save results as a Comma Seperated Values (.csv) file
-Quit == Quit the program
-View == View current results of query. Built into -Filter and -Sort. 
         Can view one or more column(s) by using -View <col_name1> <col_name2>. 
         If no columns provided willl print full dataframe
-Help == Prints this text so you have a reference"""
        print(help_text)
