import psycopg2 as pscpg
import yaml


def load_yml(filename):
    return yaml.load(open("./{}".format(filename)))


def db_config(db_name, filename='db_cfg.yml'):
    """
    Read server specific config from file to dict
    """
    cfg = load_yml(filename)
    return cfg[db_name]


def booking_info(filename='booking_info.yml'):
    """
    Read booking info from file to dict
    """
    info = load_yml(filename)
    return info['FLY_INFO'], info['HOTEL_INFO'], info['PRICE_INFO']


def sql_queries():
    """
    Set sql queries to perform TPC transaction
    """
    fly_info, hotel_info, price_info = booking_info()
    fly_query_str = "INSERT INTO booking (client_name, fly_number, dispatch, destination, dispatch_date) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')".format(
        fly_info['CLIENT_NAME'], fly_info['FLY_NUMBER'], fly_info['DISPATCH'], fly_info['DESTINATION'], fly_info['DISPATCH_DATE'])
    hotel_query_str = "INSERT INTO booking (client_name, hotel_name, arrival, departure) VALUES (\'{}\', \'{}\', \'{}\', \'{}\')".format(
        hotel_info['CLIENT_NAME'], hotel_info['HOTEL_NAME'], hotel_info['ARRIVAL'], hotel_info['DEPARTURE'])
    cash_query_str = "UPDATE booking SET cash_amount = cash_amount - \'{}\' WHERE client_name = \'{}\'".format(
        price_info['STANDARD_PRICE'], price_info['CLIENT_NAME'])
    return fly_query_str, hotel_query_str, cash_query_str


def dtc(fly_booking_db, hotel_booking_db, cash_booking_db):
    """
    Distributed Transaction Coordinator
    """
    # Establish connection to PostgreSQL server and databases
    try:
        fly_booking_conn = pscpg.connect(**db_config(fly_booking_db))
        hotel_booking_conn = pscpg.connect(**db_config(hotel_booking_db))
        cash_booking_conn = pscpg.connect(**db_config(cash_booking_db))
    except (RuntimeError, pscpg.DatabaseError) as err:
        print(err)
        raise
    finally:
        print('> INFO: Connection to PostgreSQL Server was successfully established...\n')

    # Begin a TPC transaction
    fly_booking_conn.tpc_begin(fly_booking_conn.xid(
        1, 'transaction ID', 'connection 1'))
    hotel_booking_conn.tpc_begin(hotel_booking_conn.xid(
        1, 'transaction ID', 'connection 2'))
    cash_booking_conn.tpc_begin(cash_booking_conn.xid(
        1, 'transaction ID', 'connection 3'))

    try:
        # Create cursor objects
        fly_booking_cur = fly_booking_conn.cursor()
        hotel_booking_cur = hotel_booking_conn.cursor()
        cash_booking_cur = cash_booking_conn.cursor()
        # Set sql queries to update booking information
        fly_booking_query, hotel_booking_query, cash_booking_query = sql_queries()
        fly_booking_cur.execute(fly_booking_query)
        hotel_booking_cur.execute(hotel_booking_query)
        cash_booking_cur.execute(cash_booking_query)
        # Performs a first phase of TPC transaction after tpc_begin was called
        fly_booking_conn.tpc_prepare()
        hotel_booking_conn.tpc_prepare()
        cash_booking_conn.tpc_prepare()
    except pscpg.DatabaseError as err:
        print('> ERROR: {}'.format(err))
        print('> INFO: Transaction rollback')
        # Rolls back a TPC transaction
        fly_booking_conn.tpc_rollback()
        hotel_booking_conn.tpc_rollback()
        cash_booking_conn.tpc_rollback()
    else:
        print('> INFO: TPC transaction was successfully commited.\n')
        # Perform single phase commit
        fly_booking_conn.tpc_commit()
        hotel_booking_conn.tpc_commit()
        cash_booking_conn.tpc_commit()

    # Close all connections
    fly_booking_conn.close()
    hotel_booking_conn.close()
    cash_booking_conn.close()


def main():
    dtc('fly_booking', 'hotel_booking', 'cash')


if __name__ == "__main__":
    main()
