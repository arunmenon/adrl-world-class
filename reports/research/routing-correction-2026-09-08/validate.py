"""Verify the bounded routing correction and preserved register semantics."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime
import hashlib
import importlib.util
import json
import re
import tomllib

R = Path(__file__).resolve().parents[3]
O = Path(__file__).resolve().parent
C = R.parent / 'adrl-core'
B = R.parent / '.adrl-execution-state/routing-fix-20260908T083657Z'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def decision(s):
    return re.search(r'^## Decision\s*\n(.*?)(?=^## |\Z)',s,re.M|re.S).group(1).strip()

backup=json.loads((B/'manifest.json').read_text())
assert all(sha(B/p)==m['sha256'] for p,m in backup.items())
adrs=sorted(R.glob('adr/*/ADRL-*.md'))
for p in adrs:
    old=(B/'adrl-world-class'/p.relative_to(R)).read_text();new=p.read_text()
    assert decision(old)==decision(new),p
    assert re.findall(r'^\| (?:Status|Maturity) \|.*$',old,re.M)==re.findall(r'^\| (?:Status|Maturity) \|.*$',new,re.M),p
index=re.findall(r'^\| \[(ADRL-[A-Z]{3}-\d{3})\]',(R/'INDEX.md').read_text(),re.M)
assert len(adrs)==len(index)==len(set(index))==77
assert sorted(index)==[p.stem for p in adrs]
spec=importlib.util.spec_from_file_location('checks',C/'tools/check_all.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
source=mod.source_manifest(C)
checks=json.loads((O/'checks-final/manifest.json').read_text())
lab=json.loads((O/'lab-final/manifest.json').read_text())
assert source==checks['source_before']==checks['source_after']==lab['source_manifest']
assert len(source)==322 and checks['status']=='passed'
assert len(checks['checks'])==11 and all(c['status']=='passed' for c in checks['checks'])
assert '911 passed, 8 skipped' in (O/'checks-final/tests.log').read_text()
assert '159 passed' in (O/'focused-final.log').read_text()
changed=sorted(p for p in source if not (B/'adrl-core'/p).exists() or sha(C/p)!=sha(B/'adrl-core'/p))
assert changed==sorted(['docs/adr-module-map.md','docs/routing-features.md','src/adrl/app.py','src/adrl/routing/features.py','tests/unit/routing/test_mixed_intent.py'])
assert sha(C/'artifacts/lab/routing-suite-v1.json')==lab['suite_sha256']
before=json.loads((O/'before.json').read_text());after=json.loads((O/'after-final.json').read_text())
historical=json.loads((R/'reports/research/routing-demonstration-2026-09-08/results.json').read_text())
# Locate the original matrix without modifying the earlier diagnostic.
oldmatrix=historical.get('stress',historical.get('stress_matrix'))
assert oldmatrix is not None
for previous,current in zip(oldmatrix['rows'],before['original']['rows']):
    assert previous['id']==current['id']
    for v in previous['variants']:
        assert previous['variants'][v]['decision']['decided_rung']==current['variants'][v]['decision']['decided_rung']
for key in ['original','fresh']:
    assert before[key]['input_sha256']==after[key]['input_sha256']
    assert not after[key]['invariant_failures'] and not after[key]['review_hypothesis_failures']
for row in after['fresh']['rows']:
    rung=row['variants']['ordinary']['decision']['decided_rung']
    assert rung=='local' if row['review_expectation']=='local' else rung!='local'
changes=json.loads((O/'route-changes-final.json').read_text())
assert sum(c['matrix']=='original' for c in changes)==7
assert sum(c['matrix']=='fresh' for c in changes)==18
lr=json.loads((O/'lab-final/results.json').read_text());rows={r['case_id']:r for r in lr['rows']}
for case in ['mixed-rename','mixed-explain']:
    assert rows[case]['decisions'][0]['decided_rung']=='frontier'
    assert rows[case]['dispatched'][0]['model']=='claude-fable-5-1'
assert lr['counts']=={'responded':13,'blocked':1,'upstream_error':1,'unsupported':1}
assert not lr['eligible_for_learning'] and lr['model_calls']==0
state=json.loads((R/'reports/research/adrl-execution-state.json').read_text())
automation=tomllib.loads(Path('/Users/arunmenon/.codex/automations/continue-adrl-implementation-waves/automation.toml').read_text())
assert automation['status']=='PAUSED' and state['automation']['status']=='paused'
assert state['current_build_checks']['tests_passed']==911
assert not state['automatic_graduation'] and not state['paid_api_budget_approved']

changed_docs=[R.parent/p for p,m in backup.items() if p.startswith('adrl-world-class/') and sha(R.parent/p)!=m['sha256'] and p.endswith('.md')]
docs=changed_docs+[R/'reports/adrl-routing-correction-2026-09-08.md',R/'reports/adrl-product-roadmap-2026-09-08.md',R/'design/adrl-experiment-lab-plan-2026-09-08.md',C/'docs/routing-features.md',O/'lab-final/report.md',O/'route-changes-final.md']
links=0;errors=[]
for p in docs:
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',p.read_text()):
        target=target.strip().strip('<>')
        if urlsplit(target).scheme:continue
        raw=target.partition('#')[0];local=(p.parent/unquote(raw)).resolve() if raw else p
        links+=1
        if local!=O/'validation.json' and not local.exists():errors.append([str(p),target])
assert not errors,errors
result={'passed':True,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'adrs_checked':77,'decision_status_maturity_changes':0,'runtime_inputs':322,
        'source_matches_final_lab_and_checks':True,'changed_runtime_files':changed,
        'tests_passed':911,'tests_skipped':8,'check_count':11,'focused_tests_passed':159,
        'before_final_component_decisions':720,'original_changed_cells':7,'fresh_changed_cells':18,
        'original_cases_and_lab_suite_preserved':True,'original_baseline_choices_reproduced':True,
        'new_features_version':'features-v2','learning_contract_features_version':'features-v1',
        'learning_admission_changes':0,'maturity_promotions':0,'model_calls':0,'new_paid_usage':False,
        'repair_cycles':1,'initial_full_check':'910 passed, 1 failed, 8 skipped',
        'remaining_limits':['lexical quote/negation over-routing','no model quality or savings evidence','no classifier execution','v2 learning/exploration not admitted'],
        'local_links_checked':links,'link_errors':errors,'automation_status':'PAUSED',
        'document_hashes':{str(p.relative_to(R.parent)):sha(p) for p in docs},
        'evidence_hashes':{str(p.relative_to(O)):sha(p) for p in O.rglob('*') if p.is_file() and p.name!='validation.json'}}
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['passed','adrs_checked','runtime_inputs','tests_passed','tests_skipped','local_links_checked','automation_status']},indent=2))
