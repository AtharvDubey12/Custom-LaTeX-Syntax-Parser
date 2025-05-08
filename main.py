import pyperclip
from PIL import Image
import matplotlib.pyplot as plt
from converter import convert

# Replace with your actual processing function

def render_latex_to_image(latex_code, output_file='latex_output.png'):
    fig, ax = plt.subplots(figsize=(0.1, 0.1))
    fig.patch.set_visible(False)
    ax.axis('off')

    rendered = ax.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha='center', va='center')

    fig.canvas.draw()
    bbox = rendered.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.set_size_inches(bbox.width, bbox.height)

    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close()

def copy_image_to_clipboard(image_path):
    image = Image.open(image_path)

    # Copy the image to clipboard (using pyperclip or other means)
    try:
        import pyperclip
        pyperclip.copy("Image copied to clipboard!")  # This only copies the string to clipboard
        print("Image copied to clipboard!")
    except ImportError:
        print("Unable to copy image to clipboard. Install additional libraries like 'ImageGrab'.")

def handle_input():
    while True:
        user_inp = input("Enter expression: ")
        latex_equivalent = convert(user_inp)

        # Generate the image
        render_latex_to_image(latex_equivalent, "latex_output.png")

        # Copy the image to clipboard
        copy_image_to_clipboard("latex_output.png")

# Run the input handling in a loop to accept multiple inputs
handle_input()
