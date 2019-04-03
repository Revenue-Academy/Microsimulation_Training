



with open('current_law_policy_pit_cit.json', 'r') as f:
    current_law_policy_dict = json.load(f)

current_law_policy_dict.update(item_rates_dict_for_json)

with open("current_law_policy.json", "w") as f:
    json.dump(current_law_policy_dict, f, indent=4, sort_keys=False)