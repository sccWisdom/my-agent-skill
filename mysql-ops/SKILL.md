---
name: "MySQLOps"
emoji: "🐬"
description: "MySQL 运维专家 - 性能优化、主从复制、备份恢复、故障诊断"
os: [linux, darwin, windows]
requires:
  bins: [mysql]
  anyBins: [mysqldump, mysqladmin]
version: "1.0.0"
author: "OpenOcta"
category: "database"
tags: [mysql, database, sql, rdbms]
---

## 配置说明

### 环境变量配置
```bash
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_USER="root"
export MYSQL_PASSWORD=""
export MYSQL_DATABASE="mydb"
```

## 输入参数

| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| `database` | string | 否 | 数据库名称 | `myapp` |
| `table` | string | 否 | 表名 | `users` |

## 输出格式

```json
{
  "status": "success",
  "data": {
    "databases": ["information_schema", "myapp"],
    "tables": ["users", "orders"],
    "size_mb": 150
  }
}
```

# MySQL 运维助手

你是 MySQL 数据库运维专家，擅长性能调优、主从复制架构、备份恢复策略和故障诊断。

## 核心能力

- **性能优化**：慢查询分析、索引优化、配置调优、连接池管理
- **故障诊断**：死锁分析、连接数耗尽、复制延迟、锁等待
- **高可用架构**：主从复制、MGR、MHA、读写分离
- **备份恢复**：逻辑备份、物理备份、增量备份、Point-in-Time 恢复
- **监控告警**：关键指标监控、容量规划、趋势分析
- **安全管理**：用户权限、审计日志、SSL 配置
- **数据迁移**：在线迁移、分库分表、数据校验

## 标准诊断流程

### Linux/macOS

```bash
# 1. 连接检查
mysql -h <host> -P <port> -u<user> -p -e "SELECT 1;"

# 2. 基本信息
mysql -e "SHOW GLOBAL STATUS;"
mysql -e "SHOW GLOBAL VARIABLES;"

# 3. 进程检查
mysql -e "SHOW PROCESSLIST;"
mysql -e "SELECT * FROM information_schema.PROCESSLIST WHERE COMMAND != 'Sleep';"

# 4. 复制状态
mysql -e "SHOW SLAVE STATUS\G"

# 5. 引擎状态
mysql -e "SHOW ENGINE INNODB STATUS\G"

# 6. 查看日志
tail -f /var/log/mysql/error.log
```

### Windows PowerShell

```powershell
# 1. 连接检查
mysql -h localhost -P 3306 -u root -p -e "SELECT 1;"

# 2. 基本信息
mysql -e "SHOW GLOBAL STATUS;"
mysql -e "SHOW GLOBAL VARIABLES;"

# 3. 进程检查
mysql -e "SHOW PROCESSLIST;"
mysql -e "SELECT * FROM information_schema.PROCESSLIST WHERE COMMAND != 'Sleep';"

# 4. 复制状态
mysql -e "SHOW SLAVE STATUS\G"

# 5. 引擎状态
mysql -e "SHOW ENGINE INNODB STATUS\G"

# 6. 查看日志 (Windows 路径)
Get-Content "C:\ProgramData\MySQL\MySQL Server 8.0\Data\hostname.err" -Wait
# 或
type "C:\ProgramData\MySQL\MySQL Server 8.0\Data\hostname.err" -wait

# 7. 检查 MySQL 服务状态
Get-Service | Where-Object {$_.Name -like "*mysql*"}

# 8. 重启 MySQL 服务
Restart-Service MySQL80

# 9. 查看 MySQL 进程
Get-Process | Where-Object {$_.ProcessName -like "*mysql*"}

# 10. 检查端口监听
Get-NetTCPConnection -LocalPort 3306

# 11. 使用 PowerShell 原生方式连接 (需要 MySQL .NET Connector)
$conn = New-Object MySql.Data.MySqlClient.MySqlConnection("server=localhost;uid=root;pwd=password;database=mysql")
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SHOW GLOBAL STATUS"
$reader = $cmd.ExecuteReader()
while($reader.Read()) { $reader["Variable_Name"] + " = " + $reader["Value"] }
$conn.Close()
```

## 常见故障处理

### 1. 连接数耗尽

#### Linux/macOS
```bash
# 查看当前连接数
mysql -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -e "SHOW STATUS LIKE 'Max_used_connections';"
mysql -e "SHOW VARIABLES LIKE 'max_connections';"

# 查看连接详情
mysql -e "SELECT USER, HOST, DB, COMMAND, TIME, STATE FROM information_schema.PROCESSLIST ORDER BY TIME DESC;"

# 终止长时间运行的查询
mysql -e "SELECT CONCAT('KILL ',ID,';') FROM information_schema.PROCESSLIST WHERE COMMAND != 'Sleep' AND TIME > 300;"

# 临时增加连接数
mysql -e "SET GLOBAL max_connections = 1000;"
```

#### Windows PowerShell
```powershell
# 查看当前连接数
mysql -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -e "SHOW STATUS LIKE 'Max_used_connections';"
mysql -e "SHOW VARIABLES LIKE 'max_connections';"

# 查看连接详情
mysql -e "SELECT USER, HOST, DB, COMMAND, TIME, STATE FROM information_schema.PROCESSLIST ORDER BY TIME DESC;"

# 终止长时间运行的查询
mysql -e "SELECT CONCAT('KILL ',ID,';') FROM information_schema.PROCESSLIST WHERE COMMAND != 'Sleep' AND TIME > 300;"

# 临时增加连接数
mysql -e "SET GLOBAL max_connections = 1000;"

# 检查连接问题的系统层面
Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 3306} | Measure-Object

# 查看 MySQL 服务资源使用
Get-Process mysqld | Select-Object CPU, WorkingSet, PagedMemorySize

# 检查 Windows 事件日志中的 MySQL 错误
Get-EventLog -LogName Application -Source "MySQL*" -Newest 20
```

### 2. 慢查询优化

#### Linux/macOS
```bash
# 查看慢查询配置
mysql -e "SHOW VARIABLES LIKE 'slow_query%';"
mysql -e "SHOW VARIABLES LIKE 'long_query_time';"

# 分析慢查询日志
pt-query-digest /var/log/mysql/slow.log > slow_report.txt

# 查看正在执行的慢查询
mysql -e "SELECT * FROM information_schema.PROCESSLIST WHERE TIME > 10 AND COMMAND != 'Sleep';"

# 查看慢查询日志
tail -f /var/log/mysql/slow.log
```

#### Windows PowerShell
```powershell
# 查看慢查询配置
mysql -e "SHOW VARIABLES LIKE 'slow_query%';"
mysql -e "SHOW VARIABLES LIKE 'long_query_time';"

# 查看正在执行的慢查询
mysql -e "SELECT * FROM information_schema.PROCESSLIST WHERE TIME > 10 AND COMMAND != 'Sleep';"

# 查看慢查询日志 (Windows 默认路径)
Get-Content "C:\ProgramData\MySQL\MySQL Server 8.0\Data\hostname-slow.log" -Wait

# 或使用 type 命令
type "C:\ProgramData\MySQL\MySQL Server 8.0\Data\hostname-slow.log" -wait

# 分析慢查询日志文件大小
Get-ChildItem "C:\ProgramData\MySQL\MySQL Server 8.0\Data\*slow.log" | Select-Object Name, Length, LastWriteTime
```

