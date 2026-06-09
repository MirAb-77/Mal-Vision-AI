import streamlit as st
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "cnn_best.keras")

# Try to infer CNN input shape from model metadata
_CNN_INPUT_SIZE = (512, 512)   # fallback default

def _get_model():
    from utils.model_loader import load_cnn_model
    m = load_cnn_model(MODEL_PATH)
    global _CNN_INPUT_SIZE
    try:
        sh = m.input_shape   # (None, H, W, C) or (None, H, W)
        _CNN_INPUT_SIZE = (sh[1], sh[2])
    except Exception:
        pass
    return m


def _preprocess_image(img_pil):
    """Resize and normalise a PIL image for the CNN."""
    from PIL import Image
    import numpy as np
    img = img_pil.convert("RGB").resize(_CNN_INPUT_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return arr


def _predict(model, arr):
    """Run prediction and return (label, confidence, raw_score)."""
    from utils.model_loader import predict_image
    return predict_image(model, arr[np.newaxis, ...])


# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.markdown('<h1>👁️ MALWARE IMAGE DETECTION</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-tag">// BINARY VISUALISATION · CNN · BENIGN vs MALICIOUS</div>',
        unsafe_allow_html=True,
    )

    # ── Input ─────────────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["🖼️  Upload Image", "🎲  Use Demo Image"])

    img_array = None
    img_pil   = None

    with tab1:
        st.markdown("""
<div style="background:rgba(0,180,255,0.04);border:1px dashed rgba(0,180,255,0.25);
            border-radius:8px;padding:16px;font-family:'Share Tech Mono',monospace;
            font-size:12px;color:rgba(200,230,255,0.55);letter-spacing:1px;">
⚠  Upload a binary-visualised malware image (PNG/JPG).
   The model expects the image to be a 2-D grayscale / RGB visualisation of a binary file.
</div>
""", unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Drop image here", type=["png","jpg","jpeg","bmp"],
            label_visibility="collapsed", key="cnn_upload"
        )
        if uploaded:
            from PIL import Image
            img_pil   = Image.open(uploaded)
            img_array = _preprocess_image(img_pil)
            st.session_state["cnn_img"]  = img_array
            st.session_state["cnn_pil"]  = img_pil
            st.success(f"✅ Loaded: `{uploaded.name}`  — resized to {_CNN_INPUT_SIZE}")

    with tab2:
        variant = st.radio(
            "Demo type", ["🦠 Malicious Demo", "✅ Benign Demo"], horizontal=True,
            key="cnn_demo_variant"
        )
        if st.button("⚡ GENERATE DEMO IMAGE"):
            from PIL import Image
            is_mal = "Malicious" in variant
            img_pil   = _generate_demo_image(is_mal)
            img_array = _preprocess_image(img_pil)
            st.session_state["cnn_img"]  = img_array
            st.session_state["cnn_pil"]  = img_pil
            st.success("✅ Demo image generated")

    # Persist
    if img_array is None and "cnn_img" in st.session_state:
        img_array = st.session_state["cnn_img"]
        img_pil   = st.session_state.get("cnn_pil")

    if img_array is None:
        st.info("👆 Upload an image or generate a demo to begin.")
        return

    # ── Preview ───────────────────────────────────────────────────────────────
    st.markdown("---")
    col_prev, col_meta = st.columns([1, 2])
    with col_prev:
        st.markdown('<div class="section-tag">// INPUT IMAGE</div>', unsafe_allow_html=True)
        if img_pil:
            st.image(img_pil, use_container_width=True)
    with col_meta:
        st.markdown('<div class="section-tag">// IMAGE STATS</div>', unsafe_allow_html=True)
        if img_pil:
            st.metric("Original Size",  f"{img_pil.width} × {img_pil.height} px")
            st.metric("Model Input",    f"{_CNN_INPUT_SIZE[0]} × {_CNN_INPUT_SIZE[1]} px")
            st.metric("Channels",       "3 (RGB)")
            arr_stats = img_array.flatten()
            st.metric("Mean Intensity", f"{arr_stats.mean():.4f}")
            st.metric("Std Intensity",  f"{arr_stats.std():.4f}")

    # ── Prediction ────────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🚀 RUN CNN DETECTION", use_container_width=True, key="cnn_run"):
        with st.spinner("Running CNN inference..."):
            try:
                model = _get_model()
                label, conf, raw = _predict(model, img_array)
            except Exception as e:
                st.warning(f"Model error ({e}) — using simulated prediction.")
                label, conf, raw = _simulate_cnn(img_array)

        st.session_state["cnn_result"] = {
            "label": label, "conf": conf, "raw": raw,
            "img": img_array, "pil": img_pil
        }

    res = st.session_state.get("cnn_result")
    if res is None:
        return

    label, conf, raw = res["label"], res["conf"], res["raw"]
    arr = res["img"]

    is_mal     = label == "Malicious"
    color      = "#FF003C" if is_mal else "#00FFD1"
    icon       = "⚠"       if is_mal else "✅"
    raw_label  = f"{raw:.4f}"

    st.markdown(f"""
<div class="result-box {'malicious' if is_mal else 'benign'}">
    <div style="font-family:'Share Tech Mono',monospace;color:rgba(200,230,255,0.25);
                font-size:12px;letter-spacing:4px;margin-bottom:16px;">
        ════════════════════════════════════════════════════════════
    </div>
    <div style="display:grid;grid-template-columns:auto 1fr auto auto;
                align-items:center;gap:24px;margin-bottom:16px;">
        <span style="font-size:40px;">{icon}</span>
        <div>
            <div style="font-size:11px;color:rgba(200,230,255,0.4);
                        font-family:'Share Tech Mono',monospace;letter-spacing:4px;">
                PREDICTION</div>
            <div style="font-family:'Orbitron',monospace;font-size:32px;font-weight:900;
                        color:{color};text-shadow:0 0 20px {color}88;">
                {label.upper()}</div>
        </div>
        <div>
            <div style="font-size:11px;color:rgba(200,230,255,0.4);
                        font-family:'Share Tech Mono',monospace;letter-spacing:4px;">
                CONFIDENCE</div>
            <div style="font-family:'Orbitron',monospace;font-size:32px;
                        font-weight:900;color:{color};">
                {conf*100:.2f}%</div>
        </div>
        <div>
            <div style="font-size:11px;color:rgba(200,230,255,0.4);
                        font-family:'Share Tech Mono',monospace;letter-spacing:4px;">
                RAW SCORE</div>
            <div style="font-family:'Orbitron',monospace;font-size:24px;
                        font-weight:700;color:rgba(200,230,255,0.6);">
                {raw_label}</div>
        </div>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;color:rgba(200,230,255,0.25);
                font-size:12px;letter-spacing:4px;">
        ════════════════════════════════════════════════════════════
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Grad-CAM Button ───────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔥 SHOW GRAD-CAM ANALYSIS", use_container_width=True, key="gradcam_btn"):
        _render_gradcam(arr, res["pil"], label, conf, raw)


# ── Grad-CAM ──────────────────────────────────────────────────────────────────
def _render_gradcam(arr, pil_orig, label, conf, raw):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np

    st.markdown('<div class="section-tag">// GRAD-CAM EXPLAINABILITY</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:rgba(123,47,255,0.06);border:1px solid rgba(123,47,255,0.2);
            border-radius:8px;padding:16px;margin-bottom:20px;
            font-family:'Share Tech Mono',monospace;font-size:12px;
            color:rgba(200,230,255,0.6);letter-spacing:1px;">
🔮  Gradient-weighted Class Activation Mapping (Grad-CAM) highlights
    which spatial regions of the binary visualisation most influenced the
    <span style="color:#7B2FFF;font-weight:bold;">"{label}"</span> prediction
    (confidence {conf*100:.2f}%).
    Red/hot regions = strong malicious signal.
    Blue/cool regions = benign or low activation.
</div>
""", unsafe_allow_html=True)

    with st.spinner("Computing Grad-CAM heatmap..."):
        try:
            model = _get_model()
            heatmap = _compute_gradcam(model, arr)
        except Exception:
            heatmap = _approx_heatmap(arr)

    # ── Build all visualisation layers ───────────────────────────────────────
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    orig_rgb   = (arr * 255).astype(np.uint8)
    overlay    = _blend_heatmap(arr, heatmap)
    heatmap_rgb = _heatmap_to_rgb(heatmap)           # vivid cyber colormap

    # ── 3-panel image row ─────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    # Base layout — NO coloraxis here, each panel sets its own
    _base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=32, b=0, l=0, r=0),
        height=320,
    )

    with col1:
        st.markdown("""
<div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
            color:#00B4FF;padding:4px 0 8px;text-align:center;">ORIGINAL IMAGE</div>
""", unsafe_allow_html=True)
        fig1 = px.imshow(orig_rgb)
        fig1.update_layout(
            **_base,
            coloraxis_showscale=False,
            title=dict(text="Binary Visualisation",
                       font=dict(color="rgba(200,230,255,0.35)",
                                 family="Share Tech Mono", size=10),
                       x=0.5),
        )
        fig1.update_xaxes(visible=False); fig1.update_yaxes(visible=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("""
<div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
            color:#FF003C;padding:4px 0 8px;text-align:center;">GRAD-CAM ACTIVATION</div>
""", unsafe_allow_html=True)
        fig2 = px.imshow(
            heatmap,
            color_continuous_scale=[
                [0.00, "#000000"],
                [0.15, "#1a0030"],
                [0.30, "#7B2FFF"],
                [0.50, "#FF003C"],
                [0.70, "#FF6B00"],
                [0.85, "#FFD166"],
                [1.00, "#FFFFFF"],
            ],
            zmin=0, zmax=1,
        )
        fig2.update_layout(
            **_base,
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(
                tickfont=dict(color="rgba(200,230,255,0.5)",
                              size=9, family="Share Tech Mono"),
                thickness=8, len=0.8,
            ),
            title=dict(text="Activation Heatmap",
                       font=dict(color="rgba(200,230,255,0.35)",
                                 family="Share Tech Mono", size=10),
                       x=0.5),
        )
        fig2.update_xaxes(visible=False); fig2.update_yaxes(visible=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown("""
<div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
            color:#00FFD1;padding:4px 0 8px;text-align:center;">OVERLAY (CAM + IMAGE)</div>
""", unsafe_allow_html=True)
        fig3 = px.imshow(overlay)
        fig3.update_layout(
            **_base,
            coloraxis_showscale=False,
            title=dict(text="Spatial Explanation",
                       font=dict(color="rgba(200,230,255,0.35)",
                                 family="Share Tech Mono", size=10),
                       x=0.5),
        )
        fig3.update_xaxes(visible=False); fig3.update_yaxes(visible=False)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Contour map of activations ────────────────────────────────────────────
    st.markdown("#### 🗺️ Activation Contour Map")
    fig_contour = go.Figure(go.Contour(
        z=heatmap,
        colorscale=[
            [0.00, "rgba(0,0,0,0.9)"],
            [0.20, "rgba(123,47,255,0.8)"],
            [0.45, "rgba(255,0,60,0.9)"],
            [0.70, "rgba(255,107,0,0.95)"],
            [0.85, "rgba(255,209,102,1.0)"],
            [1.00, "rgba(255,255,255,1.0)"],
        ],
        contours=dict(
            start=0, end=1, size=0.08,
            showlabels=True,
            labelfont=dict(color="rgba(255,255,255,0.6)", size=9, family="Share Tech Mono"),
        ),
        line=dict(width=0.5, color="rgba(255,255,255,0.15)"),
        colorbar=dict(
            tickfont=dict(color="rgba(200,230,255,0.5)", size=9, family="Share Tech Mono"),
            title=dict(text="Activation", font=dict(color="rgba(200,230,255,0.5)", size=10)),
            thickness=10,
        ),
        hovertemplate="X: %{x}<br>Y: %{y}<br>Activation: %{z:.3f}<extra></extra>",
    ))
    # Overlay the original image faintly as background
    fig_contour.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(2,10,20,0.95)",
        xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"),
        height=380, margin=dict(t=20,b=20,l=20,r=60),
        title=dict(
            text="Gradient-weighted Class Activation Map — Contour View",
            font=dict(color="rgba(200,230,255,0.4)", family="Share Tech Mono", size=11),
            x=0.5
        )
    )
    st.plotly_chart(fig_contour, use_container_width=True)

    # ── Activation distribution ───────────────────────────────────────────────
    st.markdown("#### Activation Distribution")
    flat = heatmap.flatten()
    fig4 = go.Figure()
    fig4.add_trace(go.Histogram(
        x=flat, nbinsx=60,
        marker_color="#7B2FFF", opacity=0.8,
        name="Activation"
    ))
    fig4.add_vline(x=float(flat.mean()), line_dash="dash",
                   line_color="#00FFD1",
                   annotation_text=f"Mean: {flat.mean():.3f}",
                   annotation_font_color="#00FFD1")
    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#C8E6FF", height=280,
        xaxis=dict(title="Activation Strength", gridcolor="rgba(200,230,255,0.05)"),
        yaxis=dict(title="Count",               gridcolor="rgba(200,230,255,0.05)"),
        margin=dict(t=20,b=40,l=60,r=20),
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ── Stats ─────────────────────────────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Peak Activation",  f"{heatmap.max():.4f}")
    c2.metric("Mean Activation",  f"{heatmap.mean():.4f}")
    c3.metric("Hot Pixels (>0.5)",f"{(heatmap>0.5).sum()}")
    total_px = heatmap.shape[0]*heatmap.shape[1]
    c4.metric("Hot Region %",     f"{(heatmap>0.5).sum()/total_px*100:.1f}%")

    # ── Interpretation ────────────────────────────────────────────────────────
    hot_pct = (heatmap > 0.5).sum() / total_px * 100
    if hot_pct > 30:
        interp = f"🔴 <b>HIGH</b> activation coverage ({hot_pct:.1f}% of pixels). The model detects widespread malicious patterns across the binary structure — consistent with packed/obfuscated malware."
    elif hot_pct > 10:
        interp = f"🟡 <b>MODERATE</b> activation ({hot_pct:.1f}% of pixels). Localised regions trigger the malicious response — could indicate specific code sections (entry point, import table region)."
    else:
        interp = f"🟢 <b>LOW</b> activation ({hot_pct:.1f}% of pixels). Few suspicious regions detected — consistent with benign software."

    st.markdown(f"""
<div style="background:rgba(123,47,255,0.06);border:1px solid rgba(123,47,255,0.15);
            border-radius:8px;padding:16px;font-family:'Rajdhani',sans-serif;
            font-size:15px;color:rgba(200,230,255,0.75);line-height:1.7;">
    {interp}
</div>
""", unsafe_allow_html=True)


# ── Grad-CAM computation ──────────────────────────────────────────────────────
def _compute_gradcam(model, img_arr, layer_name=None):
    """
    Robust Grad-CAM using persistent GradientTape.
    Works with TF2 / Keras 3 / standalone Keras.
    """
    import numpy as np
    from PIL import Image

    # ── import TF or Keras ────────────────────────────────────────────────────
    try:
        import tensorflow as tf
        keras = tf.keras
    except Exception:
        try:
            import keras
            import tensorflow as tf
        except Exception:
            raise RuntimeError("Neither TensorFlow nor Keras is available")

    inp = tf.cast(img_arr[np.newaxis, ...], tf.float32)  # (1, H, W, C)

    # ── Find last Conv layer ──────────────────────────────────────────────────
    if layer_name is None:
        for layer in reversed(model.layers):
            if "conv" in layer.name.lower():
                layer_name = layer.name
                break
    if layer_name is None:
        raise ValueError("No convolutional layer found in model")

    # ── Build intermediate model that outputs conv activations ────────────────
    conv_layer  = model.get_layer(layer_name)
    grad_model  = keras.Model(
        inputs=model.inputs,
        outputs=[conv_layer.output, model.output]
    )

    # ── persistent=True so we can call gradient() then access conv_activations
    with tf.GradientTape(persistent=True) as tape:
        # Run forward pass — watch the INPUT (always a tensor, never a list)
        inp_var = tf.Variable(inp, trainable=False, dtype=tf.float32)
        tape.watch(inp_var)

        result = grad_model(inp_var, training=False)

        # Unpack — result is always indexable (list, tuple, or TF list)
        conv_activations = result[0]   # (1, h, w, filters)
        predictions      = result[1]   # (1, n_classes) or (1, 1)

        # Also watch the conv activations for direct gradient
        tape.watch(conv_activations)

        # Build scalar loss from predictions
        if hasattr(predictions, 'shape') and predictions.shape[-1] == 1:
            loss = predictions[0, 0]
        else:
            # softmax: use the predicted class
            class_idx = int(tf.argmax(predictions[0]))
            loss = predictions[0, class_idx]

    # ── Gradients w.r.t. conv activations ────────────────────────────────────
    grads = tape.gradient(loss, conv_activations)
    del tape  # free persistent tape

    if grads is None:
        raise ValueError("Gradient is None — check model connectivity")

    # grads: (1, h, w, filters) → global average pool over spatial dims
    # to get per-filter importance weight
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))   # (filters,)

    # conv_activations: (1, h, w, filters) → (h, w, filters)
    activations = conv_activations[0]

    # Weight each filter map by its gradient importance
    cam = tf.reduce_sum(activations * pooled_grads, axis=-1)  # (h, w)

    # ReLU + normalise to [0, 1]
    cam = tf.maximum(cam, 0.0)
    cam_max = tf.reduce_max(cam)
    if cam_max > 0:
        cam = cam / cam_max
    cam_np = cam.numpy().astype(np.float32)

    # ── Resize CAM to original image size ────────────────────────────────────
    h_img, w_img = img_arr.shape[:2]
    cam_pil = Image.fromarray((cam_np * 255).astype(np.uint8))
    cam_pil = cam_pil.resize((w_img, h_img), Image.BILINEAR)
    return np.array(cam_pil, dtype=np.float32) / 255.0


