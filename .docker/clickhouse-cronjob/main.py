from src.lib import optimizate_table, delete_old_data
import os

namespace="coroot-clickhouse"
namedb="coroot-clickhouse"
db_base="default"
count_days_delete=os.getenv("OLD_COUNT_DAYS", 3)

def main():
    print(f"Оптимизация в БД:{db_base} в таблице: otel_traces запущена")
    optimizate_table(namedb, namespace, db_base, "otel_traces")
    print(f"Оптимизация в БД:{db_base} в таблице: otel_traces_trace_id_ts запущена")
    optimizate_table(namedb, namespace, db_base, "otel_traces_trace_id_ts")
    print(f"Оптимизация в БД:{db_base} в таблице: trace_log запущена")
    optimizate_table(namedb, namespace, db_base, "trace_log")
    print(f"Оптимизация в БД:{db_base} в таблице: otel_logs запущена")
    optimizate_table(namedb, namespace, db_base, "otel_logs")
    delete_old_data(namedb, namespace, "otel_traces", count_days_delete)
    delete_old_data(namedb, namespace, "otel_traces_trace_id_ts", count_days_delete)

if __name__ == "__main__":
    main()
