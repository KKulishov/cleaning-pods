## Help to clickhouse command


показать размер таблиц.
```
SELECT
    database,
    table,
    formatReadableSize(sum(data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(data_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_rate,
    sum(rows) AS rows,
    count() AS part_count
FROM system.parts
WHERE (active = 1) AND (database LIKE '%') AND (table LIKE '%')
GROUP BY
    database,
    table
ORDER BY size DESC;
```

посмотреть тек процессы 
```
SELECT * FROM system.processes\G
```

Оптимизация талицы для очистки пустых значений 
```
OPTIMIZE TABLE default.trace_log FINAL;
```

Описание таблицы
```
 DESCRIBE TABLE default.otel_traces;
```

Удалить все содержимое в табл.
```
TRUNCATE TABLE otel_traces_trace_id_ts;
TRUNCATE TABLE default.otel_traces;
```

вывести данные за посодение 3 дня
```
SELECT * FROM default.otel_traces WHERE toDate(Timestamp) < today() - 3;
SELECT * FROM default.otel_traces_trace_id_ts WHERE toDate(Start) < today() - 3;
```

удалить данные в табл. которые старше 4 дней по метки  Timestamp
```
DELETE FROM otel_traces WHERE Timestamp < now() - toIntervalDay(4);
DELETE FROM otel_traces_trace_id_ts WHERE Start < now() - toIntervalDay(3);
```

удалить таблицу исключая буффер 
```
DROP TABLE mydb.mytable no delay
```

