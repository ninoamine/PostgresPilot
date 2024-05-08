from kubernetes import client, config, watch
from utils import Logger, postgresql_url_env
from .postgresPilotHandler import PostgresPilotHandler

class PostgresPilotWatcher:
    def __init__(self):
        try:
            config.load_kube_config()
        except config.config_exception.ConfigException:
            config.load_incluster_config()

        self.kube_api_extensions = client.ApiextensionsV1Api()
        self.kube_api = client.CustomObjectsApi()
        self.loggers = Logger(log_level="INFO")
    
    def is_postgresPilot_crd_installed(self):
        crds_list = self.kube_api_extensions.list_custom_resource_definition()
        for crd in crds_list.items:
            if crd.metadata.name == "postgresdatabases.postgrespilot.io":
                return True
        self.loggers.log_error("PostgresPilot not found in cluster")
        self.loggers.log_error("Please install PostgresqlPilot CRD")
        raise SystemError()
    
    def watch_postgresPilot_instances(self):
        resource_version = ""
        if not postgresql_url_env():
           self.loggers.log_error("Environment variable POSTGRSQL_URL not found") 
           raise SystemError()
        postgresql_handler = PostgresPilotHandler()
        self.loggers.log_info("Starting postgresql connection")
        postgresql_connection_error = postgresql_handler.connection_to_postgresql(postgresql_url_env())
        if postgresql_connection_error:
            self.loggers.log_error(postgresql_connection_error)
            raise SystemError
        self.loggers.log_info("PostgresPilot found in cluster")
        self.loggers.log_info("Starting to watch PostgresqlPilot resources")
        while True:
            try:
                stream = watch.Watch().stream(
                    self.kube_api.list_cluster_custom_object,
                    group="postgrespilot.io",
                    version="v1alpha1",
                    plural="postgresdatabases",
                    resource_version=resource_version,
                )
                
                for event in stream:
                    event_type = event["type"]
                    instance = event["object"]
                    
                    if event_type == "ADDED":
                        error_create_database = postgresql_handler.create_postgresql_database(instance['metadata']['name'])
                        if error_create_database:
                            self.loggers.log_error(error_create_database)
                        else:
                            self.loggers.log_info(f"New PostgreSQL database added: {instance['metadata']['name']}")
                    elif event_type == "DELETED":
                        error_delete_database = postgresql_handler.delete_postgresql_database(instance['metadata']['name'])
                        if error_delete_database:
                            self.loggers.log_error(error_delete_database)
                        else:
                            self.loggers.log_info(f"PostgreSQL database deleted: {instance['metadata']['name']}")
                    
                    resource_version = instance["metadata"]["resourceVersion"]
                    
            except Exception as e:
                self.loggers.log_error(f"Error watching PostgreSQL instances: {str(e)}")
        
        