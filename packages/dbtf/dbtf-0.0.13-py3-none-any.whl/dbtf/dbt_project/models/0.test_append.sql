SELECT * FROM {{ref("test_table_1")}}
UNION
SELECT * FROM {{ref("test_table_2")}}