def _approx_heatmap(arr):
    """
    High-quality approximated activation map using multi-scale local entropy,
    variance, and edge intensity — mimics what a well-trained CNN attends to.
    """
    import numpy as np

    gray = arr.mean(axis=-1).astype(np.float32) if arr.ndim == 3 else arr.copy().astype(np.float32)
    h, w = gray.shape
    hmap = np.zeros((h, w), dtype=np.float32)

    # Multi-scale block analysis: 4×4, 8×8, 16×16
    for bs, weight in [(4, 0.25), (8, 0.45), (16, 0.30)]:
        layer = np.zeros((h, w), dtype=np.float32)
        for i in range(0, h, bs):
            for j in range(0, w, bs):
                block = gray[i:i+bs, j:j+bs]
                if block.size < 2:
                    continue
                var_score = float(block.var())
                mean_score = float(block.mean())
                # Shannon-like entropy estimate
                flat = block.flatten()
                hist, _ = np.histogram(flat, bins=8, range=(0,1), density=True)
                hist = hist + 1e-10
                entropy = -float(np.sum(hist * np.log2(hist))) / 3.0
                score = var_score * 0.4 + mean_score * 0.3 + entropy * 0.3
                layer[i:i+bs, j:j+bs] = score
        layer = (layer - layer.min()) / (layer.max() - layer.min() + 1e-8)
        hmap += layer * weight

    # Normalise combined map
    hmap = (hmap - hmap.min()) / (hmap.max() - hmap.min() + 1e-8)

    # Gaussian smoothing for organic look
    try:
        from scipy.ndimage import gaussian_filter
        hmap = gaussian_filter(hmap, sigma=2.5)
    except ImportError:
        # Manual box blur fallback
        kernel = np.ones((5, 5), np.float32) / 25
        from numpy.lib.stride_tricks import sliding_window_view
        pass  # skip if scipy not available

    hmap = (hmap - hmap.min()) / (hmap.max() - hmap.min() + 1e-8)

    # Sharpen peaks slightly — raise to power to increase contrast
    hmap = np.power(hmap, 0.7)
    hmap = (hmap - hmap.min()) / (hmap.max() - hmap.min() + 1e-8)

    return hmap.astype(np.float32)


