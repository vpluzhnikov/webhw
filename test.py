from bupl.price_calcs import calculate_req_line

k = {'db_type': '---', 'cluster_type': 'vcs', 'servername': '-', 'cpu_count': '4', 'item_count': '2', 'platform_type': 'power', 'backup_type': 'yes', 'san_count': '0', 'lan_segment': 'alpha', 'ram_count': '32', 'nas_count': '0', 'ostype': 'aix', 'itemstatus': 'prom', 'itemtype2': 'new', 'hdd_count': '300', 'itemtype1': 'db'}

print calculate_req_line(k)
