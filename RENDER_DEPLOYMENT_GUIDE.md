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
