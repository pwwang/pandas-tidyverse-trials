import argparse
import json
from pathlib import Path
from tqdm import tqdm
import numpy as np
import pandas as pd
import timeit
import cProfile

N = 100000
rng = np.random.default_rng(seed=42)
d = pd.DataFrame(
    np.column_stack([rng.choice(range(10), size=(N, 3)), rng.random((N, 7))]),
    columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
d_long = d.reset_index().rename(columns={'index': 'idx'}).melt(id_vars='idx', var_name='name')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pkg', type=str)
    args = parser.parse_args()
    pkg = args.pkg
    if pkg == 'pandas':
        pass
    elif pkg == 'dfply':
        from dfply import *
    elif pkg == 'dplython':
        from dplython import *
        d = DplyFrame(d)
        d_long = DplyFrame(d_long)
    elif pkg == "siuba":
        from siuba import *
    elif pkg == 'siuba-fast':
        from siuba import *
        from siuba.experimental.pd_groups import fast_filter, fast_summarize, fast_mutate
    elif pkg == 'datar':
        from datar.all import *
        from pipda import options
        options.assume_all_piping = True  # TODO: ipython でもこれをしないと動作しない?
        d >> arrange(f.a)  # TODO: ???

    with Path(f'commands/commands-{pkg}.json').open('r') as jsonfile:
        trials = json.load(jsonfile)

    for x in ['times', 'profiles']:
        Path(f'results/{x}').mkdir(parents=True, exist_ok=True)

    for trial, command in tqdm(trials.items()):
        print(trial)
        cProfile.run(command, filename=f'results/profiles/{pkg}-{trial}-profile')
        pd.DataFrame(
            {'sec': timeit.repeat(command, repeat=100, number=1, globals=locals())}
        ).assign(
            command=command, cat=trial, package=pkg
        ).to_csv(f'results/times/{pkg}-{trial}.csv', index=False)
