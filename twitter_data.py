import yaml
from twarc import Twarc

with open("./secret/keys.yaml", "r") as keyfile:
    keys = yaml.load(keyfile, yaml.FullLoader)

t = Twarc(keys['ApiKey'], keys['ApiKeySecret'], keys['AccessToken'], keys['AccessTokenSecret'])


