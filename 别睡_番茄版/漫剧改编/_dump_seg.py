import json, io
sb = json.load(io.open(r'<DESKTOP>/别睡_番茄版\漫剧改编\storyboard.json', encoding='utf-8-sig'))
ep1 = sb['episodes'][0]
seg = ep1['segments'][0]
print('seg id:', seg['id'], '| sceneIndex:', seg['sceneIndex'], '| cuts:', len(seg['cuts']))
for i, c in enumerate(seg['cuts']):
    print('--- cut', i + 1, '|', c['seconds'], 's | size=', c['size'], '| camera=', c['camera'], '| chars=', c.get('characters'), '| props=', c.get('props'))
    print('frame:', c['frame'])
