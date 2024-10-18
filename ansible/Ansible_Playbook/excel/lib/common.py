#lst_dic:
#  - name : "OS_KERNEL"
#    para_list :
#      - key : "net.ipv4.ip_local_port_range"
#        value : "32768 64999"
def check_key_in_lst_dic_para_list(lst_dic, key_to_check):
    for dic in lst_dic:
        if 'para_list' in dic:
            for para in dic:
                if 'key' in para and para["key"] == key_to_check:
                    return True
    return False

def check_item_in_lst_lst_para_list(lst_lst, desired_name, item_to_check):
    for item in lst_lst:
        if item["name"] == desired_name and item_to_check in item["para_list"]:
            return True
    return False

def check_name_in_lst(lst_dic, key_to_check):
    found = False
    for item in lst_dic:
        if "name" in item:
            if item["name"] == key_to_check:
                found = True
                break
    return found

def append_into_lst_dic_para_list(lst_dic, desired_name, new_para):
    for item in lst_dic:
        if item["name"] == desired_name:
            # need check new_para['key'] in item['para_list'] using check_key_in_lst_dic_para_list
            # exist then update or append new
            item["para_list"].append(new_para)
            break

def append_into_lst_lst_para_list(lst_lst, item_to_add):
    print(lst_lst)
    if 'para_list' in lst_lst:
        if item_to_add not in lst_lst["para_list"]:
            lst_lst["para_list"].append(item_to_add)
            return True
        else:
            return False
    else:
        lst_lst["para_list"] = [item_to_add]
        print(lst_lst)
        return True

def check_not_null_dict(my_dict):
    if my_dict and isinstance(my_dict, dict):
        return True
    else:
        return False