from src.lib import optimizate_table, delete_old_data
import os
from datetime import datetime

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

namespace="coroot-clickhouse"
namedb="coroot-clickhouse"
db_base="default"
count_days_delete=os.getenv("OLD_COUNT_DAYS", "3")

def main():
    print(f'{formatted_time} delete old data for last {count_days_delete} days')
    delete_old_data(namedb, namespace, "otel_traces", "Timestamp", count_days_delete)
    delete_old_data(namedb, namespace, "otel_traces_trace_id_ts", "Start", count_days_delete)
    print(f"{formatted_time} Оптимизация в БД:{db_base} в таблице: otel_traces запущена")
    optimizate_table(namedb, namespace, db_base, "otel_traces")
    print(f"{formatted_time} Оптимизация в БД:{db_base} в таблице: otel_traces_trace_id_ts запущена")
    optimizate_table(namedb, namespace, db_base, "otel_traces_trace_id_ts")
    print(f"{formatted_time} Оптимизация в БД:{db_base} в таблице: trace_log запущена")
    optimizate_table(namedb, namespace, db_base, "trace_log")
    print(f"{formatted_time} Оптимизация в БД:{db_base} в таблице: otel_logs запущена")
    optimizate_table(namedb, namespace, db_base, "otel_logs")

if __name__ == "__main__":
    main()