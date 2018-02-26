import os

def get_db_way(name):
    return os.path.join(get_warehouse_dir(), name)

def get_warehouse_dir():
    return os.path.join(get_main_dir(), "warehouse")


def get_main_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))