"""Generate isometric game sprites for TERRA NOVA with fal.ai (nano-banana edit + birefnet background removal).

Each sheet is one image with several poses/items (consistent look within a sheet). The background is removed
with birefnet, then sprites are cut out by alpha connected components (row-major order) and saved to
web/assets/sprites/<sheet>_<n>.png. Raw outputs are kept in Asset/generated/ (never re-billed if present).

Usage: python tools/gen_assets_fal.py [sheet ...]     (default: all sheets)
Budget guard: stops before exceeding MAX_USD (owner approved US$1.50).
"""
import base64, io, json, os, re, sys, time
import requests
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "Asset", "generated"); os.makedirs(RAW, exist_ok=True)
OUT = os.path.join(ROOT, "web", "assets", "sprites"); os.makedirs(OUT, exist_ok=True)
LEDGER = os.path.join(RAW, "cost_ledger.json")
env = open(os.path.normpath(os.path.join(ROOT, "..", ".env")), encoding="utf-8").read()
KEY = re.search(r"^FAL_KEY\s*=\s*\"?([^\"\r\n]+)", env, re.M).group(1).strip()
H = {"Authorization": "Key " + KEY, "Content-Type": "application/json"}
PRICE_IMG = 0.0398
MAX_USD = 1.50

STYLE = ("Match the art style of the reference image exactly: detailed isometric pixel-art illustration, "
         "soft painterly shading, warm daylight from the upper left, crisp dark outlines, same palette and scale feel. ")
BG = ("Place every element separately on a plain flat solid light grey (#d9d9d9) background, evenly spaced in a grid, "
      "not touching or overlapping, no shadows on the background, no ground tiles, no text, no labels, no borders, no frames.")

