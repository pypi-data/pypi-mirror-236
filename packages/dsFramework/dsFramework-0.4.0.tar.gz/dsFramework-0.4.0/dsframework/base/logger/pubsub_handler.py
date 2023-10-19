import datetime
import json
import logging


class PubSubHandler(logging.StreamHandler):

    def __init__(self, gcp_project_name, topic_name, ds_project_name, resource_type, wait=False):
        super().__init__()
        from google.cloud import pubsub_v1
        from concurrent.futures import ThreadPoolExecutor, TimeoutError

        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(gcp_project_name, topic_name)
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.wait = wait
        self.project_id = gcp_project_name
        self.ds_project_name = ds_project_name
        self.resource_type = resource_type

    def emit(self, record):
        try:
            level_name = record.levelname
            msg = self.format_entry(self.format(record), level_name, record.__dict__)
            data = json.dumps(msg).encode("utf-8")
            self.executor.submit(self.submit_func, self.publisher, self.topic_path, data)

        except TimeoutError as te:
            logging.exception(f'Pub/Sub timeout exception, make sure your are logged to gcloud, exception {te}')
        except Exception as e:
            logging.exception(f'Error publishing to Pub/Sub: {e}')

    def format_entry(self, message, bg_log_type, extra_fields):

        msg = json.loads(message)

        extra_input = ''
        output = ''
        from_host = ''
        from_service_account = ''
        pipeline_exec_time = ''
        predictable_object_count = ''
        model_version = ''

        if extra_fields and 'args' in extra_fields:
            arg_fields = extra_fields.get('args', '')
            if isinstance(arg_fields, dict):
                extra_input = arg_fields.get('input', '')
                output = arg_fields.get('output', '')
                from_host = arg_fields.get('from_host', '')
                from_service_account = arg_fields.get('from_service_account', '')
                pipeline_exec_time = arg_fields.get('pipeline_exec_time', '')
                predictable_object_count = arg_fields.get('predictable_object_count', '')
                if output:
                    model_version = dict(output[0]).get('version', '') \
                        if (isinstance(output, list) and len(output) > 0) else dict(output).get('version', '')
                else:
                    model_version = ''

        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        log_entry = {
            "type": bg_log_type,
            "insert_id": '',
            "request_input": str(extra_input),
            "request_message": str(msg).strip(),
            "request_output": str(output),
            "project_id": self.project_id,
            "project_name": self.ds_project_name,
            "version": model_version,
            "resource_type": self.resource_type,
            "timestamp": timestamp,
            "from_host": from_host,
            "from_service_account": from_service_account,
            "pipeline_exec_time": pipeline_exec_time,
            "predictable_object_count": str(predictable_object_count)
        }

        return log_entry

    def submit_func(self, publisher, topic_path, data):
        future = publisher.publish(topic_path, data)

        if self.wait:
            future.result(timeout=60)
