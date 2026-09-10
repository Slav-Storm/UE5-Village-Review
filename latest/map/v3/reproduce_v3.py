from pathlib import Path
import json,sys,shutil,subprocess,argparse
p=argparse.ArgumentParser();p.add_argument("--work",required=True);a=p.parse_args()
source=Path(__file__).resolve().parent;work=Path(a.work).resolve()
if work.exists() and any(work.iterdir()):raise SystemExit("Use a new empty scratch directory; closed package is never overwritten.")
(work/"inputs").mkdir(parents=True,exist_ok=True)
for n in ["map_data.json","map_views.json","t0_activity.json","t1_simulation.json","bone_completion.json","massacre_behaviour_rules.json"]:shutil.copyfile(source.parent/n,work/"inputs"/n)
for n in ["geometry_v3.py","initial_v3.py","engine_v3.py"]:shutil.copyfile(source/n,work/n)
subprocess.run([sys.executable,str(work/"initial_v3.py")],check=True)
# Clear geometry route cache at the same five-cycle inspection boundaries used by the original run.
sys.path.insert(0,str(work))
from engine_v3 import Sim,OUT
from geometry_v3 import CACHE
s=json.loads((OUT/"state.json").read_text());sim=Sim(s)
while not sim.s["closed"]:
 if sim.s["cycle"]%5==0:CACHE.clear()
 sim.run_cycle()
closed=json.loads((source/"v3_simulation.json").read_text())
check={k:sim.s[k]==closed[k] for k in ["casualties","decisions","people","sources"]}
(OUT/"reproduction_check.json").write_text(json.dumps(check,indent=2))
print(check)
