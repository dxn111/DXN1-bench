from __future__ import annotations
import argparse, json
from pathlib import Path
from .core import DEFAULT_MODEL, load_questions, prepare, rate_record, verify_questions

def main():
    parser=argparse.ArgumentParser(prog='dxn1-bench',description='AI self-benchmark with Kilo free rubric ratings')
    sub=parser.add_subparsers(dest='cmd',required=True)
    sub.add_parser('questions',help='print question count and categories')
    p=sub.add_parser('prepare',help='create a response file for the AI respondent')
    p.add_argument('--output',default='results/run.json'); p.add_argument('--limit',type=int)
    v=sub.add_parser('verify',help='ask Kilo to verify the question bank using bounded web search')
    v.add_argument('--model',default=DEFAULT_MODEL); v.add_argument('--output',default='results/question-verification.json')
    r=sub.add_parser('rate',help='ask Kilo Auto Free to score respondent answers against rubrics')
    r.add_argument('run_file'); r.add_argument('--model',default=DEFAULT_MODEL); r.add_argument('--output',default='results/report.json'); r.add_argument('--verification',default='results/question-verification.json')
    a=parser.parse_args()
    if a.cmd=='questions':
        qs=load_questions(); print(f'Questions: {len(qs)}')
        for cat in sorted(set(x['category'] for x in qs)): print(f'{cat}: {sum(x["category"]==cat for x in qs)}')
    elif a.cmd=='prepare':
        rec=prepare(Path(a.output),a.limit); print(f"Prepared {len(rec['results'])} questions at {a.output}; the AI respondent must fill each response independently.")
    elif a.cmd=='verify':
        rep=verify_questions(Path(a.output),a.model); print(json.dumps(rep['summary'],indent=2)); print(f'Saved verification to {a.output}')
    else:
        rec=json.loads(Path(a.run_file).read_text(encoding='utf-8'))
        verpath=Path(a.verification); verification=json.loads(verpath.read_text(encoding='utf-8')) if verpath.exists() else None
        rep=rate_record(rec,Path(a.output),a.model,verification)
        print(json.dumps({k:rep[k] for k in ('respondent','judge_resolved_models','overall_percent','categories','safety_flags_for_review','completed','total_questions','rating_failures','question_verification_summary')},indent=2))
if __name__=='__main__': main()
