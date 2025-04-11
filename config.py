import yaml

class Config:
    def __init__(self, yml_file):
        with open(yml_file, 'r') as f:
            yml_config = yaml.safe_load(f)
            print(yml_config)
            self.config = yml_config
            self.__dict__.update(yml_config)

def load_config(yml_file='offset/1.12.1.yml'):
    config = Config(yml_file)
    return config

if __name__ == "__main__":
    config = load_config()
    for i, ofs in enumerate(config.DstYOffsetArray):
        print(i, ofs)