def set_interface(management_ip, user, password, interface_name, ip, netmask):
    base_url = f"http://{management_ip}/restconf/api/running/interfaces/interface/{interface_name}"
    print("Trying to connect to URL:", base_url)
    auth = HTTPBasicAuth(user, password)
    headers = {
        'Accept': 'application/vnd.yang.data+json',
        'Content-Type': 'application/vnd.yang.data+json'
    }
    data = {
        # your interface config dict here
    }
    response = requests.put(base_url, auth=auth, headers=headers, data=json.dumps(data))
    # ...

