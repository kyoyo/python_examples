import yaml


f = open('test.yaml')

x = yaml.load(f)
print(x)

print(x.keys())
print(x.get('spouse'))