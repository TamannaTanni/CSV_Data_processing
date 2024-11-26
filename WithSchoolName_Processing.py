import csv
import os

# Define the path to the main folder containing subfolders and script files
main_folder = 'D:\\m_project\\CSV_Data_processing\\Kaliganj school'

# access subfolders list
subfolders = os.listdir ( main_folder )

# Iterate over the subfolders and create CSV files in each one
for subfolder in subfolders:
    school_file = None
    citizen_portal_file = None

    # Define the path to the subfolder
    subfolder_path = os.path.join ( main_folder , subfolder )

    file_list = os.listdir ( subfolder_path )

    for files in file_list:

        # Define the path to the subfolder
        file = os.path.join ( subfolder_path , files )

        if file.endswith ( '.csv' ):
            csv_file_path = os.path.join ( file )

            # Determine if it's the first or second input CSV file
            if file.endswith ( '_School_2023.csv' ):
                school_file = csv_file_path
            elif file.endswith( f'{subfolder}.csv'):
                citizen_portal_file = csv_file_path

    print ( f"school_file = {school_file}" )
    print ( f"citizen_portal_file = {citizen_portal_file}" )

    # variables
    current_union = None
    count = 0
    ward_school_count = []
    unicode_union_school = []
    union_list = []
    union_wise_school_list = []
    empty_list = ['']

    # Read the input CSV file and write to the output CSV file
    with open ( school_file , 'r' , newline='' , encoding="utf-8" ) as input_file , open (
            citizen_portal_file , 'r' , newline='' , encoding="utf-8" ) as alter_file:

        reader = csv.reader ( input_file )
        next ( reader )  # Skip the header row

        alter = csv.reader ( alter_file )
        next ( alter )  # Skip the header row

        # convert in unicode and build a dictionary
        for row in reader:

            unicode_school = row[0]
            unicode_union = row[1]

            if (unicode_union not in union_list) and (unicode_union not in empty_list):
                union_list.append ( unicode_union )

                dict = {'union': unicode_union}
                dict['school'] = [unicode_school]  # Initialize as a list with one element
                union_wise_school_list.append ( unicode_school )

            else:
                if (unicode_school not in union_wise_school_list) and (unicode_school not in empty_list):
                    if dict['union'] == unicode_union:
                        dict['school'].append ( unicode_school )  # Append to the existing list
                        union_wise_school_list.append ( unicode_school )

            if dict['union'] != current_union:
                current_union = dict['union']
                unicode_union_school.append ( dict )

        union_check = None
        union_check_list = []
        current_school = None
        output_data_list = []

        for a_row in alter:
            for _ in unicode_union_school:
                if str ( a_row[22] ) == _["union"]:
                    if (str ( a_row[22] ) != union_check) and (str ( a_row[22] ) not in union_check_list):
                        union_check = str ( a_row[22] )
                        union_check_list.append ( union_check )
                        school_count = 0

                        for i in _['school']:
                            # Create a new list for each iteration
                            new_row = list ( a_row )
                            new_row[24] = '99'
                            new_row[25] = 'NO OLD WARD'
                            new_row[26] = 'পুরাতন ওয়ার্ড নেই'
                            new_row[28] = '99'
                            new_row[29] = 'NO NEW WARD'
                            new_row[30] = 'নতুন ওয়ার্ড নেই'
                            new_row[31] = 'no'
                            new_row[33] = _["school"][school_count]
                            current_school = new_row[33]
                            school_count += 1
                            new_row[32] = school_count
                            new_row[34] = ''
                            new_row[35] = 'SCHOOL'
                            output_data_list.append ( new_row )

    with open ( f'{subfolder_path}/{subfolder}_school_updated.csv' , 'w' , encoding='utf-8' ,
                newline='' ) as output_file:
        writer = csv.writer ( output_file )

        writer.writerow (
            ['Code', 'Country', 'bn', 'type', 'Code', 'Division', 'bn',	'type',	'Code',	'District',	'bn', 'type', 'Code', 'Upazilla', 'bn',	'type',	'Code',	'Paurasava', 'bn', 'type', 'Code',	'Union', 'bn', 'type',	'Code',	'Old Ward',	'bn', 'type', 'Code', 'Ward', 'bn', 'type',	'Code',	'Block', 'bn',	'type'] )

        for _ in output_data_list:
            writer.writerow ( _ )

    print ( 'Processing complete.' )
