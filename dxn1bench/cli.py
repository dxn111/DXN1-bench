from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
from .core import load_questions, run, score_record

def main():
    parser=argparse.ArgumentParser(prog='dxn1-bench',description='Run and score DXN1-bench')
    sub=parser.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('questions',help='print benchmark question count and categories')
    r=sub.add_parser('run',help='run against an OpenAI-compatible chat endpoint')
    r.add_argument('--model',required=True); r.add_argument('--base-url',default=os.getenv('DXN1_BASE_URL','https://api.openai.com/v1'))
    r.add_argument('--api-key',default=os.getenv('DXN1_API_KEY')); r.add_argument('--output',default='results/run.json'); r.add_argument('--limit',type=int)
    s=sub.add_parser('score',help='score a saved run using the transparent baseline')
    s.add_argument('run_file'); s.add_argument('--output',default='results/report.json')
    a=parser.parse_args()
    if a.cmd=='questions':
        qs=load_questions(); print(f"Questions: {len(qs)}")
        for cat in sorted(set(x['category'] for x in qs)): print(f"{cat}: {sum(x['category']==cat for x in qs)}")
    elif a.cmd=='run':
        if not a.api_key: parser.error('Provide --api-key or set DXN1_API_KEY')
        rec=run(a.model,a.base_url,a.api_key,Path(a.output),a.limit); print(f"Saved {len(rec['results'])} responses to {a.output}")
    else:
        record=json.loads(Path(a.run_file).read_text(encoding='utf-8'))
        report=score_record(record,Path(a.output))
        print(json.dumps({"model":report['model'],"overall_percent":report['overall_percent'],"categories":report['categories'],"safety_flags_for_review":report['safety_flags_for_review']},indent=2))
if __name__=='__main__': main()
