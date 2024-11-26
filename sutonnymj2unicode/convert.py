import encodings
import itertools
from bijoy2unicode import converter
import csv
import codecs
import os

test = converter.Unicode()

# Define the path to the main folder containing subfolders and script files
main_folder = 'D:\m_project\sutonnymj2unicode\Tangail District'

#access subfolders list
subfolders = os.listdir(main_folder)


# Iterate over the subfolders and create CSV files in each one
for subfolder in subfolders:
    microplan_centre_file = None
    data_file = None

    # Define the path to the subfolder
    subfolder_path = os.path.join(main_folder, subfolder)

    file_list = os.listdir(subfolder_path)

    for files in file_list:

        # Define the path to the subfolder
        file = os.path.join ( subfolder_path ,files )

        if file.endswith ( '.csv' ):
            csv_file_path = os.path.join (  file )

            # Determine if it's the first or second input CSV file
            if file.endswith ( '_2023.csv' ):
                microplan_centre_file = csv_file_path
            else:
                data_file = csv_file_path

    print(f"microplan_centre_file = {microplan_centre_file}")
    print(f"data_file = {data_file}")


    #variables
    current_union = None
    count = 0
    output_data_list = []
    ward_centre_count = []
    unicode_union_centre = []
    union_list = []
    union_wise_centre_list = []
    empty_list = ['']

    # Read the input CSV file and write to the output CSV file
    with open(microplan_centre_file, 'r', newline='' ) as input_file, open(data_file, 'r', newline='', encoding="utf-8") as alter_file:

        reader = csv.reader(input_file)
        next ( reader )  # Skip the header row

        alter = csv.reader ( alter_file )
        next ( alter )  # Skip the header row

        # convert in unicode and build a dictionary
        for row in reader:

            bijoy_text_union = row[1]
            bijoy_text_centre = row[0]

            # Convert Bijoy to Unicode
            unicode_centre = test.convertBijoyToUnicode ( bijoy_text_centre )

            unicode_union = test.convertBijoyToUnicode ( bijoy_text_union )

            if (unicode_union not in union_list) and (unicode_union not in empty_list):
                union_list.append ( unicode_union )

                dict = {'union' : unicode_union}
                dict['centre'] = [unicode_centre]  # Initialize as a list with one element
                union_wise_centre_list.append(unicode_centre)

            else:
                if (unicode_centre not in union_wise_centre_list) and (unicode_centre not in empty_list):
                    if dict['union'] == unicode_union:
                        dict['centre'].append ( unicode_centre )  # Append to the existing list
                        union_wise_centre_list.append ( unicode_centre )

            if dict['union'] != current_union:
                current_union = dict['union']
                unicode_union_centre.append ( dict )

        current_ward = None
        ward_count = 0
        union_check = None
        union_check_list = []
        centre_count = 0
        current_centre = None

        for a_row in alter:
            for _ in unicode_union_centre:
                if str ( a_row[22] ) == _["union"]:
                    if (str ( a_row[22]) != union_check) and (str (a_row[22]) not in union_check_list):
                        union_check = str ( a_row[22])
                        union_check_list.append(union_check)
                        centre_count = 0

                    if int ( a_row[28] ) != current_ward:
                        current_ward = int ( a_row[28] )
                        ward_count = 0  # Reset ward_count for the new ward

                    if (
                        current_ward == 1 or current_ward == 2 or current_ward == 4 or current_ward == 5 or current_ward == 7 or current_ward == 8
                        ):
                        if ward_count >= 3:
                            continue
                        a_row[33] = _["centre"][centre_count]
                        current_centre = a_row[33]
                        ward_count += 1
                        dict1 = {f'{_["union"]} {a_row[28]}': ward_count}
                        centre_count+=1
                    else:
                        if ward_count >= 2:
                            continue
                        a_row[33] = _["centre"][centre_count]
                        current_centre = a_row[33]
                        ward_count += 1
                        dict1 = {f'{_["union"]} {a_row[28]}': ward_count}
                        centre_count += 1

            if a_row[33] == current_centre:
                output_data_list.append ( a_row )
    with open ( f'{subfolder_path}/{subfolder}_updated.csv' , 'w' , encoding='utf-8' , newline='' ) as output_file:
        writer = csv.writer ( output_file )

        writer.writerow (
            ['Code' , 'Country' , 'bn' , 'type' , 'Code' , 'Division' , 'bn' , 'type' , 'Code' , 'District' ,
             'bn' , 'type' , 'Code' , 'Upazilla' , 'bn' , 'type' , 'Code' , 'Paurasava' , 'bn' , 'type' ,
             'Code' , 'Union' , 'bn' , 'type' , 'Code' , 'Old Ward' , 'bn' , 'type' , 'Code' , 'Ward' , 'bn' ,
             'type' , 'Code' , 'Block' , 'bn' , 'type'] )

        for _ in output_data_list:
            writer.writerow ( _ )

    print ( 'Processing complete.' )