import os
import gc
import warnings
import numpy as np

# Suppress TensorFlow and protobuf warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['PYTHONHASHSEED'] = '0'
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf')

import tensorflow as tf
# Configure TensorFlow for memory efficiency
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)
from flask import Flask, request, render_template
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Conv1D, MaxPooling1D, Dense, Dropout,
    GlobalAveragePooling1D, GlobalMaxPooling1D,
    Activation, Multiply, Reshape, Add, Concatenate,
    BatchNormalization, Bidirectional, LSTM
)

def cbam_block(inputs, ratio=8):
    # --- Channel Attention ---
    channel = int(inputs.shape[-1])
    avg_pool = GlobalAveragePooling1D()(inputs)
    max_pool = GlobalMaxPooling1D()(inputs)
    shared_dense_1 = Dense(channel // ratio, activation='relu')
    shared_dense_2 = Dense(channel)
    avg_out = shared_dense_2(shared_dense_1(avg_pool))
    max_out = shared_dense_2(shared_dense_1(max_pool))
    channel_attention = Activation('sigmoid')(Add()([avg_out, max_out]))
    channel_attention = Reshape((1, channel))(channel_attention)
    x = Multiply()([inputs, channel_attention])

    # --- Spatial Attention ---
    avg_pool_spatial = tf.keras.layers.Lambda(
        lambda x: tf.reduce_mean(x, axis=-1, keepdims=True)
    )(x)
    max_pool_spatial = tf.keras.layers.Lambda(
        lambda x: tf.reduce_max(x, axis=-1, keepdims=True)
    )(x)
    concat = Concatenate(axis=-1)([avg_pool_spatial, max_pool_spatial])
    spatial_attention = Conv1D(1, kernel_size=7, padding='same', activation='sigmoid')(concat)
    out = Multiply()([x, spatial_attention])
    return out

def build_model_3x(input_shape=(9000, 1), num_classes=4):
    inputs = Input(shape=input_shape)
    x = Conv1D(64, 7, padding='same', activation='relu')(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling1D(2)(x)

    x = Conv1D(128, 5, padding='same', activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling1D(2)(x)

    x = cbam_block(x)

    x = Bidirectional(LSTM(64, return_sequences=True))(x)
    x = GlobalAveragePooling1D()(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)

    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-4),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

app = Flask(__name__)

# Global variable to hold model (lazy loading)
model = None
class_names = ["W", "N1+REM", "N2", "N3+N4"]

def load_model():
    """Load model only when needed to save memory"""
    global model
    if model is None:
        try:
            # Force garbage collection before loading
            gc.collect()
            
            # Build the model and load weights
            model = build_model_3x(input_shape=(9000, 1), num_classes=4)
            model.load_weights("fold1_model.keras")
            
            # Clear unnecessary data to save memory
            tf.keras.backend.clear_session()
            gc.collect()
            
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = "error"
    return model

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".npz"):
            npz = np.load(file)
            keys = npz.files  # names of arrays inside the .npz

            if "data" in keys:
                signal = npz["data"]
            elif len(keys) == 1:
                signal = npz[keys[0]]
            else:
                return render_template(
                    "index.html",
                    prediction=f"❌ .npz has keys {keys}. Use 'data' or a single array."
                )

            # Load model when needed
            current_model = load_model()
            if current_model == "error":
                return render_template(
                    "index.html",
                    prediction="❌ Model loading failed. Please try again later."
                )

            # Now check shape and reshape if necessary
            if signal.shape == (9000,):
                sig = signal.reshape(1, 9000, 1)
            elif signal.shape == (1, 9000, 1):
                sig = signal
            else:
                return render_template(
                    "index.html",
                    prediction=f"❌ Invalid shape {signal.shape}. Expected (9000,) or (1,9000,1)."
                )

            try:
                preds = current_model.predict(sig)
                idx = np.argmax(preds, axis=1)[0]
                prediction = class_names[idx]
            except Exception as e:
                prediction = f"❌ Prediction failed: {str(e)}"
        else:
            prediction = "❌ Please upload a valid .npz file."
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
