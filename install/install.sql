CREATE TABLE IF NOT EXISTS report (
    report_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT,
    monitoring_duration INTEGER,
    monitoring_start_time TEXT,
    monitoring_end_time TEXT
);

CREATE TABLE IF NOT EXISTS system_specs (
    system_specs_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    system_name TEXT,
    system_type TEXT,
    system_release_version_major INTEGER,
    system_release_version_minor INTEGER,
    machine_type TEXT,
    processor_type TEXT,
    processor_spec TEXT,
    ip_address TEXT,
    mac_address TEXT,
    last_boot_time TEXT,
    physical_core_count INTEGER,
    total_core_count INTEGER,
    max_core_frequency TEXT,
    total_memory TEXT,
    disk_information TEXT,
    report_fk INTEGER,
    CONSTRAINT fk_report
        FOREIGN KEY (report_fk)
        REFERENCES report(report_pk)
);

CREATE INDEX IF NOT EXISTS systemspecs_reportfk ON system_specs(report_fk);

CREATE TABLE IF NOT EXISTS system_metrics (
    system_metrics_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    cpu_percent INTEGER,
    memory_percent INTEGER,
    disk_percent INTEGER,
    disk_read_time INTEGER,
    disk_read_bytes INTEGER,
    disk_write_time INTEGER,
    disk_write_bytes INTEGER,
    network_bytes_sent INTEGER,
    network_bytes_received INTEGER,
    report_fk INTEGER,
    CONSTRAINT fk_report
        FOREIGN KEY (report_fk)
        REFERENCES report(report_pk)
);

CREATE INDEX IF NOT EXISTS systemmetrics_reportfk ON system_metrics(report_fk);

CREATE TABLE IF NOT EXISTS process_metrics (
    process_metrics_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    process_id INTEGER,
    process_name TEXT,
    process_command_line TEXT,
    metric_name INTEGER,
    metric_value REAL,
    report_fk INTEGER,
    CONSTRAINT fk_report
        FOREIGN KEY (report_fk)
        REFERENCES report(report_pk)
);

CREATE INDEX IF NOT EXISTS processmetrics_reportfk ON process_metrics(report_fk);