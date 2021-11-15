def get_developer_key():
    path = '/Users/evgenijastafurov/MY_GOOGLE_MAPS_DEV_KEY.txt'
    with open(path, 'r') as f:
        return f.readline()
