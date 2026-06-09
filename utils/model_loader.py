import joblib
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore")

# ── Feature list (75 features) ──────────────────────────────────────────────
PE_FEATURES = [
    "e_magic","e_cblp","e_cp","e_crlc","e_cparhdr","e_minalloc","e_maxalloc",
    "e_ss","e_sp","e_csum","e_ip","e_cs","e_lfarlc","e_ovno","e_oemid",
    "e_oeminfo","e_lfanew","NumberOfSections","PointerToSymbolTable",
    "NumberOfSymbols","SizeOfOptionalHeader","Characteristics","Magic",
    "MajorLinkerVersion","MinorLinkerVersion","SizeOfCode",
    "SizeOfInitializedData","SizeOfUninitializedData","AddressOfEntryPoint",
    "BaseOfCode","ImageBase","SectionAlignment","FileAlignment",
    "MajorOperatingSystemVersion","MinorOperatingSystemVersion",
    "MajorImageVersion","MinorImageVersion","MajorSubsystemVersion",
    "MinorSubsystemVersion","SizeOfHeaders","CheckSum","SizeOfImage",
    "Subsystem","DllCharacteristics","SizeOfStackReserve","SizeOfStackCommit",
    "SizeOfHeapReserve","SizeOfHeapCommit","LoaderFlags","NumberOfRvaAndSizes",
    "SuspiciousImportFunctions","SuspiciousNameSection","SectionsLength",
    "SectionMinEntropy","SectionMaxEntropy","SectionMinRawsize",
    "SectionMaxRawsize","SectionMinVirtualsize","SectionMaxVirtualsize",
    "SectionMaxPhysical","SectionMinPhysical","SectionMaxVirtual",
    "SectionMinVirtual","SectionMaxPointerData","SectionMinPointerData",
    "SectionMaxChar","SectionMainChar","DirectoryEntryImport",
    "DirectoryEntryImportSize","DirectoryEntryExport",
    "ImageDirectoryEntryExport","ImageDirectoryEntryImport",
    "ImageDirectoryEntryResource","ImageDirectoryEntryException",
    "ImageDirectoryEntrySecurity",
]

# ── CNN class labels ─────────────────────────────────────────────────────────
CNN_CLASSES = ["Benign", "Malicious"]

_pe_model  = None
_cnn_model = None

def load_pe_model(model_path="models/pe_model.pkl"):
    global _pe_model
    if _pe_model is not None:
        return _pe_model
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _pe_model = joblib.load(model_path)
        return _pe_model
    except Exception as e:
        raise RuntimeError(f"Could not load PE model: {e}")

def load_cnn_model(model_path="models/cnn_best.keras"):
    global _cnn_model
    if _cnn_model is not None:
        return _cnn_model
    try:
        # Try keras / tf.keras
        try:
            import keras
            _cnn_model = keras.models.load_model(model_path)
        except ImportError:
            import tensorflow as tf
            _cnn_model = tf.keras.models.load_model(model_path)
        return _cnn_model
    except Exception as e:
        raise RuntimeError(f"Could not load CNN model: {e}")

# ── PE prediction ─────────────────────────────────────────────────────────────
import numpy as np

def predict_pe(model, feature_vector):
    """
    Clean + stable prediction wrapper
    Works for:
    - RandomForest
    - XGBoost
    - Sklearn classifiers with predict_proba
    """

    X = np.array(feature_vector, dtype=float).reshape(1, -1)

    proba = model.predict_proba(X)[0]   # [benign, malicious]

    benign_score = float(proba[0])
    malicious_score = float(proba[1])

    # Smooth confidence (prevents fake 99.9% outputs)
    confidence = max(benign_score, malicious_score)

    label = "Malicious" if malicious_score > benign_score else "Benign"

    return label, confidence, np.array([benign_score, malicious_score])

