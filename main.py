import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import cv2
from PIL import Image

st.title("クリックして囲んだ領域のピクセル数を取得")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    # 画像が大きい場合のサイズ調整
    max_width = 700
    scale_ratio = min(max_width / image.width, 1)
    display_width = int(image.width * scale_ratio)
    display_height = int(image.height * scale_ratio)

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=4,
        stroke_color="#FF0000",
        background_image=image,
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="polygon",
        display_toolbar=True,
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            mask = np.zeros(img_array.shape[:2], dtype=np.uint8)

            for obj in objects:
                if obj["type"] == "path":
                    points = obj["path"]
                    poly_points = []
                    for p in points:
                        if len(p) == 3:
                            _, x, y = p
                            x_orig = int(x / scale_ratio)
                            y_orig = int(y / scale_ratio)
                            poly_points.append([x_orig, y_orig])
                    poly_points = np.array([poly_points], dtype=np.int32)
                    cv2.fillPoly(mask, poly_points, 255)

            pixel_count = cv2.countNonZero(mask)

            st.success(f"✅ 囲った領域のピクセル数: **{pixel_count} ピクセル**")
            st.image(mask, caption="領域マスク画像", use_column_width=True)
