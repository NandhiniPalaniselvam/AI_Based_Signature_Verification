import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# =========================================================
# SETTINGS
# =========================================================

DATASET_PATH = "dataset/person_1"
IMG_SIZE = 128

# =========================================================
# LOAD IMAGES
# =========================================================

images = []
labels = []

genuine_path = os.path.join(DATASET_PATH, "genuine")
forged_path = os.path.join(DATASET_PATH, "forged")


def load_images(folder, label):
    for filename in os.listdir(folder):

        file_path = os.path.join(folder, filename)

        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Could not read:", file_path)
            continue

        # Resize
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

        # Normalize
        image = image.astype("float32") / 255.0

        images.append(image)
        labels.append(label)


# Genuine = 0
# Forged  = 1

load_images(genuine_path, 0)
load_images(forged_path, 1)

# =========================================================
# CONVERT DATA
# =========================================================

X = np.array(images)
y = np.array(labels)

# Add channel dimension
X = X.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

# One-hot encoding
y = to_categorical(y, num_classes=2)

print("Total images:", len(X))

# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
    stratify=np.argmax(y, axis=1)
)

print("Training images:", len(X_train))
print("Testing images:", len(X_test))

# =========================================================
# CNN MODEL
# =========================================================

model = Sequential([

    Conv2D(
        32,
        (3, 3),
        activation="relu",
        input_shape=(IMG_SIZE, IMG_SIZE, 1)
    ),

    MaxPooling2D((2, 2)),

    Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    MaxPooling2D((2, 2)),

    Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    MaxPooling2D((2, 2)),

    Flatten(),

    Dense(128, activation="relu"),

    Dropout(0.5),

    Dense(2, activation="softmax")
])

# =========================================================
# COMPILE
# =========================================================

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================================================
# TRAIN
# =========================================================

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=8
)

# =========================================================
# EVALUATE
# =========================================================

loss, accuracy = model.evaluate(X_test, y_test)

print("\nTest Accuracy:", accuracy * 100, "%")

# =========================================================
# SAVE MODEL
# =========================================================

os.makedirs("model", exist_ok=True)

model.save("model/signature_model.h5")

print("\nModel saved successfully!")
print("Location: model/signature_model.h5")