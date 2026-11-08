import json, io
sb = json.load(io.open(r'<DESKTOP>/别睡_番茄版\漫剧改编\storyboard.json', encoding='utf-8-sig'))
seg = sb['episodes'][0]['segments'][0]
print('total seconds:', sum(c['seconds'] for c in seg['cuts']))
print('h3Prompt:')
print(seg['h3Prompt'])
