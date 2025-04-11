import yaml

class Config:
    def __init__(self, yml_files:list):
        self.configs = []
        for yml_file in yml_files:
            with open(yml_file, 'r') as f:
                yml_config = yaml.safe_load(f)
                print(f"loaded {yml_file}:\n", yml_config)
                self.configs.append(yml_config)
                self.__dict__.update(yml_config)

def load_config(yml_file='offset/1.12.1.yml'):
    config = Config([yml_file, 'config/global.yml'])
    return config

if __name__ == "__main__":
    config = load_config()
    # print(config.icon)
    # for i, ofs in enumerate(config.DstYOffsetArray):
    #     print(i, ofs)