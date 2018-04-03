import json


class ConfigHelper(object):
    @staticmethod
    def load_json_data(config_file):
        with open(config_file, 'r') as reader:
            json_data = json.loads(reader.read())
        reader.close()
        return json_data

    @staticmethod
    def update_config(json_data, config_file):
        with open(config_file, "w") as writer:
            writer.write(json.dumps(json_data, indent=4, sort_keys=True))
        writer.close()
