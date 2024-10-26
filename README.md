<div id="top"></div>
## 使用技術一覧　<br />
<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- インフラ一覧 -->
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
</p>

<!-- プロジェクトについて -->
## プロジェクトについて

環境構築パラメータシート（Excelファイル形）からデータを読み取り、適切に処理してホスト変数のYAMLファイルを作成　<br />　<br />
サンプルexcelファイルとホスト変数はApache導入に関するパラメータシートを例として作成されています。　<br />
　<br />
## 環境
<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | python3.9     |
| Docker                | 25.0.3      |
| Ansible　　　　　　　　| 2.15     |

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->
ansible-excel-tool　<br />
|   docker-compose.yml　<br />
|   README.md　<br />
|　<br />
+---ansible　<br />
|   |   Dockerfile　<br />
|   |　<br />
|   \---Ansible_Playbook　<br />
|       |   ansible.cfg　<br />
|       |   httpd_install_inventory.txt　<br />
|       |   httpd_install_playbook.yml　<br />
|       |　<br />
|       +---excel　<br />
|       |   |   httpd_parameter_sheet.xlsx　<br />
|       |   |   inventory.ini　<br />
|       |   |   main.py　<br />
|       |   |　<br />
|       |   \---lib　<br />
|       |       |   common.py　<br />
|       |       |   header.py　<br />
|       |　<br />
|       +---host_vars　<br />
|       |       app01.yml　<br />
|       |       node01.yml　<br />
|       |       web01.yml　<br />
|       |       web02.yml　<br />
|       |　<br />
|       \---roles　<br />
|           \---httpd_install_playbook　<br />
|               +---handlers　<br />
|               |       main.yml　<br />
|               |　<br />
|               +---tasks　<br />
|               |       install_httpd.yml　<br />
|               |       main.yml　<br />
|               |       pre_task.yml　<br />
|               |　<br />
|               \---templates　<br />
\---node　<br />
        Dockerfile　<br />
　<br />
<!-- コンテナの作成方法 -->

## サンプル環境起動し、生成されたhost_varsを試してみる

ansibleコンテナとnodeコンテナ作成と起動は以下の通りです。　<br />
docker-compose build --no-cache　<br />
docker-compose up -d　<br />
　<br />
起動されたansibleコンテナとnodeコンテナのIPをメモする。　<br />
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ansible　<br />
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node01　<br />
　<br />
起動されたansibleコンテナにログインする。　<br />
docker exec -it ansible /bin/bash　<br />
　<br />
inventoryファイル編集　<br />
nano httpd_install_inventory.txt　<br />
[node]グループにあるIPをメモしたnodeコンテナのIPに更新してください。　<br />
　<br />
[node]グループあるIPにpingをテストする。　<br />
ansible node -m ping -i httpd_install_inventory.txt　<br />
　<br />
ansibleプレイブックを実行　<br />
ansible-playbook -i httpd_install_inventory.txt httpd_install_playbook.yml　<br />
　<br />
開発削除　<br />
docker-compose down　<br />
docker volume remove ansible-excel-tool_Ansible_Playbook　<br />
docker images　<br />
docker image rm ansible-excel-tool-ansible　<br />
docker image rm ansible-excel-tool-node01　<br />
　<br />
## パラメータシート（httpd_parameter_sheet.xlsx）修正する方法
4パターンを例として作成しています。　<br />
パターン１：同じプロパティであるオブジェクトリスト　<br />
例：RHELのOSユーザー一覧　<br /> 　
| パラメータ名                 | 値                                      | 変数名                       |
| ---------------------- | ----------------------------------------- | ---------------------------------- |
| ユーザ名１    | tomcat9 | lst-os_users-username                               |
| ユーザID         | 10010   | lst-os_users-userid                          |
| グループ             | tomcat9         | lst-os_users-groupname                             |
| グループID         | 10009      | lst-os_users-groupid                             |
| パスワード             | tomcat9         | lst-os_users-password                                 |
| ホームディレクトリ             | /home/tomcat9       | lst-os_users-homedir                               |
| シェル             | /sbin/nologin                | lst-os_users-shell                          |

