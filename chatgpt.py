import re
import json
import time
import openai

from tqdm import tqdm
import os

with open('./data/api_key','r') as f:
    api_key = f.read()

propmt_path = "./data/prompts.json"

company_file = os.path.join("./data/nasdaq_constituent.json")

companies = []
with open(company_file, 'r') as jf:
            jReader = json.load(jf)
            for obj in jReader:
                companies.append(obj['name'])
companies_str = "\",\"".join(companies)
companies_str = '[\"' + companies_str + '\"]'
openai.api_key = api_key

data = list()
bar = tqdm(json.load(open(propmt_path, "r")))
for line in bar:

    # ------------------ #
    #        Open
    # ------------------ #
    while True:
        try:
            # 0. ChaGPT Pred
            bar.set_description("0. O Head")
            open_head_ans = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": line["open"]["open_head"]}
                ]
            )["choices"][0]["message"]["content"]
            print(open_head_ans)

            open_head_processed = eval(open_head_ans)["event"]
            break
        except Exception as e:
            print(e)
            time.sleep(3)

    while True:
        try:
            bar.set_description("1. O Pred")

            open_pred = "Question: What is the relationship between the event '%s' and companies in the list '%s' regarding the text '%s'? Answer me in json format like { company name: the relation }  without any additional things including your notes and explanations!" % (open_head_processed, companies_str, line["info"]["sentence"])

            open_pred_chatgpt_ans = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": open_pred}
                ]
            )["choices"][0]["message"]["content"]
            print(open_pred_chatgpt_ans)
            open_pred_chatgpt_ans_processed = eval(open_pred_chatgpt_ans)
            break
        except Exception as e:
            print(e)
            time.sleep(3)

    # while True:
    #     try:
    #         # 1. 置信度 Conf
    #         bar.set_description("2. O Conf")
    #         open_conf_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": open_pred},
    #                 {"role": "assistant", "content": open_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["open"]["open_conf"]},
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         open_conf_chatgpt_ans = int(re.search("\d+", open_conf_chatgpt_ans).group())
    #         break
    #     except Exception as e:
    #         print(e)
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 2. 原因 Reason
    #         bar.set_description("3. O Reason")
    #         open_reason_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": open_pred},
    #                 {"role": "assistant", "content": open_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["open"]["open_reason"]},
    #             ]
    #         )["choices"][0]["message"]["content"]
    #         break
    #     except Exception as e:
    #         print(e)
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 3. 是否合理 Reasonable
    #         bar.set_description("4. O Reasonable")
    #         open_reasonable_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": open_pred},
    #                 {"role": "assistant", "content": open_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["open"]["open_reason"]},
    #                 {"role": "assistant", "content": open_reason_chatgpt_ans},
    #                 {"role": "user", "content": line["open"]["open_reasonable"]},
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         if "yes" in open_reasonable_chatgpt_ans.lower():
    #             open_reasonable_chatgpt_ans = 1
    #             break
    #         elif "no" in open_reasonable_chatgpt_ans.lower():
    #             open_reasonable_chatgpt_ans = 0
    #             break
    #         else:
    #             continue
    #     except Exception as e:
    #         print(e)
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 4. 是否虚构 Fictitious
    #         bar.set_description("5. O Fictitious")
    #         open_fictitious_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": open_pred},
    #                 {"role": "assistant", "content": open_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["open"]["open_reason"]},
    #                 {"role": "assistant", "content": open_reason_chatgpt_ans},
    #                 {"role": "user", "content": line["open"]["open_fictitious"]},
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         if "yes" in open_fictitious_chatgpt_ans.lower():
    #             open_fictitious_chatgpt_ans = 1
    #             break
    #         elif "no" in open_fictitious_chatgpt_ans.lower():
    #             open_fictitious_chatgpt_ans = 0
    #             break
    #         else:
    #             continue
    #     except Exception as e:
    #         print(e)
    #         time.sleep(3)

    # ------------------ #
    #        Close
    # ------------------ #
    # while True:
    #     try:
    #         # 5. ChaGPT Pred
    #         bar.set_description("5. C Pred")
    #         close_pred_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": line["close"]["close_pred"]}
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         close_pred_chatgpt_ans_processed = eval(close_pred_chatgpt_ans)["label"]
    #         break
    #     except:
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 6. 置信度 Conf
    #         bar.set_description("6. C Conf")
    #         close_conf_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": line["close"]["close_pred"]},
    #                 {"role": "assistant", "content": close_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["close"]["close_conf"]},
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         close_conf_chatgpt_ans = int(re.search("\d+", close_conf_chatgpt_ans).group())
    #         break
    #     except:
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 7. 原因 Reason
    #         bar.set_description("7. C Reason")
    #         close_reason_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": line["close"]["close_pred"]},
    #                 {"role": "assistant", "content": close_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["close"]["close_reason"]},
    #             ]
    #         )["choices"][0]["message"]["content"]
    #         break
    #     except:
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 8. 是否合理 Reasonable
    #         bar.set_description("8. C Reasonable")
    #         close_reasonable_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": line["close"]["close_pred"]},
    #                 {"role": "assistant", "content": close_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["close"]["close_reason"]},
    #                 {"role": "assistant", "content": close_reason_chatgpt_ans},
    #                 {"role": "user", "content": line["close"]["close_reasonable"]},
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         if "yes" in close_reasonable_chatgpt_ans.lower():
    #             close_reasonable_chatgpt_ans = 1
    #             break
    #         elif "no" in close_reasonable_chatgpt_ans.lower():
    #             close_reasonable_chatgpt_ans = 0
    #             break
    #         else:
    #             continue
    #     except:
    #         time.sleep(3)

    # while True:
    #     try:
    #         # 9. 是否虚构 Fictitious
    #         bar.set_description("9. C Fictitious")
    #         close_fictitious_chatgpt_ans = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": line["close"]["close_pred"]},
    #                 {"role": "assistant", "content": close_pred_chatgpt_ans},
    #                 {"role": "user", "content": line["close"]["close_reason"]},
    #                 {"role": "assistant", "content": close_reason_chatgpt_ans},
    #                 {"role": "user", "content": line["close"]["close_fictitious"]},
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         if "yes" in close_fictitious_chatgpt_ans.lower():
    #             close_fictitious_chatgpt_ans = 1
    #             break
    #         elif "no" in close_fictitious_chatgpt_ans.lower():
    #             close_fictitious_chatgpt_ans = 0
    #             break
    #         else:
    #             continue
    #     except:
    #         time.sleep(3)
    
    # while True:
    #     try:
    #         Response_top = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "user", "content": line["close"]["close_top3_top5"]}
    #             ]
    #         )["choices"][0]["message"]["content"]

    #         Response_re = re.search('\{(.+?)\}', Response_top).group()

    #         Top3 = eval(Response_re)["three"]
    #         Top5 = eval(Response_re)["five"]
    #         break
    #     except:
    #         time.sleep(1)

    answer = {
        # 1. 基本内容
        "idx": line["info"]["idx"],
        "sentence": line["info"]["sentence"],
        # "tailEntity": line["info"]["tail_entity"],
        "GroundTruth": None,

        # 2. Open 场景下的回答
        "isOpenCorrect": -1,
        "headEntity": open_head_processed,
        "Open": open_pred_chatgpt_ans_processed,
        # "OConf": open_conf_chatgpt_ans,
        # "Reason4O": open_reason_chatgpt_ans,
        # "ifR4OAuto": open_reasonable_chatgpt_ans,
        # "ifR4OManual": -1,
        # "ifR4OFicAuto": open_fictitious_chatgpt_ans,
        # "ifR4OFicManual": -1,

        # 2. Close 场景下的回答
        # "isCloseCorrect": 1 if close_pred_chatgpt_ans_processed == line["info"]["label"].split("/")[-1] else 0,
        # "Closed": close_pred_chatgpt_ans_processed,
        # "CConf": close_conf_chatgpt_ans,
        # "Reason4C": close_reason_chatgpt_ans,
        # "ifR4CAuto": close_reasonable_chatgpt_ans,
        # "ifR4CManual": -1,
        # "ifR4CFicAuto": close_fictitious_chatgpt_ans,
        # "ifR4CFicManual": -1
    }

    data.append(answer)

with open("./data/outputs.json", "w") as f:
    f.write(json.dumps(data, indent=4))