# surefireinsights

This is an application to be used to diagnose performance issues on different hardware.

Run App
	main
		create_sqlite_db.py
			configure_monitoring.py (report_pk)
				run_monitoring.py
					run_system_specs.py (once)
					run_system_metrics.py (on interval)
					run_process_metrics.py (on interval)