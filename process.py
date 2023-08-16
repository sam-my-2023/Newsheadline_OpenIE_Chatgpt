import os
import re
import json
import csv
import random

from tqdm import tqdm

class NewsHeadlineProcessor:
    def __init__(self):
        super().__init__()
        # self.LABEL_TO_ID = {"Component-Whole(e2,e1)": "Component-Whole", 
        #             "Other": "Other", 
        #             "Instrument-Agency(e2,e1)": "Instrument-Agency", 
        #             "Member-Collection(e1,e2)": "Member-Collection", 
        #             "Cause-Effect(e2,e1)": "Cause-Effect", 
        #             "Entity-Destination(e1,e2)": "Entity-Destination", 
        #             "Content-Container(e1,e2)": "Content-Container", 
        #             "Message-Topic(e1,e2)": "Message-Topic", 
        #             "Product-Producer(e2,e1)": "Product-Producer", 
        #             "Member-Collection(e2,e1)": "Member-Collection", 
        #             "Entity-Origin(e1,e2)": "Entity-Origin", 
        #             "Cause-Effect(e1,e2)": "Cause-Effect", 
        #             "Component-Whole(e1,e2)": "Component-Whole", 
        #             "Message-Topic(e2,e1)": "Message-Topic", 
        #             "Product-Producer(e1,e2)": "Product-Producer", 
        #             "Entity-Origin(e2,e1)": "Entity-Origin", 
        #             "Content-Container(e2,e1)": "Content-Container", 
        #             "Instrument-Agency(e1,e2)": "Instrument-Agency", 
        #             "Entity-Destination(e2,e1)": "Entity-Destination"}
        
    def read(self, csvFilePath):
        features = []
        
        data = []
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader:
                data.append(rows)
        
                
        # if size is not None or size>len(companies):
        #     companies = random.sample(companies, size )
        # else:
        #     size = len(companies) 
        for idx,hl in tqdm(enumerate(data)):

            tokens = re.split(r'\s+', hl['headline'])
            
            # head_entity = d['h']['name']
            # tail_entity = d['t']['name']

            # rel = self.LABEL_TO_ID[d['relation']]
            # for i in range(size):
                # for j in range(i+1,size):
            feature = {
                'inputs': tokens,
                # 'labels': rel,
                'headline_idx':idx,
                # 'tail_entity':companies[i],
            }
                
            features.append(feature)
            
        return features

test_file = os.path.join("./data/one_day_sample.csv")

processor = NewsHeadlineProcessor()

test_features = processor.read(test_file)

i = 0
news = list()
for line in tqdm(test_features):
    new_item = {
        "idx": i, "sentence": " ".join(line["inputs"]),
        'headline_idx':line['headline_idx'],
        # "head_entity": line["head_entity"],
        # "tail_entity": line["tail_entity"],
        # "relation_type": re.sub("-", " ", line["labels"])
    }
    news.append(new_item)
    i += 1

with open("./data/newsheadline_processed.json", "w") as writer:
    writer.write(json.dumps(news, indent=4))