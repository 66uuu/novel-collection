import json, io
sb = json.load(io.open(r'<DESKTOP>/别睡_番茄版\漫剧改编\storyboard.json', encoding='utf-8-sig'))
sc = json.load(io.open(r'<DESKTOP>/别睡_番茄版\漫剧改编\script.json', encoding='utf-8-sig'))
ep1s = sb['episodes'][0]['segments']
ep1sc = sc['episodes'][0]['scenes']
for seg in ep1s[1:]:
    sidx = seg['sceneIndex'] - 1
    scn = ep1sc[sidx] if sidx < len(ep1sc) else None
    print('=' * 20, seg['id'], '| scene', seg['sceneIndex'], '|', scn['sceneId'] if scn else '?', '| lighting:', scn.get('lighting') if scn else '?')
    for i, c in enumerate(seg['cuts']):
        print(f"  [{i+1}] {c['seconds']}s {c['size']} {c['camera']} chars={c.get('characters')} props={c.get('props')}")
        print('     frame:', c['frame'])
    print('  h3:', seg['h3Prompt'][:200].replace('\n', ' | '))