SHEETS = {
    "player": dict(refs=["yard", "avatar"], target_h=150, prompt=STYLE +
        "Create a character sprite sheet of the SAME young male eco-worker shown in the second reference image "
        "(brown messy hair, aviator goggles on the forehead, green jacket over a light shirt, dark trousers, boots), "
        "full body, isometric 3/4 view, 8 poses in 2 rows of 4: row 1: (1) sitting on the ground dazed, "
        "(2) sitting and looking to his left, (3) sitting and looking to his right, (4) standing idle facing the viewer; "
        "row 2: (5) walking towards the viewer step A, (6) walking towards the viewer step B, "
        "(7) walking away from the viewer seen from the back step A, (8) walking away seen from the back step B. "
        "Identical face, outfit and proportions in all poses. " + BG),
    "npc": dict(refs=["yard"], target_h=120, prompt=STYLE +
        "Create 6 small pedestrian sprites for a city sidewalk, full body, side view walking to the right, "
        "in one row: (1-2) an older man in a batik shirt and black peci cap, two walking steps; "
        "(3-4) a woman in a long skirt carrying a woven market basket, two walking steps; "
        "(5-6) a schoolboy in a white shirt and red shorts with a backpack, two walking steps. "
        "Indonesian everyday clothing. " + BG),
    "vehicles": dict(refs=["yard"], target_h=None, prompt=STYLE +
        "Create 3 vehicle sprites seen from the side and slightly from above, driving to the right, in one row: "
        "(1) a small green pickup truck loaded with fresh vegetables, (2) an orange box delivery truck, "
        "(3) a small green three-wheeled waste collection cart (motorized tricycle) with a recycling symbol and "
        "a few sacks in the back. Same scale relative to each other. " + BG),
    "trash": dict(refs=["yard"], target_h=None, prompt=STYLE +
        "Create 8 small litter item sprites lying on the ground, isometric view, in 2 rows of 4: "
        "(1) crushed plastic water bottles, (2) crumpled aluminium drink cans, (3) a torn cardboard box with paper, "
        "(4) organic food waste and banana peels, (5) broken glass bottles, (6) a black plastic garbage bag, "
        "(7) used batteries (hazardous), (8) styrofoam food containers. Each item is a small pile, similar size. " + BG),
    "garden": dict(refs=["yard"], target_h=None, prompt=STYLE +
        "Create 4 sprites of the same raised wooden garden bed (isometric, about 2 by 1 tiles), in one row: "
        "(1) an empty bed with dark soil, (2) the bed with small green seedlings, (3) the bed with leafy vegetables "
        "ready to harvest, (4) a fenced empty dirt plot with a small wooden 'for sale' signpost without text. " + BG),
    "playerf": dict(refs=["yard", "playersheet"], target_h=150, prompt=STYLE +
        "The second reference image is the male player sprite sheet. Create the FEMALE counterpart with exactly the same "
        "8 poses, layout, size, viewing angle and pixel-art style: a young Indonesian woman eco-worker with long dark "
        "brown hair in a ponytail, the same aviator goggles on her forehead, the same green jacket over a light shirt, "
        "dark trousers and brown boots. 2 rows of 4: row 1: (1) sitting on the ground dazed, (2) sitting and looking "
        "around, (3) standing idle looking to her left, (4) standing idle facing the viewer; row 2: (5) walking towards "
        "the viewer, (6) walking away seen from the back step A, (7) standing seen from the back, (8) walking away seen "
        "from the back step B. Identical face, outfit and proportions in all poses. " + BG),
    "vehicles2": dict(refs=["yard"], target_h=None, prompt=STYLE +
        "Create 7 road vehicle sprites in PERFECT SIDE PROFILE VIEW, all facing and driving to the RIGHT (front of the "
        "vehicle on the right side), seen from the side at road level with only a very slight top-down tilt, wheels "
        "visible as circles, in 2 rows (4 then 3): (1) a small green pickup truck loaded with vegetables, (2) an orange "
        "box delivery truck, (3) a man riding a red motor scooter with a helmet, (4) a boy riding a bicycle, "
        "(5) a traditional Indonesian becak (pedicab: passenger seat in front, driver pedalling behind) with a driver, "
        "(6) a traditional delman (two-wheeled horse-drawn carriage with a brown horse in front, a driver and a small "
        "canopy), (7) a small green motorized three-wheeled waste collection cart with sacks. Consistent scale: the "
        "bicycle and motor scooter are small, the trucks are the largest. " + BG),
    "pohon": dict(refs=["yard"], target_h=None, prompt=STYLE +
        "Create 8 small sprites of organic litter from trees, isometric view, in 2 rows of 4: row 1 (lying on the "
        "ground): (1) a pile of dry brown and yellow fallen leaves, (2) a small bundle of broken dry twigs, "
        "(3) a fallen broken tree branch with a few green leaves, (4) a few fallen rotten mangoes and leaves; "
        "row 2 (single leaves in the air, for a falling animation): (5) one dry orange leaf, (6) one dry brown leaf "
        "rotated, (7) one yellow leaf, (8) one green leaf. The single leaves are small. " + BG),
    # single vehicles, strict side profile (the road in the yard art is almost horizontal)
    **{f"veh_{k}": dict(refs=["yard"], target_h=None, prompt=STYLE +
        "Create ONE vehicle sprite: " + desc + " Draw it in a STRICT 90-DEGREE SIDE PROFILE VIEW like a side-scrolling "
        "game: camera exactly at the side, NO three-quarter angle, NO front or rear face visible, the front of the vehicle "
        "points to the RIGHT edge of the image, the wheels are seen as flat circles in one horizontal line on the ground. "
        "Single object centred on a plain flat solid light grey (#d9d9d9) background, no shadow on the background, no text.")
       for k, desc in {
        "pikap": "a small green pickup truck with a load of fresh vegetables in the open cargo bed, driver visible in the side window.",
        "truk": "an orange box delivery truck with a closed cargo box behind the cab, driver visible in the side window.",
        "becak": "a traditional Indonesian becak (cycle rickshaw): the passenger seat with a striped canopy is at the FRONT "
                 "(right side), and an adult male driver in a shirt and cap sits on the bicycle saddle at the BACK (left side), "
                 "pedalling, holding the handlebar behind the canopy. Two small wheels at the front, one big wheel at the back.",
        "delman": "a traditional Indonesian delman: a brown horse walking at the FRONT (right side) pulling a small two-wheeled "
                  "wooden carriage behind it (left side) with a cloth canopy and a driver holding the reins.",
        "gerobak": "a small green motorized three-wheeled waste collection cart: the rider on the motorcycle part at the FRONT "
                   "(right side) and an open green cargo box with sacks of sorted waste and a recycling symbol at the back.",
       }.items()},
    "badges": dict(refs=["badge"], target_h=None, prompt=
        "Match the style of the reference badge exactly (glossy hexagonal game achievement badge with a metallic rim). "
        "Create 8 achievement badges in 2 rows of 4, each a hexagon with a single clear icon and no text: "
        "(1) a hand picking up litter, (2) a recycling arrows symbol, (3) a compost heap with a sprout, "
        "(4) a basket of harvested vegetables, (5) a gold coin stack, (6) a clean river wave, "
        "(7) a garden bed with a plus sign, (8) a golden crown with leaves. Varied rim colors: bronze, silver, gold, emerald. "
        "Plain flat solid light grey (#d9d9d9) background, badges evenly spaced, not touching, no text."),
}

REFS = {
    "yard": os.path.join(ROOT, "web", "assets", "img", "yard_iso.webp"),
    "avatar": os.path.join(ROOT, "web", "assets", "img", "ui_avatar.png"),
    "badge": os.path.join(ROOT, "web", "assets", "landing", "b_zwm.webp"),
    "playersheet": os.path.join(ROOT, "Asset", "generated", "player.png"),
}


def data_uri(path, crop=None, max_w=1024):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def ledger():
    return json.load(open(LEDGER)) if os.path.exists(LEDGER) else {"usd": 0.0, "items": []}


def run(endpoint, payload):
    r = requests.post(f"https://queue.fal.run/{endpoint}", headers=H, json=payload, timeout=120)
    r.raise_for_status()
    q = r.json()
    for _ in range(200):
        st = requests.get(q["status_url"], headers=H, timeout=60).json()
        if st.get("status") == "COMPLETED":
            break
        if st.get("status") in ("FAILED", "ERROR"):
            raise RuntimeError(st)
        time.sleep(3)
    return requests.get(q["response_url"], headers=H, timeout=60).json()