生成されるhost_vars変数、以下の通りでる。　<br />
os_users:　<br />
- username: apache　<br />
  userid: 10010　<br />
  groupname: apache　<br />
  groupid: 10010　<br />
  password: apache　<br />
  homedir: /home/apache　<br />
  shell: /sbin/nologin　<br />
host_vars変数を利用する方法　<br />
- name: Create user　<br />
  user:　<br />
    name: "{{ item.username }}"　<br />
    uid: "{{ item.userid }}"　<br />
    group: "{{ item.groupname }}"　<br />
    state: present　<br />
  loop: "{{ os_users }}"　<br />

パターン２：辞書のリスト　<br />
例：RHELのカーネルパラメータ　<br />
| パラメータ名                 | 値                                      | 変数名                       |
| ---------------------- | ----------------------------------------- | ---------------------------------- |
| net.ipv4.ip_local_port_range    | 32768 64999 | lst_dic-os_kernel                               |
| net.ipv4.tcp_keepalive_intvl         | 未定義   | lst_dic-os_kernel                         |
| net.ipv4.tcp_keepalive_probes             | 未定義         | lst_dic-os_kernel                             |
| net.ipv4.tcp_keepalive_time         | 未定義      | lst_dic-os_kernel                             |
| kernel.hung_task_warnings             | 10000000         | lst_dic-os_kernel                                 |
| net.ipv4.tcp_tw_recycle             | 0       | lst_dic-os_kernel                               |
| net.core.somaxconn             | 511                | lst_dic-os_kernel                          |

生成されるhost_vars変数、以下の通りでる。para_listは辞書のリストで、各辞書にはkeyとvalueのペアが含まれています。　<br />
lst_dic:　<br />
- name: os_kernel　<br />
  para_list:　<br />
  - key: net.ipv4.ip_local_port_range　<br />
    value: 32768 64999　<br />
  - key: kernel.hung_task_warnings　<br />
    value: 10000000　<br />
  - key: net.ipv4.tcp_tw_recycle　<br />
    value: 0　<br />
  - key: net.core.somaxconn　<br />
    value: 511　<br />

host_vars変数を利用する方法　<br />
- name: debug list kernel parameters　<br />
  debug: 　<br />
    msg="{{ item.key }} = {{ item.value }}"　<br />
  with_items: "{{ lst_dic | selectattr('name', 'equalto', 'os_kernel') | map(attribute='para_list') | flatten }}"　<br />

パターン３：辞書のリスト、各辞書には、nameというキーと、para_listというキーがあります。para_listは文字列のリストです　<br />
例：httpd.confの<Directory />タグ設定　<br />


| First Header  | Second Header | Second Header |
| ------------- | ------------- | ------------- |
| <Directory / >  |    | lst_lst-httpd_conf_b-name  |
| AllowOverride  | Content Cell  | Content Cell  |
| Require  | Content Cell  | Content Cell  |
| Options  | Content Cell  | Content Cell  |

生成されるhost_vars変数、以下の通りでる。　<br />
lst_lst_httpd_conf_b:　<br />
- name: <Directory />　<br />
  para_list:　<br />
  - AllowOverride None　<br />
  - Require all denied　<br />
  - Options FollowSymLinks　<br />
  　<br />
host_vars変数を利用する方法　<br />
- name: debug lst_lst_httpd_conf_b　<br />
  debug: 　<br />
    msg:　<br />
    - "{{ item.0.name }}"　<br />
    - "{{ item.1 }}"　<br />
  loop: "{{ lst_lst_httpd_conf_b|subelements('para_list') }}"　<br />
  loop_control:　<br />
    label: "{{ item.0.name }}"　<br />
　<br />
パターン４：パターン３と同じような形で、パラメータ名が空白である　<br />
　<br />
## inventoryファイル生成
0.hostsシートの「自動化」例に〇が付いていれば、そのホストがinventoryファイルにいれされます。　<br />
新規ホストをhostsシートに追加した後、設定シート（例は2.apacheシート）にも該当するホストの列を追加してください。　<br />

## Discussion
何ご質問がございましたら、<a href="devopsroles.com">devopsroles.com</a>にてコメントください。　<br />

<p align="right">(<a href="#top">トップへ</a>)</p>
