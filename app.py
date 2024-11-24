from flask import Flask, request, render_template
import re
import os

app = Flask(__name__)

# List of predefined countries, colors, shapes, and styles
countries_list = [
    "India", "USA", "China", "Germany", "France", "Japan", "Italy", "UK", "Canada", "Australia"
]

colors_list = [
    "red", "blue", "green", "yellow", "black", "white", "gray", "purple", "pink", "orange", "brown", "beige"
]

shapes_list = [
    "round", "square", "rectangle", "oval", "triangle", "hexagon", "octagon"
]

styles_list = [
    "modern", "antique", "classy", "vintage", "contemporary", "rustic", "minimalistic", "traditional"
]

# Function to extract price from the caption
def extract_price(caption):
    price_match = re.search(r'₹([\d,]+)', caption)  # Searching for ₹ symbol followed by numbers (with commas)
    if price_match:
        price_str = price_match.group(1)
        price_str = price_str.replace(',', '')  # Remove commas for proper price extraction
        return '₹' + price_str
    return "  "

# Function to extract country from the caption (case-insensitive)
def extract_country(caption):
    caption = caption.lower()  # Convert caption to lowercase for case-insensitive comparison
    for country in countries_list:
        if country.lower() in caption:
            return country
    return "  "

# Function to extract color from the caption
def extract_color(caption):
    caption = caption.lower()
    for color in colors_list:
        if color in caption:
            return color.capitalize()  # Capitalize the color for consistency
    return "  "

# Function to extract shape from the caption
def extract_shape(caption):
    caption = caption.lower()
    for shape in shapes_list:
        if shape in caption:
            return shape.capitalize()  # Capitalize the shape for consistency
    return "  "

# Function to extract style from the caption
def extract_style(caption):
    caption = caption.lower()
    for style in styles_list:
        if style in caption:
            return style.capitalize()  # Capitalize the style for consistency
    return "  "

# Route to display the upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to process the uploaded image and caption
@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files or 'caption' not in request.form:
        return "No image or caption provided", 400
    
    image = request.files['image']
    caption = request.form['caption']

    # Save the uploaded image to the 'uploads' folder
    image_path = os.path.join('static', 'uploads', image.filename)
    image.save(image_path)

    # Extract details
    price = extract_price(caption)
    country = extract_country(caption)
    color = extract_color(caption)
    shape = extract_shape(caption)
    style = extract_style(caption)

    product_listing = {
        "image": image.filename,
        "description": caption,
        "price": price,
        "country_of_origin": country,
        "color": color,
        "shape": shape,
        "style": style
    }

    return render_template('index.html', result=product_listing)

if __name__ == '__main__':
    # Create 'uploads' folder if it doesn't exist
    if not os.path.exists(os.path.join('static', 'uploads')):
        os.makedirs(os.path.join('static', 'uploads'))
    
    app.run(debug=True)
