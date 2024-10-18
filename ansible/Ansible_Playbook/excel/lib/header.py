import os

def get_header():
    # ホスト名
    os.environ["INVENTORY_SERVER_NAME"] = os.environ.get("INVENTORY_SERVER_NAME", "ホスト名")
    # サーバIP
    os.environ["INVENTORY_SERVER_IP"] = os.environ.get("SERVER_IP", "サーバIP")
    # グループ
    os.environ["INVENTORY_GROUP_NAME"] = os.environ.get("INVENTORY_GROUP_NAME", "グループ")  
    # 自動化
    os.environ["INVENTORY_AUTO_GEN"] = os.environ.get("INVENTORY_AUTO_GEN", "自動化")
    
    
    # variable file name location
    # os.environ["FILE_NAME_LOCATION"] = os.environ.get("FILE_NAME_LOCATION", "4")
    # パラメータ名
    os.environ["HOSTVARS_PARAMETER"] = os.environ.get("HOSTVARS_PARAMETER", "パラメータ名")
    # デフォルト
    os.environ["HOSTVARS_DEFAULT_VALUE"] = os.environ.get("HOSTVARS_DEFAULT_VALUE", "デフォルト")
    # 設定値
    #os.environ["HOSTVARS_SETTING_VALUE"] = os.environ.get("HOSTVARS_SETTING_VALUE", "設定値")
    # 自動化
    os.environ["HOSTVARS_AUTO_GEN"] = os.environ.get("HOSTVARS_AUTO_GEN", "自動化")
    # 変数名
    os.environ["HOSTVARS_VARIABLE_NAME"] = os.environ.get("HOSTVARS_VARIABLE_NAME", "変数名")

    return os.environ