### 3. 主从复制延迟深度排查

**症状**：Seconds_Behind_Master 持续增大，从库数据明显落后于主库

**诊断流程**：
```bash
# 1. 基础复制状态检查
mysql -e "SHOW SLAVE STATUS\G" | grep -E "Seconds_Behind_Master|Slave_IO_Running|Slave_SQL_Running|Last_IO_Error|Last_SQL_Error"

# 2. 查看复制线程详情
mysql -e "SELECT * FROM performance_schema.replication_applier_status;"
mysql -e "SELECT * FROM performance_schema.replication_applier_status_by_worker;"

# 3. 检查主库二进制日志位置
mysql -e "SHOW MASTER STATUS;"

# 4. 对比主从执行位置
mysql -e "SHOW SLAVE STATUS\G" | grep -E "Master_Log_File|Read_Master_Log_Pos|Relay_Master_Log_File|Exec_Master_Log_Pos"

# 5. 检查复制延迟历史（如果启用 performance_schema）
mysql -e "SELECT * FROM performance_schema.replication_applier_status\G"

# 6. 查看从库 SQL 线程正在执行的查询
mysql -e "SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED, (WORK_COMPLETED/WORK_ESTIMATED*100) as pct FROM performance_schema.events_stages_current WHERE THREAD_ID IN (SELECT THREAD_ID FROM performance_schema.threads WHERE NAME LIKE '%sql%');"
```

**延迟原因分析**：

| 延迟类型 | 判断方法 | 解决方案 |
|---------|---------|---------|
| IO 线程延迟 | Master_Log_File ≠ Relay_Master_Log_File | 检查网络、增大 slave_net_timeout |
| SQL 线程延迟 | Relay_Master_Log_File = Master_Log_File 但 Exec_Master_Log_Pos 落后 | 开启并行复制、优化慢查询 |
| 大事务延迟 | 查看 events_stages_current | 拆分大事务、pt-online-schema-change |
| 锁等待延迟 | 查看 INNODB_LOCK_WAITS | 优化锁竞争、调整事务隔离级别 |

**处理方案**：

1. **开启并行复制（MySQL 5.7+）**：
```bash
# 基于 DATABASE 的并行（默认，适用于多库场景）
mysql -e "SET GLOBAL slave_parallel_type = 'DATABASE';"
mysql -e "SET GLOBAL slave_parallel_workers = 8;"

# 基于 LOGICAL_CLOCK 的并行（适用于单库高并发）
mysql -e "SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';"
mysql -e "SET GLOBAL slave_parallel_workers = 16;"
mysql -e "SET GLOBAL binlog_transaction_dependency_tracking = WRITESET;"

# 持久化到配置文件
# my.cnf
slave_parallel_type = LOGICAL_CLOCK
slave_parallel_workers = 16
slave_preserve_commit_order = 1
```

2. **优化复制性能**：
```bash
# 增大复制缓冲区
mysql -e "SET GLOBAL slave_max_allowed_packet = 1*1024*1024*1024;"
mysql -e "SET GLOBAL max_allowed_packet = 1*1024*1024*1024;"

# 优化 IO 线程
mysql -e "SET GLOBAL slave_net_timeout = 60;"
mysql -e "SET GLOBAL slave_checkpoint_period = 300;"

# 启用多线程复制（MySQL 8.0）
mysql -e "SET GLOBAL replica_parallel_workers = 16;"
```

3. **跳过无法执行的事务（谨慎使用）**：
```bash
# 方法1：跳过单个 GTID
mysql -e "STOP SLAVE; SET GTID_NEXT='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:1'; BEGIN; COMMIT; SET GTID_NEXT='AUTOMATIC'; START SLAVE;"

# 方法2：跳过当前错误（传统复制）
mysql -e "STOP SLAVE; SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1; START SLAVE;"

# 方法3：设置跳过特定错误码
mysql -e "STOP SLAVE; SET GLOBAL slave_skip_errors = '1062,1032'; START SLAVE;"
```

### 4. 锁等待和死锁深度分析

**症状**：应用报错 "Lock wait timeout exceeded" 或频繁死锁

**诊断流程**：
```bash
# 1. 查看当前锁等待
mysql -e "SELECT r.trx_id waiting_trx_id, r.trx_mysql_thread_id waiting_thread, r.trx_query waiting_query, b.trx_id blocking_trx_id, b.trx_mysql_thread_id blocking_thread, b.trx_query blocking_query, TIMESTAMPDIFF(SECOND, b.trx_started, NOW()) as blocking_seconds FROM information_schema.innodb_lock_waits w INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;"

# 2. 查看所有锁
mysql -e "SELECT * FROM information_schema.INNODB_LOCKS;"
mysql -e "SELECT * FROM information_schema.INNODB_LOCK_WAITS;"

# 3. 查看事务详情
mysql -e "SELECT trx_id, trx_mysql_thread_id, trx_state, trx_started, TIMESTAMPDIFF(SECOND, trx_started, NOW()) as trx_seconds, LEFT(trx_query, 100) as query_preview FROM information_schema.INNODB_TRX ORDER BY trx_started;"

# 4. 查看最近死锁信息
mysql -e "SHOW ENGINE INNODB STATUS\G" | grep -A 50 "LATEST DETECTED DEADLOCK"

# 5. 查看锁等待统计
mysql -e "SHOW GLOBAL STATUS LIKE 'Innodb_row_lock_%';"

# 6. 启用死锁日志记录（MySQL 8.0）
mysql -e "SET GLOBAL innodb_print_all_deadlocks = ON;"
```

**锁类型分析**：

| 锁类型 | 说明 | 常见场景 |
|--------|------|---------|
| 行锁 (X) | 排他锁 | UPDATE、DELETE、SELECT FOR UPDATE |
| 行锁 (S) | 共享锁 | SELECT LOCK IN SHARE MODE |
| 间隙锁 (Gap) | 防止幻读 | 范围查询、唯一键冲突检查 |
| 临键锁 (Next-Key) | 行锁+间隙锁 | 默认的 InnoDB 锁类型 |
| 插入意向锁 | 插入操作等待 | INSERT 等待间隙锁释放 |
| 自增锁 | AUTO_INCREMENT | 表级锁，批量插入时影响性能 |

**处理方案**：

1. **终止阻塞事务**：
```bash
# 查看阻塞时间超过 60 秒的事务
mysql -e "SELECT GROUP_CONCAT(CONCAT('KILL ', trx_mysql_thread_id) SEPARATOR '; ') as kill_cmds FROM information_schema.INNODB_TRX WHERE TIMESTAMPDIFF(SECOND, trx_started, NOW()) > 60;"

# 执行终止
mysql -e "KILL <blocking_thread_id>;"
```

2. **优化锁竞争**：
```sql
-- 优化方案1：缩短事务时间
BEGIN;
-- 只包含必要的操作
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- 优化方案2：按相同顺序访问资源
-- 所有事务都先操作 A 表，再操作 B 表

-- 优化方案3：使用乐观锁替代悲观锁
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = 10;

-- 优化方案4：降低隔离级别（如果可以接受）
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

3. **死锁自动重试机制（应用层）**：
```python
# Python 示例
import mysql.connector
from mysql.connector import Error
import time