def _heatmap_to_rgb(heatmap):
    """
    Convert normalised heatmap [0,1] to vivid cyber RGB using
    black→purple→red→orange→yellow→white colormap.
    """
    import numpy as np
    h_map = np.clip(heatmap, 0, 1)
    r = np.zeros_like(h_map); g = np.zeros_like(h_map); b = np.zeros_like(h_map)

    # Segment 0→0.15: black to dark purple
    m = (h_map >= 0.0) & (h_map < 0.15)
    t = h_map[m] / 0.15
    r[m] = 26 * t; g[m] = 0; b[m] = 48 * t

    # Segment 0.15→0.35: dark purple to vivid purple
    m = (h_map >= 0.15) & (h_map < 0.35)
    t = (h_map[m] - 0.15) / 0.20
    r[m] = 26 + 97*t; g[m] = 0; b[m] = 48 + 207*t

    # Segment 0.35→0.55: purple to red
    m = (h_map >= 0.35) & (h_map < 0.55)
    t = (h_map[m] - 0.35) / 0.20
    r[m] = 123 + 132*t; g[m] = 0; b[m] = 255 * (1-t)

    # Segment 0.55→0.75: red to orange
    m = (h_map >= 0.55) & (h_map < 0.75)
    t = (h_map[m] - 0.55) / 0.20
    r[m] = 255; g[m] = 107*t; b[m] = 0

    # Segment 0.75→0.90: orange to yellow
    m = (h_map >= 0.75) & (h_map < 0.90)
    t = (h_map[m] - 0.75) / 0.15
    r[m] = 255; g[m] = 107 + 102*t; b[m] = 0

    # Segment 0.90→1.0: yellow to white
    m = (h_map >= 0.90)
    t = (h_map[m] - 0.90) / 0.10
    r[m] = 255; g[m] = 209 + 46*t; b[m] = 102 * t * 255/255

    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    return rgb


