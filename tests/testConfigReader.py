from modules.configPropertiesReader import getConfigProperties

CONFIG_FILENAME = 'config.json'

props = getConfigProperties(CONFIG_FILENAME)

print(props)