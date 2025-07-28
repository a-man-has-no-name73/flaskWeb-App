import numpy as np
import os

# 1) Load your merged dataset
npz = np.load("SC4021E0_merged.npz")
X = npz["x"]   # shape (N, 3000)
y = npz["y"]   # shape (N,)

# 2) Build 3-epoch context windows
#    For each i in [1 .. N-2], we take epochs [i-1], [i], [i+1]
ctx_X = []
ctx_y = []
for i in range(1, len(X)-1):
    window = np.concatenate([X[i-1], X[i], X[i+1]], axis=0)  # → shape (9000,)
    ctx_X.append(window)
    ctx_y.append(y[i])

ctx_X = np.array(ctx_X)  # shape (N-2, 9000)
ctx_y = np.array(ctx_y)  # shape (N-2,)

# 3) Save each window as its own .npz for single-upload prediction
out_dir = "epochs_context"
os.makedirs(out_dir, exist_ok=True)

for idx, (signal, label) in enumerate(zip(ctx_X, ctx_y)):
    fn = os.path.join(out_dir, f"context_{idx:04d}.npz")
    # store under key "data" so your Flask app will find it automatically
    np.savez_compressed(fn,
                        data=signal,    # model input
                        label=int(label)  # optional: ground-truth if you want
                       )

print(f"Saved {len(ctx_X)} files to '{out_dir}/'—each is a (9000,)→(1,9000,1) input.")
