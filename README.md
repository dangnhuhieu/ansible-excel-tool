<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/ansible-EE0000?style=plastic&logo=ansible&logoColor=white">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- インフラ一覧 -->
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
</p>

<!-- プロジェクトについて -->

## プロジェクトについて

環境構築パラメータシート（Excelファイル形）からデータを読み取り、適切に処理してホスト変数のYAMLファイルを作成
サンプルexcelファイルとホスト変数はApache導入に関するパラメータシートを例として作成されています。

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | python3.9     |
| Docker                | 25.0.3      |
| Ansible　　　　　　　　| 2.15     |

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->

ansible-excel-tool
|   docker-compose.yml
|   README.md
|
+---ansible
|   |   Dockerfile
|   |
|   \---Ansible_Playbook
|       |   ansible.cfg
|       |   httpd_install_inventory.txt
|       |   httpd_install_playbook.yml
|       |
|       +---excel
|       |   |   httpd_parameter_sheet.xlsx
|       |   |   inventory.ini
|       |   |   main.py
|       |   |
|       |   \---lib
|       |       |   common.py
|       |       |   header.py
|       |
|       +---host_vars
|       |       app01.yml
|       |       node01.yml
|       |       web01.yml
|       |       web02.yml
|       |
|       \---roles
|           \---httpd_install_playbook
|               +---handlers
|               |       main.yml
|               |
|               +---tasks
|               |       install_httpd.yml
|               |       main.yml
|               |       pre_task.yml
|               |
|               \---templates
\---node
        Dockerfile

<!-- コンテナの作成方法 -->

## サンプル環境起動し、生成されたhost_varsを試してみる

ansibleコンテナとnodeコンテナ作成と起動は以下の通りです。
docker-compose build --no-cache
docker-compose up -d

起動されたansibleコンテナとnodeコンテナのIPをメモする。
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ansible
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node01

起動されたansibleコンテナにログインする。
docker exec -it ansible /bin/bash

inventoryファイル編集
nano httpd_install_inventory.txt
[node]グループにあるIPをメモしたnodeコンテナのIPに更新してください。

[node]グループあるIPにpingをテストする。
ansible node -m ping -i httpd_install_inventory.txt

ansibleプレイブックを実行
ansible-playbook -i httpd_install_inventory.txt httpd_install_playbook.yml

開発削除
docker-compose down
docker volume remove ansible-excel-tool_Ansible_Playbook
docker images
docker image rm ansible-excel-tool-ansible
docker image rm ansible-excel-tool-node01

## パラメータシート（httpd_parameter_sheet.xlsx）修正する方法
4パターンを例として作成しています。
パターン１：同じプロパティであるオブジェクトリスト
例：RHELのOSユーザー一覧
| パラメータ名              | 値                | 変数名                   
| ----------------------| -----------------------------------------
| ユーザ名１		 		| tomcat9	 		| lst-os_users-username    
| ユーザID		 		| 10009	   			| lst-os_users-userid      
| グループ		 			| Mtomcat9	    	| lst-os_users-groupname   
| グループID		 		| 10009	    		| lst-os_users-groupid     
| パスワード		 		| tomcat9	     	| lst-os_users-password    
| ホームディレクトリ	 		| /home/tomcat9	    | lst-os_users-homedir     
| シェル			 		| /sbin/nologin	   	| lst-os_users-shell       

生成されるhost_vars変数、以下の通りでる。
os_users:
- username: apache
  userid: 10010
  groupname: apache
  groupid: 10010
  password: apache
  homedir: /home/apache
  shell: /sbin/nologin

host_vars変数を利用する方法
- name: Create user
  user:
    name: "{{ item.username }}"
    uid: "{{ item.userid }}"
    group: "{{ item.groupname }}"
    state: present
  loop: "{{ os_users }}"
  
 
パターン２：辞書のリスト
例：RHELのカーネルパラメータ
| パラメータ名              			| 値                | 変数名                   
| ----------------------------------| -----------------------------------------
| net.ipv4.ip_local_port_range 		| 32768 64999		| lst_dic-os_kernel  
| net.ipv4.tcp_keepalive_intvl 		| 未定義				| lst_dic-os_kernel  
| net.ipv4.tcp_keepalive_probes		| 未定義				| lst_dic-os_kernel  
| net.ipv4.tcp_keepalive_time	 	| 未定義				| lst_dic-os_kernel  
| kernel.hung_task_warnings	 		| 10000000			| lst_dic-os_kernel  
| net.ipv4.tcp_tw_recycle		 	| 0   				| lst_dic-os_kernel  
| net.core.somaxconn		 		| 511  				| lst_dic-os_kernel

生成されるhost_vars変数、以下の通りでる。para_listは辞書のリストで、各辞書にはkeyとvalueのペアが含まれています。
lst_dic:
- name: os_kernel
  para_list:
  - key: net.ipv4.ip_local_port_range
    value: 32768 64999
  - key: kernel.hung_task_warnings
    value: 10000000
  - key: net.ipv4.tcp_tw_recycle
    value: 0
  - key: net.core.somaxconn
    value: 511

host_vars変数を利用する方法
- name: debug list kernel parameters
  debug: 
    msg="{{ item.key }} = {{ item.value }}"
  with_items: "{{ lst_dic | selectattr('name', 'equalto', 'os_kernel') | map(attribute='para_list') | flatten }}"


パターン３：辞書のリスト、各辞書には、nameというキーと、para_listというキーがあります。para_listは文字列のリストです
例：httpd.confの<Directory />タグ設定
| パラメータ名              			| 値                | 変数名                   
| ----------------------------------| -----------------------------------------
| <Directory />				 		| 					| lst_lst-httpd_conf_b-name 
| AllowOverride 					| None				| lst_lst-httpd_conf_b-para_list
| Require							| all denied		| lst_lst-httpd_conf_b-para_list 
| Options	 						| FollowSymLinks	| lst_lst-httpd_conf_b-para_list 

生成されるhost_vars変数、以下の通りでる。
lst_lst_httpd_conf_b:
- name: <Directory />
  para_list:
  - AllowOverride None
  - Require all denied
  - Options FollowSymLinks
  
host_vars変数を利用する方法
- name: debug lst_lst_httpd_conf_b
  debug: 
    msg:
    - "{{ item.0.name }}"
    - "{{ item.1 }}"
  loop: "{{ lst_lst_httpd_conf_b|subelements('para_list') }}"
  loop_control:
    label: "{{ item.0.name }}"

パターン４：パターン３と同じような形で、パラメータ名が空白である

## inventoryファイル生成
0.hostsシートの「自動化」例に〇が付いていれば、そのホストがinventoryファイルにいれされます。
新規ホストをhostsシートに追加した後、設定シート（例は2.apacheシート）にも該当するホストの列を追加してください。

## Discussion
何ご質問がございましたら、<p align="right">(<a href="devopsroles.com">devopsroles.com</a>)</p>にてコメントをお入れください。

<p align="right">(<a href="#top">トップへ</a>)</p>
