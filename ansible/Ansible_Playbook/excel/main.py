import sys
import os
import pandas as pd
from pathlib import Path
import traceback
import yaml
import math

from lib.header import get_header
from lib.common import check_name_in_lst
from lib.common import check_not_null_dict
from lib.common import append_into_lst_dic_para_list

# 現在のファイルの親ディレクトリを取得する
parent_path = Path(__file__).resolve().parent

# Excelファイルからインベントリ情報を抽出し、inventory.iniファイル生成
def inventory_build(excel_data, env, hosts):
    # envの環境変数を取り出し
    col_map = {
        "sever_name": env["INVENTORY_SERVER_NAME"],
        "sever_ip": env["INVENTORY_SERVER_IP"],
        "group_name": env["INVENTORY_GROUP_NAME"],
        "auto_gen": env["INVENTORY_AUTO_GEN"]
    }
    # excel_dataデータフレームからcol_mapに含まれるキーに対応する列を抽出し、sheet_dataデータフレームに格納
    sheet_data = excel_data[[col_map[key] for key in col_map if key in col_map]]
    # sheet_dataから自動化列が"〇"である行だけを抽出し、sheet_data_ftデータフレームに格納
    sheet_data_ft = sheet_data.query('自動化 == "〇"')
    
    # 空の辞書作成
    inventory = {}
    # sheet_data_ftの各行をループ
    for index, row in sheet_data_ft.iterrows():
        # sheet_data_ftの各行のgroup（グループ名）、hostname（ホスト名）、ip（サーバIP）を取得
        group = row['グループ']
        hostname = row['ホスト名']
        ip = row['サーバIP']
        # inventory辞書に存在しないgroupをinventoryの新しいリストとして作成し
        if group not in inventory:
            inventory[group] = []
        # inventoryの新しいリストに該当するhostnameとipを追加する
        inventory[group].append(f"{hostname} ansible_host={ip}")
        
        # hosts辞書にホスト名を追加する
        hosts[hostname] = hostname

    # parent_pathにinventory.iniというファイルを作成
    with open(parent_path.joinpath('inventory.ini'), 'w', encoding="utf-8") as f:
        # 各グループの名前をヘッダとして書き込み、そのグループに所属するホスト情報を続けて書き込む
        for group, lines in inventory.items():
            f.write(f"[{group}]\n")
            for line in lines:
                f.write(f"{line}\n")
            f.write("\n")
#end inventory_build関数

