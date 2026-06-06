# Deploy Gomoku AI len internet

Huong dan nay dung Vercel cho frontend React/Vite va Render cho backend FastAPI. Blueprint Render tao 2 service:

- `gomoku-ai-backend`: API cho che do nguoi - may.
- `gomoku-ai-arena`: API cho che do AI tu dau.

## 1. Chuan bi repository

1. Day source code len GitHub.
2. Dam bao cac file sau co trong repo:
   - `render.yaml`
   - `backend/requirements.txt`
   - `backend/requirements-ml.txt`
   - `dl/model.py`
   - `dl/predict_policy.py`
   - `model/consultant_model.pt`
   - `frontend/package.json`
   - `frontend/.env.example`
   - `backend/.env.example`

Khong commit file `.env` that. Chi dung `.env.example` de ghi mau cau hinh.

## 2. Deploy backend va arena tren Render

### Cach khuyen nghi: dung Blueprint

1. Vao Render Dashboard.
2. Chon **New +** -> **Blueprint**.
3. Ket noi GitHub repository cua du an.
4. Render se doc `render.yaml` va tao 2 service:
   - `gomoku-ai-backend`
   - `gomoku-ai-arena`
5. Sau khi deploy xong, ghi lai 2 URL dang:

```text
https://gomoku-ai-backend.onrender.com
https://gomoku-ai-arena.onrender.com
```

### Cau hinh backend dang duoc khai bao

```yaml
rootDir: backend
buildCommand: pip install -r requirements-ml.txt
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
healthCheckPath: /api/health
```

Kiem tra backend:

```text
https://<render-backend-url>/api/health
https://<render-backend-url>/docs
```

Kiem tra arena:

```text
https://<render-arena-url>/arena/api/health
https://<render-arena-url>/docs
```

Neu deploy thu cong thay vi Blueprint, tao 2 **Web Service** Python:

Backend:

```text
Root Directory: backend
Build Command: pip install -r requirements-ml.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Arena:

```text
Root Directory: repo root
Build Command: pip install -r backend/requirements.txt
Start Command: uvicorn arena.service:app --host 0.0.0.0 --port $PORT
```

## 3. Deploy frontend tren Vercel

1. Vao Vercel Dashboard.
2. Chon **Add New** -> **Project**.
3. Import GitHub repository cua du an.
4. Trong phan project settings:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Them Environment Variable:

```text
VITE_API_BASE_URL=https://<render-backend-url>
VITE_ARENA_API_BASE_URL=https://<render-arena-url>
```

Sau do bam **Deploy**. URL frontend se co dang:

```text
https://<your-vercel-app>.vercel.app
```

## 4. Khoa CORS sau khi co URL Vercel

Luc dau `render.yaml` de:

```text
FRONTEND_ORIGINS=*
```

Gia tri nay giup deploy nhanh va test duoc ngay. Sau khi co URL Vercel, vao Render -> tung service backend/arena -> Environment va doi thanh:

```text
FRONTEND_ORIGINS=https://<your-vercel-app>.vercel.app
```

Neu co nhieu domain, ngan cach bang dau phay:

```text
FRONTEND_ORIGINS=https://app.vercel.app,https://custom-domain.com
```

Sau khi sua bien moi truong, redeploy backend va arena.

## 5. Checklist kiem tra demo

- Mo `https://<render-backend-url>/api/health`, thay `{"status":"ok"}`.
- Mo `https://<render-backend-url>/docs`, thay Swagger UI cua FastAPI.
- Goi `POST https://<render-backend-url>/api/get-consultation`, thay `model_available: true` neu model da duoc deploy.
- Mo `https://<render-arena-url>/arena/api/health`, thay `{"status":"ok"}`.
- Mo app Vercel.
- Danh mot nuoc co, AI tra loi duoc.
- Chuyen sang Arena va bam **Run arena**.
- Thu Easy/Medium/Hard.
- Kiem tra panel AI co hien reason, evaluation, completed depth va elapsed time.

## 6. Loi thuong gap

### Frontend bao backend unreachable

Kiem tra `VITE_API_BASE_URL` tren Vercel da dung URL Render chua. URL khong co dau `/` o cuoi, vi du:

```text
https://gomoku-ai-backend.onrender.com
```

Sau khi sua environment variable tren Vercel, can redeploy frontend.

### Loi CORS

Kiem tra `FRONTEND_ORIGINS` tren ca 2 service Render co dung origin Vercel khong. Origin chi gom protocol + domain, khong gom path:

```text
https://your-app.vercel.app
```

### Render lan dau phan hoi cham

Neu dung goi mien phi hoac instance ngu sau thoi gian khong co traffic, request dau tien co the cham. Cho backend warm up roi thu lai.

### AI Hard cham

Hard dung search sau hon Easy/Medium. Neu demo tren instance yeu, uu tien Medium de dam bao phan hoi on dinh.

### Consultant model khong loaded

Kiem tra cac diem sau:

1. Backend Render phai build bang:

```text
pip install -r requirements-ml.txt
```

2. Repository phai co file:

```text
model/consultant_model.pt
```

3. Repository phai co thu muc:

```text
dl/
```

4. Goi endpoint consultation de kiem tra:

```http
POST /api/get-consultation
```

Neu response co `model_available: false`, backend van chay classical AI duoc, nhung consultant advisor va hybrid policy prior se fallback ve classical ordering.

### Arena tao output path rong

Ban deploy dang gui `save_to_disk: false` de khong ghi file dataset vao filesystem tam thoi cua Render. Arena van tra summary va replay game. Neu can sinh JSONL that, chay CLI local:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 10
```

## 7. Cau hinh local tuong ung

Backend:

```powershell
cd backend
Copy-Item .env.example .env
.\start_backend.ps1
```

Frontend:

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm.cmd run dev
```

Local frontend van co Vite proxy `/api`, nen `VITE_API_BASE_URL` co the de trong khi chay local. Khi deploy Vercel thi bat buoc dat `VITE_API_BASE_URL`.
