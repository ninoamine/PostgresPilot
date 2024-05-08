from controllers import PostgresPilotWatcher

def main():
    postgresql_cr_watcher = PostgresPilotWatcher()
    postgresql_cr_watcher.is_postgresPilot_crd_installed()
    postgresql_cr_watcher.watch_postgresPilot_instances()


if __name__ == "__main__":
    main()