# ── CNN prediction ────────────────────────────────────────────────────────────
def predict_image(model, img_array: np.ndarray):
    """
    img_array: preprocessed numpy array ready for the model.
    Returns (label, confidence, raw_score)
    """
    preds = model.predict(img_array, verbose=0)

    if preds.shape[-1] == 1:
        # Sigmoid output
        raw   = float(preds[0][0])
        label = CNN_CLASSES[int(raw > 0.5)]
        conf  = raw if raw > 0.5 else 1 - raw
    else:
        # Softmax output
        idx   = int(np.argmax(preds[0]))
        raw   = float(preds[0][idx])
        label = CNN_CLASSES[idx] if idx < len(CNN_CLASSES) else str(idx)
        conf  = raw

    return label, conf, float(preds[0][0]) if preds.shape[-1] == 1 else float(preds[0][1])

def get_dummy_pe_features(variant="malicious"):
    """
    Generate realistic synthetic PE features.
    Every call returns a different sample.
    """

    import numpy as np

    rng = np.random.default_rng()

    if variant == "malicious":

        base = {
            "e_magic": 23117,
            "e_cblp": rng.integers(120, 200),
            "e_cp": rng.integers(3, 8),
            "e_crlc": 0,
            "e_cparhdr": 4,
            "e_minalloc": 0,
            "e_maxalloc": 65535,
            "e_ss": 0,
            "e_sp": rng.integers(150, 250),
            "e_csum": 0,
            "e_ip": 0,
            "e_cs": 0,
            "e_lfarlc": 64,
            "e_ovno": 0,
            "e_oemid": 0,
            "e_oeminfo": 0,

            "e_lfanew": rng.integers(128, 512),

            "NumberOfSections": rng.integers(5, 12),

            "PointerToSymbolTable": 0,
            "NumberOfSymbols": 0,

            "SizeOfOptionalHeader": 224,
            "Characteristics": rng.choice([258, 290, 8462]),

            "Magic": 267,

            "MajorLinkerVersion": rng.integers(10, 15),
            "MinorLinkerVersion": 0,

            "SizeOfCode": rng.integers(300000, 3000000),
            "SizeOfInitializedData": rng.integers(100000, 2500000),
            "SizeOfUninitializedData": 0,

            "AddressOfEntryPoint": rng.integers(100000, 2000000),

            "BaseOfCode": 4096,
            "ImageBase": 4194304,

            "SectionAlignment": 4096,
            "FileAlignment": 512,

            "MajorOperatingSystemVersion": 6,
            "MinorOperatingSystemVersion": 0,

            "MajorImageVersion": 0,
            "MinorImageVersion": 0,

            "MajorSubsystemVersion": 6,
            "MinorSubsystemVersion": 0,

            "SizeOfHeaders": rng.choice([512, 1024]),

            "CheckSum": rng.integers(0, 2000),

            "SizeOfImage": rng.integers(1000000, 6000000),

            "Subsystem": 2,

            "DllCharacteristics": rng.choice([
                33088, 33120, 33216, 33280
            ]),

            "SizeOfStackReserve": 1048576,
            "SizeOfStackCommit": 8192,

            "SizeOfHeapReserve": 1048576,
            "SizeOfHeapCommit": 4096,

            "LoaderFlags": 0,
            "NumberOfRvaAndSizes": 16,

            "SuspiciousImportFunctions": rng.integers(4, 15),

            "SuspiciousNameSection": rng.integers(1, 6),

            "SectionsLength": rng.integers(5, 12),

            "SectionMinEntropy": rng.uniform(0.0, 1.5),
            "SectionMaxEntropy": rng.uniform(7.0, 8.6),

            "SectionMinRawsize": rng.integers(128, 1024),
            "SectionMaxRawsize": rng.integers(500000, 3000000),

            "SectionMinVirtualsize": rng.integers(1, 50),
            "SectionMaxVirtualsize": rng.integers(400000, 3000000),

            "SectionMaxPhysical": rng.integers(500000, 3000000),
            "SectionMinPhysical": rng.integers(128, 1024),

            "SectionMaxVirtual": rng.integers(500000, 3000000),
            "SectionMinVirtual": rng.integers(1, 50),

            "SectionMaxPointerData": rng.integers(500000, 3000000),
            "SectionMinPointerData": rng.integers(512, 4096),

            "SectionMaxChar": 1610612768,
            "SectionMainChar": 1610612768,

            "DirectoryEntryImport": rng.integers(4, 12),
            "DirectoryEntryImportSize": rng.integers(80, 500),

            "DirectoryEntryExport": rng.choice([0, 1]),

            "ImageDirectoryEntryExport": rng.integers(0, 1000),
            "ImageDirectoryEntryImport": rng.integers(4, 12),

            "ImageDirectoryEntryResource": rng.integers(1, 10),

            "ImageDirectoryEntryException": 0,

            "ImageDirectoryEntrySecurity": rng.choice([0, 0, 0, 1]),
        }

    else:

        base = {
            "e_magic": 23117,
            "e_cblp": rng.integers(80, 120),
            "e_cp": rng.integers(2, 5),
            "e_crlc": 0,
            "e_cparhdr": 4,
            "e_minalloc": 0,
            "e_maxalloc": 65535,
            "e_ss": 0,
            "e_sp": 184,
            "e_csum": 0,
            "e_ip": 0,
            "e_cs": 0,
            "e_lfarlc": 64,
            "e_ovno": 0,
            "e_oemid": 0,
            "e_oeminfo": 0,

            "e_lfanew": rng.integers(128, 256),

            "NumberOfSections": rng.integers(3, 6),

            "PointerToSymbolTable": 0,
            "NumberOfSymbols": 0,

            "SizeOfOptionalHeader": 224,

            "Characteristics": rng.choice([34, 258]),

            "Magic": 267,

            "MajorLinkerVersion": rng.integers(12, 15),
            "MinorLinkerVersion": 0,

            "SizeOfCode": rng.integers(10000, 80000),
            "SizeOfInitializedData": rng.integers(5000, 50000),
            "SizeOfUninitializedData": 0,

            "AddressOfEntryPoint": rng.integers(4000, 20000),

            "BaseOfCode": 4096,
            "ImageBase": 4194304,

            "SectionAlignment": 4096,
            "FileAlignment": 512,

            "MajorOperatingSystemVersion": 6,
            "MinorOperatingSystemVersion": 0,

            "MajorImageVersion": 0,
            "MinorImageVersion": 0,

            "MajorSubsystemVersion": 6,
            "MinorSubsystemVersion": 0,

            "SizeOfHeaders": 512,

            "CheckSum": rng.integers(15000, 60000),

            "SizeOfImage": rng.integers(20000, 100000),

            "Subsystem": 2,

            "DllCharacteristics": rng.choice([
                33344, 33280, 34000
            ]),

            "SizeOfStackReserve": 1048576,
            "SizeOfStackCommit": 4096,

            "SizeOfHeapReserve": 1048576,
            "SizeOfHeapCommit": 4096,

            "LoaderFlags": 0,
            "NumberOfRvaAndSizes": 16,

            "SuspiciousImportFunctions": rng.integers(0, 2),

            "SuspiciousNameSection": 0,

            "SectionsLength": rng.integers(3, 5),

            "SectionMinEntropy": rng.uniform(0.8, 2.5),
            "SectionMaxEntropy": rng.uniform(4.5, 6.5),

            "SectionMinRawsize": rng.integers(256, 1024),
            "SectionMaxRawsize": rng.integers(10000, 50000),

            "SectionMinVirtualsize": rng.integers(50, 500),
            "SectionMaxVirtualsize": rng.integers(10000, 50000),

            "SectionMaxPhysical": rng.integers(10000, 50000),
            "SectionMinPhysical": rng.integers(256, 1024),

            "SectionMaxVirtual": rng.integers(10000, 50000),
            "SectionMinVirtual": rng.integers(50, 500),

            "SectionMaxPointerData": rng.integers(5000, 50000),
            "SectionMinPointerData": rng.integers(512, 1024),

            "SectionMaxChar": 1073741888,
            "SectionMainChar": 1610612736,

            "DirectoryEntryImport": rng.integers(1, 4),
            "DirectoryEntryImportSize": rng.integers(20, 80),

            "DirectoryEntryExport": 0,

            "ImageDirectoryEntryExport": 0,
            "ImageDirectoryEntryImport": rng.integers(1, 4),

            "ImageDirectoryEntryResource": rng.integers(1, 3),

            "ImageDirectoryEntryException": 0,

            "ImageDirectoryEntrySecurity": rng.choice([0, 1]),
        }

    return np.array(
        [base.get(feature, 0) for feature in PE_FEATURES],
        dtype=np.float64
    )
