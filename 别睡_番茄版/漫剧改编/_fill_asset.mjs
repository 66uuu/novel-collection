import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { resolveLayers, viewLayersHash, lookHash } from 'file:///<USER_HOME>/DoubaoWork/skills/character-refs/scripts/core.mjs';

const base = '<DESKTOP>/别睡_番茄版/漫剧改编/character-refs';
const sha256 = (x) => createHash('sha256').update(x).digest('hex');
const now = new Date().toISOString();

// 每个角色：视图 -> 文件(相对 default/) -> 参考的锚点版本
const plan = {
  '苏晚': {
    'front-full': { file: 'default/front-full.v1.png', anchorV: null },
    'face-front': { file: 'default/face-front.v1.png', anchorV: 1 },
    'side-full':  { file: 'default/side-full.v1.png', anchorV: 1 },
    'back-full':  { file: 'default/back-full.v1.png', anchorV: 1 },
  },
  '白衣的她': {
    'front-full': { file: 'default/front-full.v1.png', anchorV: null },
    'face-front': { file: 'default/face-front.v1.png', anchorV: 1 },
    'side-full':  { file: 'default/side-full.v1.png', anchorV: 1 },
    'back-full':  { file: 'default/back-full.v1.png', anchorV: 1 },
  },
  '张秀兰': {
    'front-full': { file: 'default/front-full.v1.png', anchorV: null },
    'face-front': { file: 'default/face-front.v1.png', anchorV: 1 },
    'side-full':  { file: 'default/side-full.v1.png', anchorV: 1 },
    'back-full':  { file: 'default/back-full.v1.png', anchorV: 1 },
  },
  '苏晚父亲': {
    'front-full': { file: 'default/front-full.v1.png', anchorV: null },
    'face-front': { file: 'default/face-front.v1.png', anchorV: 1 },
    'side-full':  { file: 'default/side-full.v1.png', anchorV: 1 },
    'back-full':  { file: 'default/back-full.v1.png', anchorV: 1 },
  },
  'ICU护士': {
    'front-full': { file: 'default/front-full.v2.png', anchorV: null, alsoV1: 'default/front-full.v1.png' },
    'face-front': { file: 'default/face-front.v1.png', anchorV: 2 },
    'side-full':  { file: 'default/side-full.v1.png', anchorV: 2 },
    'back-full':  { file: 'default/back-full.v1.png', anchorV: 2 },
  },
};

const anchorPrompt = (name) => ({
  '苏晚': 'Full-body photograph of a gaunt twenty-six-year-old Chinese woman, contemporary urban China, a tired office worker. Thin face with prominent cheekbones, deep bluish-black under-eye circles, chapped lips, tired bloodshot eyes. Black medium-length hair half-dried in a low ponytail. Oversized faded cotton t-shirt, loose home pants, barefoot. Portrait 2:3, white seamless backdrop, realistic photo.',
  '白衣的她': 'Full-body photograph of a ghostly gaunt young Chinese woman in her twenties, drenched and dripping. Pale bluish skin, sunken dark eye sockets, glassy empty wet eyes, head hanging low behind wet hair. Old washed-out blue-white shirt with yellowed patch, shirt past knees, bare feet in a pool of water. Portrait 2:3, white seamless backdrop, realistic photo.',
  '张秀兰': 'Full-body photograph of a worn fifty-three-year-old Chinese supermarket worker. Round tired face, deep crow\'s feet, sallow skin, greying hair in a loose low bun. Dark old coat over uniform vest and stained apron, dark trousers, mismatched shoes one black one brown. Portrait 2:3, white seamless backdrop, realistic photo.',
  '苏晚父亲': 'Full-body photograph of a stooped fifty-eight-year-old Chinese man, stroke survivor. Deeply lined weathered face, grey hair, heavy drooping eyelids, age spots. Worn dark jacket over rumpled checked shirt, dark trousers, plain cloth shoes. Portrait 2:3, white seamless backdrop, realistic photo.',
  'ICU护士': 'Full-body photograph of a composed Chinese ICU nurse in her early thirties. Neat oval face, calm steady eyes, low bun. Clean white coat over pale blue-grey scrubs, ID badge, surgical mask at chin, flat white ward shoes. Portrait 2:3, white seamless backdrop, realistic photo.',
})[name];

const neg = 'CGI, 3D render, digital painting, illustration, anime, airbrushed skin, plastic skin, beauty filter, oversharpened, HDR, glossy, text, watermark';

for (const [name, views] of Object.entries(plan)) {
  const assetPath = join(base, name, 'asset.json');
  const asset = JSON.parse(readFileSync(assetPath, 'utf8'));
  const L = resolveLayers(asset, 'default');
  const lh = lookHash(asset.outfits.default.look);
  const anchors = {}; // view -> version obj（先算 front-full）
  const outViews = {};
  for (const [view, p] of Object.entries(views)) {
    const versions = [];
    if (view === 'front-full' && p.alsoV1) {
      const v1path = join(base, name, p.alsoV1);
      if (existsSync(v1path)) {
        const sha = sha256(readFileSync(v1path));
        const v1 = {
          v: 1, id: `${name}/default/front-full/v1`, file: 'default/front-full.v1.png', sha256: sha,
          model: 'doubao-image', seed: null, prompt: anchorPrompt(name), negative: neg, refs: [], notes: ['v1 背景带病房环境，已由 v2 白底版替代'],
          layersHash: viewLayersHash(L, undefined), lookHash: lh, gates: [], createdAt: now, confirmed: 'auto',
        };
        versions.push(v1);
      }
    }
    const v = p.anchorV ? p.anchorV : 1;
    const fpath = join(base, name, p.file);
    const sha = sha256(readFileSync(fpath));
    const refs = p.anchorV ? [{ view: 'front-full', v: p.anchorV, sha256: anchors['front-full'] }] : [];
    const ver = {
      v, id: `${name}/default/${view}/v${v}`, file: p.file, sha256: sha,
      model: 'doubao-image', seed: null, prompt: view === 'front-full' ? anchorPrompt(name) : `${anchorPrompt(name)} (derived view: ${view})`,
      negative: neg, refs, notes: [], layersHash: viewLayersHash(L, undefined), lookHash: lh, gates: [], createdAt: now, confirmed: 'auto',
    };
    versions.push(ver);
    anchors[view] = sha;
    outViews[view] = { current: view === 'front-full' ? (p.alsoV1 ? 2 : 1) : 1, versions };
  }
  asset.outfits.default.views = outViews;
  asset.outfits.default.upgrades = asset.outfits.default.upgrades ?? [];
  writeFileSync(assetPath, JSON.stringify(asset, null, 2), 'utf8');
  console.log(`${name}: ${Object.keys(outViews).join(', ')}`);
}
console.log('done');
