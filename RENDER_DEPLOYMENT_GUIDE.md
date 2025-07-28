# Render Deployment Guide for Sleep Stage Prediction App

## Files Created for Render:

1. requirements.txt - Python dependencies
2. runtime.txt - Python version specification
3. Procfile - How to start the app
4. Modified app.py - Updated for production

## Render Deployment Steps:

### 1. Create GitHub Repository

- Create a new repository on GitHub
- Upload all your files:
  - app.py
  - fold1_model.keras
  - templates/ folder
  - requirements.txt
  - runtime.txt
  - Procfile

### 2. Deploy on Render

1. Go to render.com and sign up/login
2. Click "New +" -> "Web Service"
3. Connect your GitHub repository
4. Configure settings:
   - Name: sleep-stage-prediction
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   - Instance Type: Free

### 3. If Deployment Fails (TensorFlow/NumPy issues):

#### URGENT FIX for "Cannot import 'setuptools.build_meta'" error:

**Option A: Use the updated requirements.txt (recommended)**
The requirements.txt has been updated with explicit setuptools and wheel versions.
Also changed runtime.txt to python-3.10.13 for better compatibility.

**Option B: If still failing, try Python 3.13 compatible versions:**
1. In Render dashboard, go to your service settings
2. Replace requirements.txt content with requirements-py313.txt content:
```
setuptools>=68.0.0
wheel>=0.38.0
Flask==3.0.0
numpy>=1.26.0
tensorflow>=2.15.0
Werkzeug>=3.0.0
gunicorn>=21.2.0
```

**Option C: Minimal deployment (if TensorFlow keeps failing)**
Replace requirements.txt content with:
```
setuptools>=68.0.0
wheel>=0.38.0
Flask
numpy
tensorflow-cpu
gunicorn
```

#### Alternative approaches:

#### Option A: Use requirements_backup.txt

1. Rename requirements.txt to requirements_old.txt
2. Rename requirements_backup.txt to requirements.txt
3. Try different Python versions in runtime.txt:
   - python-3.10.13
   - python-3.9.18

#### Option B: Minimal deployment

Replace requirements.txt content with:

```
Flask
numpy
tensorflow-cpu
gunicorn
```

#### Option C: Alternative approach

If TensorFlow keeps failing, consider:

1. Using a simpler ML library (scikit-learn)
2. Converting model to ONNX format
3. Using TensorFlow Lite

### 4. Environment Variables (if needed)

In Render dashboard, add:

- TF_ENABLE_ONEDNN_OPTS=0 (to reduce TensorFlow warnings)

### 5. File Upload Considerations

- Render has file size limits
- fold1_model.keras should be < 100MB
- Consider using external storage for large models

### 6. Troubleshooting Common Issues:

- Build timeout: Use simpler requirements
- Memory issues: Use Free tier limitations
- Import errors: Check Python version compatibility

### 7. Alternative Platforms:

If Render fails:

- Heroku (similar setup)
- Railway
- PythonAnywhere
- Streamlit Cloud (requires app conversion)
