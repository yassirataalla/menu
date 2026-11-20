import sys, os, cv2, numpy as np
from concurrent.futures import ProcessPoolExecutor
SRC, SP, DST = sys.argv[1:4]; frames = range(int(sys.argv[4]), int(sys.argv[5]) + 1)
K = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
def one(f):
    a = f"{SRC}f_{f:04d}.png"; p = f"{SP}f_{f:04d}.png"; d = f"{DST}f_{f:04d}.png"
    if not os.path.exists(a) or not os.path.exists(p): return 0
    img = cv2.imread(a); ps = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32) / 255
    al = ps[..., 3]; r = ps[..., 2] ** 2.2; g = ps[..., 1] ** 2.2; t = r + g + 1e-6
    cr, cg = al * r / t, al * g / t
    if cr.max() < 0.02 and cg.max() < 0.02: cv2.imwrite(d, img); return 1
    solid = cr > 0.97
    col = np.median(img[solid], axis=0) if solid.sum() > 20 else np.array([200, 255, 190.0])
    m = cv2.dilate((cr > 0.02).astype(np.uint8) * 255, K)
    out = cv2.inpaint(img, m, 5, cv2.INPAINT_TELEA).astype(np.float32) if m.any() else img.astype(np.float32)
    if m.any():
        ring = (cv2.dilate(m, K) > 0) & (m == 0); mb = m > 0
        if ring.sum() > 50:
            cap = np.percentile(img[ring].astype(np.float32), 70, axis=0)
            out[mb] = np.minimum(out[mb], cap[None, :])
    out = out * (1 - cg[..., None]) + col[None, None, :] * cg[..., None]
    cv2.imwrite(d, np.clip(out + 0.5, 0, 255).astype(np.uint8)); return 1
if __name__ == "__main__":
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with ProcessPoolExecutor(4) as ex: print("comp", sum(ex.map(one, frames, chunksize=16)))
