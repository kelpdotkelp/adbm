import database

uri = 'mongodb://localhost:27017'


def main():
    database.connect(uri)
    database.db_name = 'testDatabase'

    database.insert_recursive('C:/Users/Noah/Desktop/july31/pos_group_1', 'data')
    database.insert_recursive('C:/Users/Noah/Desktop/july31/incident', 'incident')
    database.insert_recursive('C:/Users/Noah/Desktop/july31/calibration', 'calibration')


if __name__ == '__main__':
    main()