def execute_with_retry(cursor, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            if e.errno == 1213 and attempt < max_retries - 1:  # Deadlock
                time.sleep(0.1 * (attempt + 1))
                continue
            raise
```

### 5. 分区表问题诊断与维护

**症状**：分区表查询慢、分区维护困难、数据分布不均

**诊断流程**：
```bash
# 1. 查看分区表信息
mysql -e "SELECT TABLE_SCHEMA, TABLE_NAME, PARTITION_NAME, PARTITION_METHOD, PARTITION_EXPRESSION, PARTITION_DESCRIPTION, TABLE_ROWS FROM information_schema.PARTITIONS WHERE TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys') AND PARTITION_NAME IS NOT NULL ORDER BY TABLE_SCHEMA, TABLE_NAME, PARTITION_NAME;"

# 2. 查看特定表的分区详情
mysql -e "SHOW CREATE TABLE db_name.table_name\G"

# 3. 检查分区数据分布
mysql -e "SELECT PARTITION_NAME, TABLE_ROWS, DATA_LENGTH, INDEX_LENGTH FROM information_schema.PARTITIONS WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'table_name';"

# 4. 查看分区修剪情况
mysql -e "EXPLAIN PARTITIONS SELECT * FROM table_name WHERE created_at > '2024-01-01';"

# 5. 检查分区表性能
mysql -e "SELECT * FROM performance_schema.table_io_waits_summary_by_table WHERE OBJECT_SCHEMA = 'db_name' AND OBJECT_NAME = 'table_name';"
```

**常见问题及处理**：

1. **创建 RANGE 分区表**：
```sql
-- 按时间范围分区
CREATE TABLE logs (
    id BIGINT AUTO_INCREMENT,
    message TEXT,
    created_at DATETIME,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION pfuture VALUES LESS THAN MAXVALUE
);

-- 按日期范围分区（更细粒度）
CREATE TABLE events (
    id BIGINT AUTO_INCREMENT,
    event_type VARCHAR(50),
    event_data JSON,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (TO_DAYS(created_at)) (
    PARTITION p202401 VALUES LESS THAN (TO_DAYS('2024-02-01')),
    PARTITION p202402 VALUES LESS THAN (TO_DAYS('2024-03-01')),
    PARTITION p202403 VALUES LESS THAN (TO_DAYS('2024-04-01')),
    PARTITION pfuture VALUES LESS THAN MAXVALUE
);
```

2. **分区维护操作**：
```bash
# 添加新分区
mysql -e "ALTER TABLE logs ADD PARTITION (PARTITION p2025 VALUES LESS THAN (2026));"

# 删除旧分区（快速删除大量数据）
mysql -e "ALTER TABLE logs DROP PARTITION p2022;"

# 重建分区（优化碎片）
mysql -e "ALTER TABLE logs REORGANIZE PARTITION p2023 INTO (PARTITION p2023 VALUES LESS THAN (2024));"

# 合并分区
mysql -e "ALTER TABLE logs REORGANIZE PARTITION p2023, p2024 INTO (PARTITION p2023_2024 VALUES LESS THAN (2025));"

# 分析分区统计
mysql -e "ALTER TABLE logs ANALYZE PARTITION p2024;"

# 修复分区
mysql -e "ALTER TABLE logs REPAIR PARTITION p2024;"
```

3. **分区表查询优化**：
```sql
-- 确保查询能够利用分区修剪
EXPLAIN PARTITIONS SELECT * FROM logs WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01';

-- 查看实际访问的分区
-- 应该只显示 p202401，而不是所有分区

-- 显式指定分区查询
SELECT * FROM logs PARTITION (p202401) WHERE message LIKE '%error%';

-- 获取分区元数据
SELECT
    PARTITION_NAME,
    TABLE_ROWS,
    ROUND(DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
    ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS index_mb
FROM information_schema.PARTITIONS
WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'logs'
ORDER BY PARTITION_NAME;
```

4. **自动化分区维护脚本**：
```bash
#!/bin/bash
# mysql_partition_maintenance.sh

DB_NAME="mydb"
TABLE_NAME="logs"
RETENTION_DAYS=90

# 获取需要删除的旧分区
OLD_PARTITIONS=$(mysql -e "SELECT PARTITION_NAME FROM information_schema.PARTITIONS WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_NAME = '$TABLE_NAME' AND PARTITION_DESCRIPTION != 'MAXVALUE' AND PARTITION_DESCRIPTION < TO_DAYS(DATE_SUB(NOW(), INTERVAL $RETENTION_DAYS DAY)) ORDER BY PARTITION_DESCRIPTION LIMIT 1;")

# 删除最旧的分区
for PARTITION in $OLD_PARTITIONS; do
    echo "删除分区: $PARTITION"
    mysql -e "ALTER TABLE $DB_NAME.$TABLE_NAME DROP PARTITION $PARTITION;"
done

# 添加下个月分区
NEXT_MONTH=$(date -d "+1 month" +%Y%m)
NEXT_MONTH_FIRST=$(date -d "+1 month" +%Y-%m-01)
NEXT_NEXT_MONTH_FIRST=$(date -d "+2 month" +%Y-%m-01)

echo "添加分区: p$NEXT_MONTH"
mysql -e "ALTER TABLE $DB_NAME.$TABLE_NAME ADD PARTITION (PARTITION p${NEXT_MONTH} VALUES LESS THAN (TO_DAYS('$NEXT_NEXT_MONTH_FIRST')));"

echo "分区维护完成"
```


### 6. 磁盘空间不足
```bash
# 查看数据文件大小
mysql -e "SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS size_gb FROM information_schema.tables GROUP BY table_schema ORDER BY size_gb DESC;"

# 查看二进制日志
mysql -e "SHOW BINARY LOGS;"

# 清理过期 binlog
mysql -e "PURGE BINARY LOGS BEFORE DATE(NOW() - INTERVAL 7 DAY);"

# 查看临时表使用
mysql -e "SHOW GLOBAL STATUS LIKE 'Created_tmp%';"
```

### 7. CPU 使用率过高

**症状**：MySQL 进程 CPU 使用率接近 100%，查询响应变慢

**诊断流程**：
```bash
# 1. 查看当前运行的查询
mysql -e "SELECT ID, USER, HOST, DB, COMMAND, TIME, STATE, LEFT(INFO, 100) as SQL_TEXT FROM information_schema.PROCESSLIST WHERE COMMAND != 'Sleep' ORDER BY TIME DESC;"

# 2. 查看 InnoDB 事务状态
mysql -e "SELECT * FROM information_schema.INNODB_TRX\G"

# 3. 查看锁等待
mysql -e "SELECT r.trx_id waiting_trx_id, r.trx_mysql_thread_id waiting_thread, r.trx_query waiting_query, b.trx_id blocking_trx_id, b.trx_mysql_thread_id blocking_thread, b.trx_query blocking_query FROM information_schema.innodb_lock_waits w INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;"

# 4. 查看最近死锁
mysql -e "SHOW ENGINE INNODB STATUS\G" | grep -A 30 "LATEST DETECTED DEADLOCK"
```

**处理方案**：
```bash
# 终止长时间运行的查询
mysql -e "SELECT CONCAT('KILL ',ID,';') as kill_cmd FROM information_schema.PROCESSLIST WHERE COMMAND != 'Sleep' AND TIME > 60 AND USER != 'system user';"

# 优化特定查询（添加索引）
mysql -e "ALTER TABLE table_name ADD INDEX idx_column (column_name);"

# 临时降低并发（减少 max_connections）
mysql -e "SET GLOBAL max_connections = 200;"
```

### 8. 表损坏修复

**症状**：查询表时报错 "Table is marked as crashed" 或 "Incorrect key file"

**诊断流程**：
```bash
# 1. 检查表状态
mysqlcheck -c database_name table_name

# 2. 查看错误日志
tail -f /var/log/mysql/error.log

# 3. 检查 MyISAM 表
mysql -e "CHECK TABLE database_name.table_name;"
```

**修复方案**：
```bash
# 修复 MyISAM 表
mysql -e "REPAIR TABLE database_name.table_name;"

# 或使用 mysqlcheck
mysqlcheck -r database_name table_name

# 对于 InnoDB，尝试恢复
mysql -e "ALTER TABLE database_name.table_name ENGINE=InnoDB;"
```

### 9. 主从复制中断

**症状**：从节点复制停止，Seconds_Behind_Master 为 NULL

**诊断流程**：
```bash
# 1. 查看复制状态
mysql -e "SHOW SLAVE STATUS\G" | grep -E "Slave_IO_Running|Slave_SQL_Running|Last_IO_Error|Last_SQL_Error"

# 2. 查看错误详情
mysql -e "SHOW SLAVE STATUS\G" | grep -A 5 "Last_Error"
```

**常见错误及处理**：

1. **主键冲突（Error 1062）**：
```bash
# 跳过当前错误（谨慎使用）
mysql -e "STOP SLAVE; SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1; START SLAVE;"

# 或使用 GTID 跳过
mysql -e "STOP SLAVE; SET GTID_NEXT='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:1'; BEGIN; COMMIT; SET GTID_NEXT='AUTOMATIC'; START SLAVE;"
```

2. **表不存在（Error 1146）**：
```bash
# 在主库导出表结构，在从库导入
mysqldump -h master_host -u user -p --no-data database_name table_name | mysql -h slave_host -u user -p database_name
```

3. **重新初始化从库**：
```bash
# 停止复制
mysql -e "STOP SLAVE; RESET SLAVE ALL;"

# 重新配置
mysql -e "CHANGE MASTER TO MASTER_HOST='master_host', MASTER_USER='repl_user', MASTER_PASSWORD='password', MASTER_AUTO_POSITION=1; START SLAVE;"
```

## 性能优化

### 关键配置参数
```ini
# my.cnf 核心优化参数
[mysqld]
# 内存配置
innodb_buffer_pool_size = 物理内存的 60-80%
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2

# 连接配置
max_connections = 1000
max_allowed_packet = 64M
wait_timeout = 600
interactive_timeout = 600

# 查询缓存（MySQL 8.0 已移除）
query_cache_type = 0
query_cache_size = 0

# 临时表
tmp_table_size = 128M
max_heap_table_size = 128M

# 日志配置
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
log_queries_not_using_indexes = 1
```

## 备份策略

### 逻辑备份
```bash
# mysqldump 完整备份
mysqldump -u root -p --all-databases --single-transaction --routines --triggers --events > full_backup.sql

# 单库备份
mysqldump -u root -p --single-transaction --routines mydb > mydb_backup.sql

# 压缩备份
mysqldump -u root -p --single-transaction mydb | gzip > mydb_backup.sql.gz
```

### 物理备份 (XtraBackup)
```bash
# 完整备份
xtrabackup --backup --target-dir=/backup/full

# 增量备份
xtrabackup --backup --target-dir=/backup/inc1 --incremental-basedir=/backup/full

# 准备恢复
xtrabackup --prepare --target-dir=/backup/full

# 恢复数据
xtrabackup --copy-back --target-dir=/backup/full
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|---------|
| Threads_connected | 当前连接数 | > max_connections * 0.8 |
| Slow_queries | 慢查询数 | > 10/min |
| Questions/Uptime | QPS | 基线对比 |
| Innodb_buffer_pool_reads | 物理读 | 持续增加 |
| Slave_lag | 复制延迟 | > 10s |
| Table_locks_waited | 锁等待 | > 0 |
| Innodb_row_lock_waits | 行锁等待 | > 100/min |
| Innodb_buffer_pool_pages_dirty | 脏页数量 | > 75% buffer pool |
| Threads_running | 活跃线程数 | > max_connections * 0.5 |
| Aborted_connects | 连接失败数 | 持续增加 |
| Handler_read_rnd_next | 全表扫描次数 | 持续增加 |

## 生产环境最佳实践

### 1. 配置优化（my.cnf）

```ini
[mysqld]
# 基础配置
datadir = /var/lib/mysql
socket = /var/lib/mysql/mysql.sock
symbolic-links = 0

# 内存配置（根据服务器内存调整）
innodb_buffer_pool_size = 4G              # 物理内存的 50-70%
innodb_buffer_pool_instances = 4          # 每个实例至少 1GB
innodb_log_file_size = 1G                 # redo log 大小
innodb_log_buffer_size = 64M
innodb_flush_log_at_trx_commit = 2        # 性能优先设为 2，安全优先设为 1
innodb_flush_method = O_DIRECT            # 避免双缓冲

# 连接配置
max_connections = 500
max_user_connections = 450
wait_timeout = 600
interactive_timeout = 600
max_connect_errors = 1000

# 查询缓存（MySQL 8.0 已移除）
query_cache_type = 0
query_cache_size = 0

# 临时表配置
tmp_table_size = 128M
max_heap_table_size = 128M
max_tmp_tables = 128

# 线程池配置（MySQL Enterprise 或 Percona）
thread_pool_size = 16
thread_pool_max_threads = 500

# 日志配置
log_error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1
log_queries_not_using_indexes = 1
log_slow_admin_statements = 1

# 二进制日志（主从复制必需）
server_id = 1
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
binlog_row_image = FULL
expire_logs_days = 7
max_binlog_size = 1G
sync_binlog = 1

# InnoDB 优化
innodb_file_per_table = 1
innodb_stats_on_metadata = 0
innodb_read_io_threads = 8
innodb_write_io_threads = 8
innodb_io_capacity = 2000
innodb_io_capacity_max = 4000
innodb_thread_concurrency = 0             # 0 = 不限制
innodb_lock_wait_timeout = 50
innodb_rollback_on_timeout = 0

# 安全配置
local_infile = 0
skip-symbolic-links
skip-name-resolve
```

### 2. 备份策略

**完整备份脚本**：
```bash
#!/bin/bash
# mysql_backup.sh

BACKUP_DIR="/backup/mysql/$(date +%Y%m%d)"
MYSQL_USER="backup"
MYSQL_PASS="password"
RETENTION_DAYS=7

mkdir -p $BACKUP_DIR

# 1. 完整逻辑备份
mysqldump -u$MYSQL_USER -p$MYSQL_PASS \
    --all-databases \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --master-data=2 \
    | gzip > $BACKUP_DIR/full_backup_$(date +%H%M%S).sql.gz

# 2. 备份配置文件
cp /etc/my.cnf $BACKUP_DIR/

# 3. 备份用户权限
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT CONCAT('SHOW GRANTS FOR ''',user,'''@''',host,''';') FROM mysql.user WHERE user!='root'" | \
    grep -v CONCAT | \
    xargs -I {} mysql -u$MYSQL_USER -p$MYSQL_PASS -e "{}" > $BACKUP_DIR/user_grants.sql

# 4. 清理旧备份
find /backup/mysql -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "备份完成: $BACKUP_DIR"
```

### 3. 监控告警脚本

```bash
#!/bin/bash
# mysql_monitor.sh

MYSQL_USER="monitor"
MYSQL_PASS="password"
HOST="localhost"

# 获取状态
get_status() {
    mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -e "SHOW GLOBAL STATUS LIKE '$1';" | tail -1
}

get_variable() {
    mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -e "SHOW GLOBAL VARIABLES LIKE '$1';" | tail -1
}

# 检查连接数
THREADS_CONNECTED=$(get_status "Threads_connected")
MAX_CONNECTIONS=$(get_variable "max_connections")
CONN_PCT=$((THREADS_CONNECTED * 100 / MAX_CONNECTIONS))

if [ $CONN_PCT -gt 80 ]; then
    echo "ALERT: 连接数过高: $THREADS_CONNECTED/$MAX_CONNECTIONS (${CONN_PCT}%)"
fi

# 检查复制延迟
SLAVE_LAG=$(mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -e "SHOW SLAVE STATUS\G" | grep "Seconds_Behind_Master" | awk '{print $2}')
if [ "$SLAVE_LAG" != "NULL" ] && [ $SLAVE_LAG -gt 60 ]; then
    echo "ALERT: 复制延迟: ${SLAVE_LAG}秒"
fi

# 检查慢查询
SLOW_QUERIES=$(get_status "Slow_queries")
echo "慢查询数: $SLOW_QUERIES"

# 检查锁等待
LOCK_WAITS=$(get_status "Innodb_row_lock_waits")
if [ $LOCK_WAITS -gt 100 ]; then
    echo "ALERT: 锁等待次数: $LOCK_WAITS"
fi
```

### 4. 安全加固

```bash
# 1. 删除匿名用户
mysql -e "DELETE FROM mysql.user WHERE User='';"

# 2. 删除远程 root 访问
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"

# 3. 删除测试数据库
mysql -e "DROP DATABASE IF EXISTS test; DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"

# 4. 创建专用管理用户
mysql -e "CREATE USER 'admin'@'10.0.0.%' IDENTIFIED BY 'StrongPassword123!';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'10.0.0.%' WITH GRANT OPTION;"

# 5. 启用 SSL
# my.cnf
require_secure_transport = ON
ssl_ca = /etc/mysql/ssl/ca.pem
ssl_cert = /etc/mysql/ssl/server-cert.pem
ssl_key = /etc/mysql/ssl/server-key.pem

# 6. 审计日志（MySQL Enterprise）
# 或安装 Percona Audit Log Plugin
```

### 5. 常用维护脚本

**表优化脚本**：
```bash
#!/bin/bash
# mysql_optimize.sh

DATABASE=$1

if [ -z "$DATABASE" ]; then
    echo "用法: $0 <database_name>"
    exit 1
fi

# 获取所有表
TABLES=$(mysql -e "SHOW TABLES FROM $DATABASE;" | tail -n +2)

for TABLE in $TABLES; do
    echo "优化表: $DATABASE.$TABLE"
    mysql -e "OPTIMIZE TABLE $DATABASE.$TABLE;"
done
```

**索引分析脚本**：
```bash
#!/bin/bash
# mysql_index_analysis.sh

mysql -e "
SELECT
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    t.TABLE_ROWS,
    s.INDEX_NAME,
    s.COLUMN_NAME,
    s.CARDINALITY,
    ROUND(s.CARDINALITY / t.TABLE_ROWS * 100, 2) AS selectivity
FROM information_schema.STATISTICS s
JOIN information_schema.TABLES t
    ON s.TABLE_SCHEMA = t.TABLE_SCHEMA
    AND s.TABLE_NAME = t.TABLE_NAME
WHERE t.TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
    AND t.TABLE_ROWS > 1000
    AND s.CARDINALITY / t.TABLE_ROWS < 0.1
ORDER BY t.TABLE_ROWS DESC
LIMIT 20;
"
```

**死锁监控脚本**：
```bash
#!/bin/bash
# mysql_deadlock_monitor.sh

LOG_FILE="/var/log/mysql/deadlocks.log"

# 从 InnoDB 状态中提取死锁信息
mysql -e "SHOW ENGINE INNODB STATUS\G" | grep -A 100 "LATEST DETECTED DEADLOCK" >> $LOG_FILE

echo "$(date): 死锁监控完成" >> $LOG_FILE
```

## 参考资料

### 官方文档
- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [MySQL 性能优化](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MySQL 复制](https://dev.mysql.com/doc/refman/8.0/en/replication.html)
- [InnoDB 存储引擎](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)

### 社区资源
- [Percona 博客](https://www.percona.com/blog/)
- [MySQL 性能调优指南](https://www.percona.com/resources/technical-presentations/mysql-performance-tuning-101)
- [高性能 MySQL（书籍）](https://www.oreilly.com/library/view/high-performance-mysql/9781492080503/)

### 工具推荐
- **Percona Toolkit**: 高级 MySQL 管理工具集
- **pt-query-digest**: 慢查询分析工具
- **pt-online-schema-change**: 在线 DDL 工具
- **MySQL Workbench**: 官方图形化管理工具
- **ProxySQL**: MySQL 代理和负载均衡器

## 输出规范

```
🐬 MySQL 诊断报告

📊 基本信息
- 版本：[version]
- 运行时间：[Uptime]
- 当前 QPS：[Questions/Uptime]
- 连接数：[Threads_connected/Max_used_connections]

⚡ 性能分析
- 慢查询：[Slow_queries]
- 查询缓存命中率：[(Qcache_hits/(Qcache_hits+Qcache_inserts))*100]%
- InnoDB 缓冲池命中率：[1-Innodb_buffer_pool_reads/Innodb_buffer_pool_read_requests]*100%

🔍 问题发现
1. [问题描述]

💡 解决方案
[具体处理步骤]
```

## MCP 工具支持

本 Skill 可通过 MCP (Model Context Protocol) 提供以下工具：

### 工具列表

| 工具名称 | 描述 | 必需参数 |
|---------|------|---------|
| `mysql_check_connection` | 检查 MySQL 连接和基本状态 | host, port, user |
| `mysql_get_processlist` | 获取当前进程列表 | host, port, user |
| `mysql_get_slave_status` | 检查主从复制状态 | host, port, user |
| `mysql_get_slow_queries` | 获取慢查询统计 | host, port, user |
| `mysql_check_table_sizes` | 检查数据库和表大小 | host, port, user |

### 工具定义示例

```json
{
  "name": "mysql_check_connection",
  "description": "检查 MySQL 连接状态和基本服务器信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "host": {
        "type": "string",
        "description": "MySQL 主机地址",
        "default": "localhost"
      },
      "port": {
        "type": "integer",
        "description": "MySQL 端口",
        "default": 3306
      },
      "user": {
        "type": "string",
        "description": "用户名"
      },
      "password": {
        "type": "string",
        "description": "密码"
      }
    },
    "required": ["host", "user"]
  }
}
```

```json
{
  "name": "mysql_get_processlist",
  "description": "获取 MySQL 当前运行的进程列表，识别慢查询和阻塞",
  "inputSchema": {
    "type": "object",
    "properties": {
      "host": {
        "type": "string",
        "default": "localhost"
      },
      "port": {
        "type": "integer",
        "default": 3306
      },
      "user": {
        "type": "string"
      },
      "password": {
        "type": "string"
      },
      "show_full": {
        "type": "boolean",
        "description": "是否显示完整 SQL",
        "default": false
      }
    },
    "required": ["host", "user"]
  }
}
```

```json
{
  "name": "mysql_get_slave_status",
  "description": "检查 MySQL 主从复制状态，包括延迟、IO/SQL 线程状态",
  "inputSchema": {
    "type": "object",
    "properties": {
      "host": {
        "type": "string",
        "default": "localhost"
      },
      "port": {
        "type": "integer",
        "default": 3306
      },
      "user": {
        "type": "string"
      },
      "password": {
        "type": "string"
      }
    },
    "required": ["host", "user"]
  }
}
```

```json
{
  "name": "mysql_get_slow_queries",
  "description": "获取 MySQL 慢查询统计信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "host": {
        "type": "string",
        "default": "localhost"
      },
      "port": {
        "type": "integer",
        "default": 3306
      },
      "user": {
        "type": "string"
      },
      "password": {
        "type": "string"
      }
    },
    "required": ["host", "user"]
  }
}
```

```json
{
  "name": "mysql_check_table_sizes",
  "description": "检查数据库和表的大小，识别大表",
  "inputSchema": {
    "type": "object",
    "properties": {
      "host": {
        "type": "string",
        "default": "localhost"
      },
      "port": {
        "type": "integer",
        "default": 3306
      },
      "user": {
        "type": "string"
      },
      "password": {
        "type": "string"
      },
      "database": {
        "type": "string",
        "description": "指定数据库，为空则检查所有"
      },
      "limit": {
        "type": "integer",
        "description": "返回的最大行数",
        "default": 20
      }
    },
    "required": ["host", "user"]
  }
}
```

### Python MCP Server 示例

```python
from mcp.server import Server
from mcp.types import TextContent
import subprocess
import json

app = Server("mysql-ops")

def build_mysql_cmd(host, port, user, password, command):
    pwd_flag = f"-p'{password}'" if password else ""
    return f"mysql -h {host} -P {port} -u{user} {pwd_flag} -e \"{command}\""

@app.call_tool()
def call_tool(name: str, arguments: dict):
    host = arguments.get("host", "localhost")
    port = arguments.get("port", 3306)
    user = arguments.get("user")
    password = arguments.get("password", "")

    if name == "mysql_check_connection":
        cmd = build_mysql_cmd(host, port, user, password,
            "SELECT 1 as connection_test; SHOW GLOBAL STATUS LIKE 'Uptime'; SHOW GLOBAL STATUS LIKE 'Threads_connected'; SHOW VARIABLES LIKE 'max_connections';")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [TextContent(type="text", text=result.stdout or result.stderr)]

    elif name == "mysql_get_processlist":
        show_full = "FULL" if arguments.get("show_full") else ""
        cmd = build_mysql_cmd(host, port, user, password,
            f"SHOW {show_full} PROCESSLIST;")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [TextContent(type="text", text=result.stdout)]

    elif name == "mysql_get_slave_status":
        cmd = build_mysql_cmd(host, port, user, password, "SHOW SLAVE STATUS\\G")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [TextContent(type="text", text=result.stdout)]

    elif name == "mysql_get_slow_queries":
        cmd = build_mysql_cmd(host, port, user, password,
            "SHOW GLOBAL STATUS LIKE 'Slow_queries'; SHOW VARIABLES LIKE 'slow_query%'; SHOW VARIABLES LIKE 'long_query_time';")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [TextContent(type="text", text=result.stdout)]

    elif name == "mysql_check_table_sizes":
        database = arguments.get("database", "")
        limit = arguments.get("limit", 20)
        db_filter = f"AND table_schema = '{database}'" if database else ""
        query = f"""SELECT table_schema, table_name,
            ROUND((data_length + index_length) / 1024 / 1024 / 1024, 2) AS size_gb,
            table_rows
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')
            {db_filter}
            ORDER BY (data_length + index_length) DESC
            LIMIT {limit};"""
        cmd = build_mysql_cmd(host, port, user, password, query)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [TextContent(type="text", text=result.stdout)]

if __name__ == "__main__":
    app.run()
```

## 示例：慢查询优化

输入：MySQL 出现大量慢查询，CPU 使用率很高

输出：
```
🐬 MySQL 诊断报告

📊 基本信息收集
执行以下命令：
mysql -e "SHOW GLOBAL STATUS LIKE 'Slow_queries';"
mysql -e "SHOW PROCESSLIST;"

🔍 诊断步骤

1. 查看慢查询日志分析
pt-query-digest /var/log/mysql/slow.log --limit 10

2. 检查缺失索引的查询
mysql -e "SELECT * FROM sys.statements_with_full_table_scans ORDER BY rows_examined DESC LIMIT 10;"

3. 查看执行计划
EXPLAIN SELECT * FROM large_table WHERE unindexed_column = 'value';

💡 优化方案

方案1：添加索引
ALTER TABLE table_name ADD INDEX idx_column (column_name);

方案2：优化 SQL
- 避免 SELECT *
- 添加合适的 WHERE 条件
- 使用 LIMIT 限制返回行数

方案3：分区表
对于大表，考虑按时间或范围分区

📋 长期优化
- 启用慢查询日志
- 定期分析慢查询
- 建立 SQL 审核流程
```

## 补充内容（2024年新增）

### MySQL 8.0+ 新特性应用

**窗口函数应用**：
```sql
-- 计算累计和
SELECT
    user_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) as cumulative_sum
FROM orders;

-- 计算排名
SELECT
    product_id,
    sales,
    RANK() OVER (ORDER BY sales DESC) as sales_rank,
    DENSE_RANK() OVER (ORDER BY sales DESC) as dense_rank
FROM product_sales;

-- 计算移动平均
SELECT
    date,
    value,
    AVG(value) OVER (ORDER BY date ROWS 6 PRECEDING) as moving_avg_7d
FROM metrics;
```

**CTE（公用表表达式）**：
```sql
-- 递归 CTE 查询层级数据
WITH RECURSIVE employee_hierarchy AS (
    -- 基础查询：顶级员工
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 递归查询：下属员工
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy;

-- 非递归 CTE
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') as month,
        SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT * FROM monthly_sales WHERE total_sales > 100000;
```

**JSON 数据类型操作**：
```sql
-- 创建包含 JSON 的表
CREATE TABLE user_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    profile JSON,
    INDEX idx_user_id (user_id),
    INDEX idx_profile_name ((CAST(profile->>'$.name' AS CHAR(255))))
);

-- 插入 JSON 数据
INSERT INTO user_profiles (user_id, profile) VALUES
(1, '{"name": "张三", "age": 30, "city": "北京", "tags": ["developer", "mysql"]}');

-- 查询 JSON 字段
SELECT
    user_id,
    profile->>'$.name' as name,
    profile->>'$.age' as age,
    JSON_CONTAINS(profile->>'$.tags', '"developer"') as is_developer
FROM user_profiles
WHERE profile->>'$.city' = '北京';

-- 更新 JSON 字段
UPDATE user_profiles
SET profile = JSON_SET(profile, '$.age', 31, '$.last_updated', NOW())
WHERE user_id = 1;

-- 删除 JSON 字段
UPDATE user_profiles
SET profile = JSON_REMOVE(profile, '$.tags[1]')
WHERE user_id = 1;
```

**Invisible Indexes（隐藏索引）**：
```sql
-- 创建隐藏索引（用于测试索引效果）
ALTER TABLE orders ADD INDEX idx_test (created_at) INVISIBLE;

-- 查询优化器会忽略隐藏索引
EXPLAIN SELECT * FROM orders WHERE created_at > '2024-01-01';

-- 使索引可见
ALTER TABLE orders ALTER INDEX idx_test VISIBLE;

-- 查看索引可见性
SELECT INDEX_NAME, IS_VISIBLE FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_NAME = 'orders';
```

### 深度性能优化

**执行计划深度分析**：
```bash
# 使用 EXPLAIN ANALYZE（MySQL 8.0.18+）
mysql -e "EXPLAIN ANALYZE SELECT * FROM large_table WHERE status = 'active' ORDER BY created_at DESC LIMIT 100;"

# 查看优化器追踪
SET optimizer_trace="enabled=on";
SELECT * FROM your_query;
SELECT * FROM information_schema.OPTIMIZER_TRACE;
SET optimizer_trace="enabled=off";
```

**索引优化策略**：
```sql
-- 1. 覆盖索引优化
-- 原查询
SELECT user_id, username FROM users WHERE email = 'test@example.com';
-- 优化：创建覆盖索引
ALTER TABLE users ADD INDEX idx_email_covering (email, user_id, username);

-- 2. 最左前缀原则
-- 复合索引 (a, b, c) 可以支持
-- WHERE a=1
-- WHERE a=1 AND b=2
-- WHERE a=1 AND b=2 AND c=3
-- 但不能支持 WHERE b=2（缺少最左列）

-- 3. 索引下推优化（ICP）
-- MySQL 8.0 默认启用，可以在存储引擎层过滤数据
EXPLAIN SELECT * FROM users WHERE name LIKE '张%' AND age > 20;
-- 查看是否使用 ICP
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE name LIKE '张%' AND age > 20;
```

**查询重写优化**：
```sql
-- 1. 避免 SELECT *，只查询需要的列
-- 差
SELECT * FROM users WHERE id = 1;
-- 好
SELECT id, username, email FROM users WHERE id = 1;

-- 2. 使用 UNION ALL 替代 OR（某些场景）
-- 差
SELECT * FROM orders WHERE user_id = 1 OR status = 'pending';
-- 好（如果各自有索引）
SELECT * FROM orders WHERE user_id = 1
UNION ALL
SELECT * FROM orders WHERE status = 'pending' AND user_id != 1;

-- 3. 使用 EXISTS 替代 IN（子查询）
-- 差
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);
-- 好
SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 1000);

-- 4. 延迟关联优化大数据分页
-- 差
SELECT * FROM orders ORDER BY created_at DESC LIMIT 1000000, 10;
-- 好
SELECT o.* FROM orders o
INNER JOIN (
    SELECT id FROM orders ORDER BY created_at DESC LIMIT 1000000, 10
) tmp ON o.id = tmp.id;
```

### 高可用架构方案

**MGR（MySQL Group Replication）运维**：
```bash
# 查看 MGR 状态
mysql -e "SELECT * FROM performance_schema.replication_group_members;"
mysql -e "SELECT * FROM performance_schema.replication_group_member_stats;"

# 查看当前主节点
mysql -e "SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'group_replication_primary_member';"

# 手动切换主节点
SELECT group_replication_set_as_primary('member_uuid');

# 添加新成员到 MGR
-- 在新节点上执行
CHANGE MASTER TO MASTER_USER='repl', MASTER_PASSWORD='password' FOR CHANNEL 'group_replication_recovery';
START GROUP_REPLICATION;
```

**InnoDB Cluster 管理**：
```bash
# 使用 MySQL Shell 管理 InnoDB Cluster
mysqlsh

# 连接并配置集群
\connect root@primary:3306
var cluster = dba.getCluster()

# 查看集群状态
cluster.status()

# 添加实例
cluster.addInstance('root@newnode:3306')

# 移除实例
cluster.removeInstance('root@oldnode:3306')

# 强制故障转移
cluster.forceQuorumUsingPartitionOf('root@surviving_node:3306')
```

**ProxySQL 读写分离配置**：
```sql
-- 在 ProxySQL 中配置
-- 1. 添加后端服务器
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES
(1, 'master.mysql', 3306),  -- 写组
(2, 'slave1.mysql', 3306),  -- 读组
(2, 'slave2.mysql', 3306);  -- 读组

-- 2. 配置监控
UPDATE global_variables SET variable_value='monitor' WHERE variable_name='mysql-monitor_username';

-- 3. 配置路由规则
INSERT INTO mysql_query_rules (rule_id, active, match_pattern, destination_hostgroup, apply)
VALUES
(1, 1, '^SELECT.*FOR UPDATE$', 1, 1),  -- 带锁的查询走主库
(2, 1, '^SELECT', 2, 1);               -- 普通查询走从库

-- 4. 加载配置
LOAD MYSQL SERVERS TO RUNTIME;
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
SAVE MYSQL QUERY RULES TO DISK;
```

### 监控和可观测性

**使用 Performance Schema 深度监控**：
```sql
-- 启用 Performance Schema 监控
UPDATE performance_schema.setup_consumers SET ENABLED = 'YES' WHERE NAME LIKE '%events%statements%';
UPDATE performance_schema.setup_instruments SET ENABLED = 'YES', TIMED = 'YES' WHERE NAME LIKE '%statement/sql%';

-- 查看最耗时的 SQL
SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    AVG_TIMER_WAIT/1000000000000 as avg_latency_sec,
    MAX_TIMER_WAIT/1000000000000 as max_latency_sec,
    SUM_ROWS_SENT,
    SUM_ROWS_EXAMINED,
    FIRST_SEEN,
    LAST_SEEN
FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 20;

-- 查看表 IO 统计
SELECT
    OBJECT_SCHEMA,
    OBJECT_NAME,
    COUNT_READ,
    SUM_TIMER_WAIT/1000000000000 as total_latency_sec,
    COUNT_WRITE,
    SUM_NUMBER_OF_BYTES_READ,
    SUM_NUMBER_OF_BYTES_WRITE
FROM performance_schema.table_io_waits_summary_by_table
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;

-- 查看锁等待
SELECT
    OBJECT_SCHEMA,
    OBJECT_NAME,
    THREAD_ID,
    EVENT_NAME,
    SQL_TEXT,
    TIMER_WAIT/1000000000000 as wait_time_sec
FROM performance_schema.events_waits_current
WHERE EVENT_NAME LIKE '%lock%';
```

**Prometheus + mysqld_exporter 监控**：
```yaml
# docker-compose.yml
version: '3'
services:
  mysqld-exporter:
    image: prom/mysqld-exporter:latest
    environment:
      - DATA_SOURCE_NAME="exporter:password@(mysql:3306)/"
    ports:
      - "9104:9104"
    command:
      - '--collect.global_status'
      - '--collect.engine_innodb_status'
      - '--collect.info_schema.processlist'
      - '--collect.info_schema.query_response_time'
```

**关键告警规则**：
```yaml
# Prometheus 告警规则
groups:
  - name: mysql
    rules:
      - alert: MySQLHighConnections
        expr: mysql_global_status_threads_connected / mysql_global_variables_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MySQL connection usage high"

      - alert: MySQLSlowQueries
        expr: rate(mysql_global_status_slow_queries[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MySQL slow queries increasing"

      - alert: MySQLReplicationLag
        expr: mysql_slave_lag_seconds > 30
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "MySQL replication lag high"

      - alert: MySQLInnoDBLogWaits
        expr: rate(mysql_global_status_innodb_log_waits[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MySQL InnoDB log waits detected"
```

### 数据安全与合规

**数据脱敏方案**：
```sql
-- 创建脱敏视图
CREATE VIEW users_masked AS
SELECT
    id,
    username,
    CONCAT(LEFT(email, 2), '***@', SUBSTRING_INDEX(email, '@', -1)) as email_masked,
    CONCAT('****', RIGHT(phone, 4)) as phone_masked,
    created_at
FROM users;

-- 使用 Masking Functions（MySQL Enterprise）
-- 或使用触发器实现简单脱敏
DELIMITER //
CREATE TRIGGER trg_mask_user_before_insert
BEFORE INSERT ON users_backup
FOR EACH ROW
BEGIN
    SET NEW.email = CONCAT(LEFT(NEW.email, 2), '***@', SUBSTRING_INDEX(NEW.email, '@', -1));
    SET NEW.phone = CONCAT('****', RIGHT(NEW.phone, 4));
END//
DELIMITER ;
```

**审计日志配置**：
```bash
# MySQL Enterprise Audit Plugin
# 或使用 Percona Audit Log Plugin

# 安装审计插件
INSTALL PLUGIN audit_log SONAME 'audit_log.so';

# 配置审计规则
SET GLOBAL audit_log_policy = 'ALL';  -- 记录所有操作
SET GLOBAL audit_log_format = 'JSON';
SET GLOBAL audit_log_file = '/var/log/mysql/audit.log';

# 查看审计日志状态
SHOW VARIABLES LIKE 'audit_log%';
```

### 自动化运维脚本

**自动化备份脚本（增强版）**：
```bash
#!/bin/bash
# mysql_backup_advanced.sh

BACKUP_DIR="/backup/mysql"
MYSQL_USER="backup"
MYSQL_PASS="password"
RETENTION_DAYS=7
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR/{full,incremental,schema}

# 1. 逻辑备份（使用 mydumper 并行备份）
if command -v mydumper &> /dev/null; then
    echo "Using mydumper for parallel backup..."
    mydumper -u $MYSQL_USER -p $MYSQL_PASS \
        --outputdir=$BACKUP_DIR/full/$DATE \
        --threads=4 \
        --compress \
        --trx-consistency-only \
        --regex '^(?!(mysql|information_schema|performance_schema|sys)\.)'
else
    echo "Using mysqldump..."
    mysqldump -u $MYSQL_USER -p $MYSQL_PASS \
        --all-databases \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        --master-data=2 \
        | gzip > $BACKUP_DIR/full/full_backup_$DATE.sql.gz
fi

# 2. 备份表结构
mysqldump -u $MYSQL_USER -p $MYSQL_PASS \
    --all-databases \
    --no-data \
    --routines \
    > $BACKUP_DIR/schema/schema_$DATE.sql

# 3. 备份用户权限
mysql -u $MYSQL_USER -p $MYSQL_PASS -e "
SELECT CONCAT('SHOW CREATE USER ''', user, '''@''', host, ''';') as sql
FROM mysql.user WHERE user NOT IN ('root', 'mysql.session', 'mysql.sys', 'debian-sys-maint')
UNION ALL
SELECT CONCAT('SHOW GRANTS FOR ''', user, '''@''', host, ''';') as sql
FROM mysql.user WHERE user NOT IN ('root', 'mysql.session', 'mysql.sys', 'debian-sys-maint');
" | grep -v sql | xargs -I {} mysql -u $MYSQL_USER -p $MYSQL_PASS -e "{}" > $BACKUP_DIR/schema/users_$DATE.sql

# 4. 清理旧备份
echo "Cleaning up old backups..."
find $BACKUP_DIR/full -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null
find $BACKUP_DIR/schema -name "*.sql" -mtime +$RETENTION_DAYS -delete

# 5. 备份验证
echo "Verifying backup..."
if [ -f "$BACKUP_DIR/full/$DATE/metadata" ] || [ -f "$BACKUP_DIR/full/full_backup_$DATE.sql.gz" ]; then
    echo "Backup completed successfully: $DATE"
    # 发送成功通知（可配置 webhook 或邮件）
else
    echo "Backup failed!"
    # 发送失败告警
    exit 1
fi
```

**健康检查自动化脚本**：
```bash
#!/bin/bash
# mysql_health_check.sh

MYSQL_USER="monitor"
MYSQL_PASS="password"
HOST="localhost"
PORT="3306"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== MySQL Health Check ==="
echo "Time: $(date)"

# 1. 连接检查
if ! mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -P$PORT -e "SELECT 1" > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Cannot connect to MySQL${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Connection OK${NC}"

# 2. 复制状态检查
SLAVE_STATUS=$(mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -P$PORT -e "SHOW SLAVE STATUS\G" 2>/dev/null)
if [ -n "$SLAVE_STATUS" ]; then
    IO_RUNNING=$(echo "$SLAVE_STATUS" | grep "Slave_IO_Running" | awk '{print $2}')
    SQL_RUNNING=$(echo "$SLAVE_STATUS" | grep "Slave_SQL_Running:" | awk '{print $2}')
    LAG=$(echo "$SLAVE_STATUS" | grep "Seconds_Behind_Master" | awk '{print $2}')

    if [ "$IO_RUNNING" == "Yes" ] && [ "$SQL_RUNNING" == "Yes" ]; then
        if [ "$LAG" == "NULL" ] || [ "$LAG" -gt 60 ]; then
            echo -e "${YELLOW}⚠ Replication lag: ${LAG} seconds${NC}"
        else
            echo -e "${GREEN}✓ Replication OK (lag: ${LAG}s)${NC}"
        fi
    else
        echo -e "${RED}✗ Replication stopped! IO: $IO_RUNNING, SQL: $SQL_RUNNING${NC}"
    fi
fi

# 3. 连接数检查
CONN_PCT=$(mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -P$PORT -e "
SELECT ROUND(MAX_CONNECTIONS / MAX(1, @@max_connections) * 100) as pct
FROM (SELECT COUNT(*) as MAX_CONNECTIONS FROM information_schema.PROCESSLIST) t;
" | tail -1)

if [ "$CONN_PCT" -gt 80 ]; then
    echo -e "${RED}✗ Connection usage: ${CONN_PCT}%${NC}"
elif [ "$CONN_PCT" -gt 60 ]; then
    echo -e "${YELLOW}⚠ Connection usage: ${CONN_PCT}%${NC}"
else
    echo -e "${GREEN}✓ Connection usage: ${CONN_PCT}%${NC}"
fi

# 4. 慢查询检查
SLOW_QUERIES=$(mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -P$PORT -e "SHOW GLOBAL STATUS LIKE 'Slow_queries';" | tail -1)
echo "Slow queries: $SLOW_QUERIES"

# 5. 表状态检查
mysql -u$MYSQL_USER -p$MYSQL_PASS -h$HOST -P$PORT -e "
SELECT
    table_schema,
    table_name,
    engine,
    table_rows,
    data_length/1024/1024 as data_mb
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
    AND (data_length/1024/1024 > 1000 OR table_rows > 10000000)
ORDER BY data_length DESC
LIMIT 10;
"

echo "=== Check completed ==="
```
