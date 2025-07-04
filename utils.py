from PIL import Image
import rembg

def remove_bg_and_merge(user_image_path, bg_path, output_path):
    with open(user_image_path, "rb") as inp_file:
        input_data = inp_file.read()
    output_data = rembg.remove(input_data)

    with open("temp.png", "wb") as out_file:
        out_file.write(output_data)

    person = Image.open("temp.png").convert("RGBA").resize((400, 600))
    background = Image.open(bg_path).convert("RGBA").resize((1080, 1350))

    background.paste(person, (340, 700), person)
    background.save(output_path)