def generate(name):
    spec = SHEETS[name]
    raw = os.path.join(RAW, f"{name}.png")
    if not os.path.exists(raw):
        L = ledger()
        if L["usd"] + PRICE_IMG > MAX_USD:
            sys.exit(f"Budget guard: {L['usd']:.2f} USD spent, next image would exceed {MAX_USD}")
        refs = []
        for r in spec["refs"]:
            crop = (380, 60, 1420, 620) if r == "yard" else None   # yard crop: buildings, fence, truck, people scale
            refs.append(data_uri(REFS[r], crop))
        res = run("fal-ai/nano-banana/edit", {"prompt": spec["prompt"], "image_urls": refs,
                                               "num_images": 1, "output_format": "png"})
        url = res["images"][0]["url"]
        open(raw, "wb").write(requests.get(url, timeout=120).content)
        L["usd"] += PRICE_IMG; L["items"].append({"sheet": name, "t": time.time()})
        json.dump(L, open(LEDGER, "w"), indent=1)
        print(f"{name}: generated (total spent {L['usd']:.2f} USD)")
    cut = os.path.join(RAW, f"{name}_cut.png")
    if not os.path.exists(cut):
        res = run("fal-ai/birefnet/v2", {"image_url": data_uri(raw, max_w=2048), "output_format": "png"})
        open(cut, "wb").write(requests.get(res["image"]["url"], timeout=120).content)
        print(f"{name}: background removed")
    return cut


def components(alpha, min_area):
    """Connected components of alpha>32 on a 4x downsample (fast), returned as full-res boxes."""
    w, h = alpha.size
    s = 4
    small = alpha.resize((w // s, h // s), Image.BILINEAR).load()
    sw, sh = w // s, h // s
    seen = [[False] * sw for _ in range(sh)]
    boxes = []
    for y in range(sh):
        for x in range(sw):
            if seen[y][x] or small[x, y] <= 32:
                continue
            stack = [(x, y)]; seen[y][x] = True
            x0 = x1 = x; y0 = y1 = y; n = 0
            while stack:
                cx, cy = stack.pop(); n += 1
                x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1), (cx + 1, cy + 1), (cx - 1, cy - 1), (cx + 1, cy - 1), (cx - 1, cy + 1)):
                    if 0 <= nx < sw and 0 <= ny < sh and not seen[ny][nx] and small[nx, ny] > 32:
                        seen[ny][nx] = True; stack.append((nx, ny))
            if n * s * s >= min_area:
                boxes.append([x0 * s, y0 * s, (x1 + 1) * s, (y1 + 1) * s])
    # merge boxes that overlap (detached bits such as a hat or a wheel)
    merged = True
    while merged:
        merged = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] < b[2] + 6 and b[0] < a[2] + 6 and a[1] < b[3] + 6 and b[1] < a[3] + 6:
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]
                    boxes.pop(j); merged = True; break
            if merged:
                break
    return boxes


def slice_sheet(name, cut):
    spec = SHEETS[name]
    im = Image.open(cut).convert("RGBA")
    boxes = components(im.getchannel("A"), min_area=im.width * im.height // 900)
    # row-major order: group by row (centre y within half a median height), then by x
    boxes.sort(key=lambda b: (b[1] + b[3]) / 2)
    hmed = sorted(b[3] - b[1] for b in boxes)[len(boxes) // 2] if boxes else 1
    rows, cur = [], []
    for b in boxes:
        if cur and (b[1] + b[3]) / 2 - (cur[-1][1] + cur[-1][3]) / 2 > hmed * 0.5:
            rows.append(cur); cur = []
        cur.append(b)
    if cur:
        rows.append(cur)
    ordered = [b for r in rows for b in sorted(r, key=lambda b: b[0])]
    for f in os.listdir(OUT):
        if f.startswith(name + "_"):
            os.remove(os.path.join(OUT, f))
    meta = []
    for i, b in enumerate(ordered, 1):
        spr = im.crop(b)
        if spec["target_h"] and spr.height > spec["target_h"]:
            spr = spr.resize((round(spr.width * spec["target_h"] / spr.height), spec["target_h"]), Image.LANCZOS)
        elif spr.width > 360:
            spr = spr.resize((360, round(spr.height * 360 / spr.width)), Image.LANCZOS)
        spr.save(os.path.join(OUT, f"{name}_{i}.png"), optimize=True)
        meta.append(dict(file=f"{name}_{i}.png", w=spr.width, h=spr.height))
    print(f"{name}: {len(ordered)} sprites -> web/assets/sprites/")
    return meta


if __name__ == "__main__":
    names = sys.argv[1:] or list(SHEETS)
    allmeta = {}
    mpath = os.path.join(OUT, "sprites.json")
    if os.path.exists(mpath):
        allmeta = json.load(open(mpath))
    for n in names:
        allmeta[n] = slice_sheet(n, generate(n))
    json.dump(allmeta, open(mpath, "w"), indent=1)
    print("spent:", f"{ledger()['usd']:.2f} USD")
