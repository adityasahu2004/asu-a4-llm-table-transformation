from strategies.common import synthesize

def generate(case_dir, client, model) -> str:
    return synthesize(case_dir, client, model, 's4', few_shot=True, consistency=True)
