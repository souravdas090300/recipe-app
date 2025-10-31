from io import BytesIO
import base64
import matplotlib.pyplot as plt
from .models import Recipe


def get_recipename_from_id(val):
    """Retrieve recipe name from recipe ID."""
    try:
        recipename = Recipe.objects.get(id=val)
        return recipename.name
    except Recipe.DoesNotExist:
        return "Unknown Recipe"


def get_graph():
    """Generate a graph as a base64-encoded string for HTML embedding.
    
    This function handles low-level image processing:
    - Creates a BytesIO buffer for the image
    - Saves the plot to the buffer as PNG
    - Encodes the image as base64
    - Returns the decoded string for HTML embedding
    """
    # Create a BytesIO buffer for the image
    buffer = BytesIO()
    
    # Save the plot to the buffer in PNG format
    plt.savefig(buffer, format='png')
    
    # Set cursor to the beginning of the stream
    buffer.seek(0)
    
    # Retrieve the content of the file
    image_png = buffer.getvalue()
    
    # Encode the bytes-like object to base64
    graph = base64.b64encode(image_png)
    
    # Decode to get the string as output
    graph = graph.decode('utf-8')
    
    # Free up the memory of buffer
    buffer.close()
    
    # Return the image/graph
    return graph


def get_chart(chart_type, data, **kwargs):
    """Generate a chart based on user input and data.
    
    Args:
        chart_type: String indicating chart type (#1=bar, #2=pie, #3=line)
        data: pandas DataFrame with recipe data
        **kwargs: Additional arguments like labels
        
    Returns:
        Base64-encoded string of the chart image
    """
    # Switch plot backend to AGG (Anti-Grain Geometry) for writing to file
    plt.switch_backend('AGG')
    
    # Clear any existing plots
    plt.clf()
    
    # Specify figure size
    fig = plt.figure(figsize=(8, 5))
    
    # Select chart type based on user input
    if chart_type == '#1':
        # Bar chart: recipes vs cooking time
        plt.bar(data['name'], data['cooking_time'], color='#3498db')
        plt.xlabel('Recipe Name', fontsize=12)
        plt.ylabel('Cooking Time (minutes)', fontsize=12)
        plt.title('Cooking Time by Recipe', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        
    elif chart_type == '#2':
        # Pie chart: distribution of recipes by difficulty
        labels = kwargs.get('labels')
        colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
        plt.pie(data['difficulty'].value_counts(), 
                labels=data['difficulty'].value_counts().index,
                autopct='%1.1f%%',
                colors=colors,
                startangle=90)
        plt.title('Recipe Distribution by Difficulty', fontsize=14, fontweight='bold')
        
    elif chart_type == '#3':
        # Line chart: cooking time trend
        plt.plot(data['name'], data['cooking_time'], 
                marker='o', 
                color='#9b59b6',
                linewidth=2,
                markersize=8)
        plt.xlabel('Recipe Name', fontsize=12)
        plt.ylabel('Cooking Time (minutes)', fontsize=12)
        plt.title('Cooking Time Trend', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
    else:
        print('Unknown chart type')
    
    # Specify layout details
    plt.tight_layout()
    
    # Render the graph to file
    chart = get_graph()
    return chart