# Excel data frame
def hostvars_build(sheet_data_ft, env, hosts):
    # yamlデータを格納するの為空辞書
    yaml_data = {}
    # 一時yamlデータ格納
    tmp = {}
    # インプットのhostsに含まれる各ホストをループ
    # ホストに対して、yaml_data、tmp辞書成
    for host in hosts:
        yaml_data[host] = {}
        tmp[host] = {}
    # 空のリスト作成、後でサブカテゴリキーを格納する
    sub_category_keys = []
    
    # sheet_data_ftの各行をループし、行のデータを分割してカテゴリ情報を取得
    for index, row in sheet_data_ft.iterrows():
        next_row_category = ""
        # 次の行のデータ
        if index < len(sheet_data_ft) - 1:
            next_row = sheet_data_ft.iloc[index + 1]
            next_row_category = next_row['変数名'].split('-')[0]
            # lst_lstの場合の処理
            next_row_category_lv2 = next_row['変数名'].split('-')[2] if next_row_category == "lst_lst" else ""
        
        # 変数名を分割
        var_name_parts = row['変数名'].split('-')
        # lst or lst_dic or lst_lst
        category, category_lv1 = var_name_parts[0], var_name_parts[1]

        # 現在の行がlst-xxx-yyyの形式
        if category == 'lst':
            # YAMLファイルのルートキーをチェック
            if category_lv1 not in sub_category_keys:
                sub_category_keys.append(category_lv1)
                # 一時データの初期化
                for host in hosts:
                    # xxxをyaml_data[host]のリストとして作成
                    yaml_data[host] = yaml_data[host] | { category_lv1 : [] }
                    # yaml_data[host][category_lv1]リストのエレメントを初期化
                    tmp[host] = {}
            
            # lst-xxx-yyyのyyyエレメントを取る
            category_lv2 = var_name_parts[2]
            for host in hosts:
                # check item yyy in yaml_data[host][category_lv1] list
                if category_lv2 not in tmp[host]:
                    if (row[host] != '未定義'):
                        tmp[host][category_lv2] = row[host]
                else:
                    # item yyy exist in yaml_data[host][category_lv1] list
                    # add tmp[host] into yaml_data[host][category_lv1]
                    yaml_data[host][category_lv1].append(tmp[host])
                    # Refresh tmp[host] to store the new data
                    tmp[host] = {}
                    # store item yyy into tmp[host]
                    if (row[host] != '未定義'):
                        tmp[host][category_lv2] = row[host]

            # 次の行のカテゴリをチェック
            if next_row_category != 'lst':
                for host in hosts:
                    if check_not_null_dict(tmp[host]):
                        yaml_data[host][category_lv1].append(tmp[host])
                        tmp[host] = {}
        # End of row is lst-xxx-yyy


        # 現在の行がlst_dic-xxxの形式
        if category == 'lst_dic':
            for host in hosts:
                # check root key of yaml file
                if category not in yaml_data[host]:
                    # init new key of yaml is lst_dic
                    yaml_data[host] = yaml_data[host] | { 'lst_dic' : [] }
                    # init element of yaml_data[host][category] list
                    tmp[host] = {}

                # if category_lv1(xxx) not exist in tmp[host]
                if check_name_in_lst(yaml_data[host]['lst_dic'], category_lv1) == False:
                    if row[host] != '未定義':
                        tmp[host] = {
                            'name': category_lv1,
                            'para_list': []
                        }
                        tmp[host]['para_list'].append({
                            'key': row['パラメータ名'],
                            'value': row[host]
                        })
                        yaml_data[host]['lst_dic'].append(tmp[host])
                        tmp[host] = {}
                else:
                    if row[host] != '未定義':
                        append_into_lst_dic_para_list( yaml_data[host]['lst_dic'], category_lv1,
                        {
                            'key': row['パラメータ名'],
                            'value': row[host]
                        })
        # End of lst_dic

        # current row is lst_lst-xxx-name or lst_lst-xxx-para_list
        if category == 'lst_lst':
            #lst_lst_xxx
            lst_lst_key = f"{category}_{category_lv1}"
            # get third element of lst_lst-xxx-name or lst_lst-xxx-para_list row
            category_lv2 = var_name_parts[2]

            for host in hosts:
                # check root lst_lst_xxx key of yaml file
                if lst_lst_key not in yaml_data[host]:
                    # init new key of yaml is lst_lst_xxx
                    yaml_data[host] = yaml_data[host] | { lst_lst_key : [] }
                    # init element of yaml_data[host]['lst_lst_xxx'] list
                    tmp[host] = {}

                # if category_lv2(lst_lst-xxx-name) not exist in yaml and category_lv2 not blank
                if category_lv2 == 'name' and row['パラメータ名'] != '':
                    if check_name_in_lst(yaml_data[host][lst_lst_key], row['パラメータ名'] ) == False:
                        tmp[host] = {
                            'name': row['パラメータ名'],
                            'para_list': []
                        }
                    else:
                        print(f"Error Key:name:{row['パラメータ名']},var:{row['変数名']} was duplicated.\n")
                        exit
                # lst_lst-xxx-para_list row
                if category_lv2 == 'para_list' and row[host] != '未定義':
                    # if type _a(ex:lst_lst-httpd_conf_a-para_list)
                    if category_lv1.endswith('_a'):
                        if "para_list" in tmp[host]:
                            if row[host] not in tmp[host]["para_list"]:
                                tmp[host]["para_list"].append(row[host])
                            else:
                                print(f"Error Key:name:{tmp[host]['name']},var:{row['変数名']}, value:{row[host]} was duplicated.\n")
                                exit
                    # if type _b(ex:lst_lst-httpd_conf_b-para_list)
                    elif category_lv1.endswith('_b'):
                        # check special value : row[host] = None
                        if isinstance(row[host], float) and  math.isnan(row[host]):
                            tmp_para_value = f"{row['パラメータ名']} None"
                        else:
                            tmp_para_value = f"{row['パラメータ名']} {str(row[host])}" 
                        if "para_list" in tmp[host]:
                            if tmp_para_value not in tmp[host]["para_list"]:
                                tmp[host]["para_list"].append(tmp_para_value)
                        else:
                            #print(f"Error Key:name:{tmp[host]['name']},var:{row['変数名']}, value:{tmp_para_value} was duplicated.\n")
                            exit
                # lst_lst-xxx-para_list row, and next_row lst_lst-xxx-name
                # then insert current data into lst_lst_key
                if category_lv2 == 'para_list' and next_row_category_lv2 == 'name':
                    if "para_list" in tmp[host]:
                        if len(tmp[host]["para_list"]) != 0:
                            yaml_data[host][lst_lst_key].append(tmp[host])
                            tmp[host] = {}
            
            # check next_row_category and add data into the lst_lst_key
            if next_row_category != 'lst_lst':
                for host in hosts:
                    if 'para_list' in tmp[host]:
                        if len(tmp[host]["para_list"]) != 0:
                            yaml_data[host][lst_lst_key].append(tmp[host])
                            tmp[host] = {}
                    # check element of yaml_data[host][lst_lst_key], if member = 0 then remove lst_lst_key
                    # print(yaml_data[host])
                    if len(yaml_data[host][lst_lst_key]) == 0:
                        yaml_data[host].pop(lst_lst_key, None)
        # End of lst_lst
        
    # End of For


    # YAMLファイルの書き込み
    for host in hosts:
        #print(yaml_data[host])
        yaml_file_path = os.path.join(parent_path, '..', 'host_vars', f'{host}.yml')
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(yaml_data[host], yaml_file, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main(excel_file_path):
    try:
        # get_header関数を呼び出して環境変数を取得
        env = get_header()
        # 空の辞書
        hosts = {}
        # 空のDataFrameを初期化
        sheet_data_ft = pd.DataFrame()
        # Excelファイルを読み込み、worksheet_dataに格納
        worksheet_data = pd.ExcelFile(parent_path.joinpath(excel_file_path))

        # シートのループ処理
        for sheetname in worksheet_data.sheet_names:
            print(f"=========={sheetname}==========")
            # Excelファイル内の各シート名をループで処理
            
            # シート名が'0.hosts'の場合、そのシートのデータを読み込み、inventory_build関数で処理
            if sheetname == '0.hosts':
                # Read sheet data into a dictionary of DataFrames
                excel_data = worksheet_data.parse(sheet_name=sheetname,header=4)
                inventory_build(excel_data, env, hosts)
            # シート名が'setting'、'0.hosts'、'表紙'以外の場合、そのシートのデータを読み込み、
            # 特定のカラムを抽出してフィルタリング
            if sheetname != 'setting' and sheetname != '0.hosts' and sheetname != '表紙':
                # Read sheet data into a dictionary of DataFrames
                excel_data = worksheet_data.parse(sheet_name=sheetname,header=5)

                # header build
                col_map = {}
                col_map = {
                    "default_value": env["HOSTVARS_DEFAULT_VALUE"],
                    "parameter": env["HOSTVARS_PARAMETER"]
                }
                col_map = col_map | hosts
                col_map["auto_gen"] = env["HOSTVARS_AUTO_GEN"]
                col_map["variable_name"] = env["HOSTVARS_VARIABLE_NAME"]
                
                # フィルタリングされたデータをsheet_data_ftに結合
                # filter data from excel
                sheet_data = excel_data[[col_map[key] for key in col_map if key in col_map]]

                # join data
                sheet_data_ft = pd.concat([sheet_data_ft, sheet_data.query('自動化 == "〇"')], ignore_index=True)

        # End of Iterate through each worksheet

        # sheet_data_ftを使用してhostvars.ymlファイルを生成
        hostvars_build(sheet_data_ft, env, hosts)
        
    # 例外が発生した場合
    except Exception:
        print(f"Error:")
        traceback.print_exc()

if __name__ == "__main__":
    main(sys.argv[1])