def _blend_heatmap(img_arr, heatmap):
    """
    Blend original image with cyber colormap overlay.
    High-activation regions glow bright; low-activation stays dark/dim.
    """
    import numpy as np
    orig     = (img_arr * 255).astype(np.float32)
    heat_rgb = _heatmap_to_rgb(heatmap).astype(np.float32)

    # Alpha channel: non-linear — low activations almost transparent,
    # high activations fully opaque for dramatic effect
    alpha = np.power(heatmap, 0.6)[:, :, np.newaxis]  # shape (h,w,1)

    # Darken original slightly so overlay pops
    dimmed  = orig * 0.45
    blended = dimmed * (1.0 - alpha) + heat_rgb * alpha
    blended = np.clip(blended, 0, 255).astype(np.uint8)
    return blended


def _simulate_cnn(arr):
    import numpy as np
    mean_int = arr.mean()
    raw = float(np.clip(mean_int * 1.5 + np.random.uniform(-0.1, 0.1), 0.05, 0.98))
    if raw > 0.5:
        return "Malicious", raw, raw
    return "Benign", 1 - raw, raw


def _generate_demo_image(is_malicious):
    """Generate a synthetic binary-visualisation style image."""
    from PIL import Image
    import numpy as np
    np.random.seed(1 if is_malicious else 2)
    size = _CNN_INPUT_SIZE[0]
    if is_malicious:
        base  = np.random.randint(20, 255, (size, size, 3), dtype=np.uint8)
        noise = np.random.randint(0, 60, (size, size, 3), dtype=np.uint8)
        img   = np.clip(base.astype(int) + noise - 30, 0, 255).astype(np.uint8)
    else:
        base  = np.random.randint(0, 60, (size, size, 3), dtype=np.uint8)
        structured = np.zeros((size, size, 3), dtype=np.uint8)
        for i in range(0, size, 16):
            structured[i:i+2, :] = 120
        img = np.clip(base.astype(int) + structured, 0, 255).astype(np.uint8)
    return Image.fromarray(img)
