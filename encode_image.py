import base64
from io import BytesIO

def encode_figure_to_base64(figure):
    """
    Encode a matplotlib figure to a base64 string without saving to file.

    Args:
    figure (matplotlib.figure.Figure): The matplotlib figure to encode.

    Returns:
    str: The base64 encoded string representation of the image.
    """
    img_data = BytesIO()  # Create a buffer
    figure.savefig(img_data, format='png')  # Save figure to the buffer
    img_data.seek(0)  # Move to the start of the buffer
    return base64.b64encode(img_data.read()).decode('utf-8')  # Encode and return
