import os
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, render_template, url_for, redirect, flash

os.makedirs("uploads", exist_ok=True)
os.makedirs("generated", exist_ok=True)
OUTPUT_FOLDER = "generated"

UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "naj_ostane_prazno"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

font_path = "fonts\Anton-Regular.ttf"
font_size = 20
font = ImageFont.truetype(font_path, font_size)


def render_meme(img, top_text, bottom_text):
    draw = ImageDraw.Draw(img)

    def draw_text_with_outline(text, y_pos, max_width_ratio=0.9):
        # Startna velikost fonta
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]

        # zmanjsa font ko tekst ne stane
        while w > img.width * max_width_ratio and font_size > 10:
            font_size -= 2
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]

        h = bbox[3] - bbox[1]
        x = (img.width - w) / 2

        # outline
        outline_range = max(1, font_size // 15)
        for ox in range(-outline_range, outline_range+1):
            for oy in range(-outline_range, outline_range+1):
                if ox != 0 or oy != 0:
                    draw.text((x+ox, y_pos+oy), text, font=font, fill="black")

        # main text
        draw.text((x, y_pos), text, font=font, fill="white")
        return h

    if top_text:
        draw_text_with_outline(top_text, y_pos=10)

    if bottom_text:
        h = draw_text_with_outline(
            bottom_text, y_pos=img.height - 10 - font_size)

    output_path = os.path.join(UPLOAD_FOLDER, "meme.png")
    img.save(output_path)
    return output_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            flash("Slika ne obstaja")
            return redirect(request.url)
        file = request.files["image"]
        top_text = request.form.get("top_text", "")
        bottom_text = request.form.get("bottom_text", "")
        if file.filename == "":
            flash("Fajl ni izbran")
            return redirect(request.url)
        try:
            img = Image.open(file.stream)
        except Exception as e:
            flash("Napaka pri odpiranju slike: " + str(e))
            return redirect(request.url)

        out_path = render_meme(img, top_text, bottom_text)
        filename = os.path.basename(out_path)
        return render_template("res.html", meme_url=url_for('static', filename=f'uploads/{filename}'))
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
    # 0.0.0.0 za lan
