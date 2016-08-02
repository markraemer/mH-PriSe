SELECT group_concat(COLUMN_NAME, ' = None' SEPARATOR '\n') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'mhealth_apps' AND TABLE_NAME = 'app_attsuf';
SELECT group_concat('if self.',COLUMN_NAME,' is not None:\n','\t data.append(self.',COLUMN_NAME,')\n\t sql.append("',COLUMN_NAME,'=\%s\")\n' SEPARATOR ' ') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'mhealth_apps' AND TABLE_NAME = 'code_analysiscode_analysis';
SELECT COLUMN_NAME FROM information_schema.columns where table_schema = 'mhealth_apps' and table_name = 'apps';
select ts.name, ts.order, test_case, short_desc, long_desc, rating from experiment_test_steps ts where name = 'av1_data_trans';

SELECT group_concat("'", table_name, "'") FROM information_schema.tables where table_schema = 'mhealth_apps';