import system_specs


report_fk = 1

try:
    system_specs.system_information()
# prints a new error message if you cancel the script.
except KeyboardInterrupt:
    print("Monitoring stopped.")
