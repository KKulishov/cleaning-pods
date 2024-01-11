import clickhouse_connect
from os import getenv

db_admin_password = getenv("ROOT_PASSWORD")

def db_connect(namedb, namespace):
    """
    Подключение к БД clickhouse
    """
    host_db = namedb + "." + namespace
    client = clickhouse_connect.get_client(host=host_db,
                                       user='default',
                                       password=db_admin_password,
                                       port=8123,
                                       database='default',
                                       connect_timeout=15)
    return client

def optimizate_table(namedb, namespace, db_name, name_table):
    if  name_table == "trace_log":
        with db_connect(namedb, namespace) as client: 
            tables = client.command('SHOW TABLES')
            table_exists = any(table[0] == name_table for table in tables)
            if table_exists:
                # Действия, если таблица существует
                print(f"Таблица {name_table} существует. Выполняем optimization.")
                query = 'OPTIMIZE TABLE ' + name_table + ' FINAL'
                with db_connect(namedb, namespace) as client: 
                    client.command(query)
                    print(f"Оптимизация в БД:{namedb} в таблице: {name_table} запущена")
            else:
                 print(f"Таблица {name_table} не существует. Оптимизация пропускается.")    
    else:
        query = 'OPTIMIZE TABLE ' +  db_name + '.' + name_table + ' FINAL'
        with db_connect(namedb, namespace) as client: 
            #client.query(query, parameters=parameters)
            client.command(query)
            print(f"Оптимизация в БД:{namedb} в таблице: {name_table} запущена")

def delete_old_data (namedb, namespace, table, params,  count_days):
    #parameters = {'table_db': table, 'parameters': params, 'count': count_days}
    #query = 'DELETE FROM %(table_db)s WHERE %(parameters)s < now() - toIntervalDay(%(count)s)'
    with db_connect(namedb, namespace) as client: 
        #client.query(query, parameters=parameters)
        query_1 = 'DELETE FROM ' + table + ' WHERE ' + params + ' < now() - toIntervalDay(' + count_days + ')'
        client.command(query_1)
        print(f"Удаление старых данных в БД:{namedb} в таблице: {table} старше {count_days} дней выполнена")
