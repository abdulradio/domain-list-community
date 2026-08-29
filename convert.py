import json
import os
import sys

file_path = sys.argv[1]
cat_name = sys.argv[2]
data_dir = './code/data'

def parse_file(path):
    suffixes, fulls, keywords, regexes = [], [], [], []
    if not os.path.exists(path):
        return suffixes, fulls, keywords, regexes
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            line = line.split('@')[0].strip()
            
            if line.startswith('full:'):
                fulls.append(line[5:])
            elif line.startswith('keyword:'):
                keywords.append(line[8:])
            elif line.startswith('regexp:'):
                regexes.append(line[7:])
            elif line.startswith('include:'):
                inc_suffixes, inc_fulls, inc_keywords, inc_regexes = parse_file(os.path.join(data_dir, line[8:]))
                suffixes.extend(inc_suffixes)
                fulls.extend(inc_fulls)
                keywords.extend(inc_keywords)
                regexes.extend(inc_regexes)
            elif line.startswith('domain:'):
                suffixes.append(line[7:])
            else:
                suffixes.append(line)
    return list(set(suffixes)), list(set(fulls)), list(set(keywords)), list(set(regexes))

suffixes, fulls, keywords, regexes = parse_file(file_path)

rule = {}
if fulls: rule['domain'] = fulls
if suffixes: rule['domain_suffix'] = suffixes
if keywords: rule['domain_keyword'] = keywords
if regexes: rule['domain_regex'] = regexes

rule_set = {
    'version': 1,
    'rules': [rule] if rule else []
}

os.makedirs('./tmp', exist_ok=True)
with open(f'./tmp/rule_{cat_name}.json', 'w') as out:
    json.dump(rule_set, out)
