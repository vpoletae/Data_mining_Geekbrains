from datetime import datetime

similarity_threshold = int() # define

def check_doc_type(eoa_doc_type):
    if eoa_doc_type:
        return eoa_doc_type.capitalize()
    else:
        return 'Couldn\'t define doc type'

def check_date(eoa_date, the_closest_date):
    file_date = datetime.strftime(the_closest_date, '%d.%m.%Y')
    return (eoa_date, file_date)

def check_pids(eoa_pids, did_party_pids_dict):
    in_common_list = list(set(eoa_pids) & set(did_party_pids_dict))
    similarity_ratio = str(round(len(in_common_list)/len(did_party_pids_dict), 2)*100) + '%'
    return similarity_ratio

# def give_recommendation():
#     pass
