import json, io
sb = json.load(io.open(r'<DESKTOP>/别睡_番茄版\漫剧改编\storyboard.json', encoding='utf-8-sig'))
ep1 = sb['episodes'][0]
print('EP1 segments:', len(ep1['segments']))
for seg in ep1['segments']:
    total = sum(c['seconds'] for c in seg['cuts'])
    chars = set()
    props = set()
    for c in seg['cuts']:
        chars.update(c.get('characters') or [])
        props.update(c.get('props') or [])
    print(f"{seg['id']} | scene={seg['sceneIndex']} | {len(seg['cuts'])} cuts | {total}s | chars={sorted(chars)} | props={sorted(props)}")
