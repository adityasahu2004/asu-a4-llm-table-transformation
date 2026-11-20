from strategies.common import synthesize

def generate(case_dir, client, model) -> str:
    return synthesize(case_dir, client, model, 's1', few_shot=False, consistency=False)
