"""
Recipe App Utilities Module

This module provides utility functions for the Recipe application,
primarily for data visualization and chart generation.

Functions:
    get_recipename_from_id: Retrieve recipe name from database by ID
    get_graph: Convert matplotlib plot to base64 string for HTML embedding
    get_chart: Generate data visualization charts (bar, pie, line)

Dependencies:
    - matplotlib: For creating charts and graphs
    - pandas: For data manipulation (used by calling functions)
    - base64: For encoding images as strings
"""

from io import BytesIO
import base64
import matplotlib.pyplot as plt
from .models import Recipe


def get_recipename_from_id(val):
    """
    Retrieve recipe name from database using recipe ID.
    
    This helper function looks up a recipe by its primary key (ID)
    and returns the recipe name. If the recipe doesn't exist,
    it returns a fallback string.
    
    Args:
        val (int): Recipe primary key (ID)
    
    Returns:
        str: Recipe name if found, "Unknown Recipe" if not found
    
    Example:
        >>> get_recipename_from_id(5)
        'Spaghetti Carbonara'
        
        >>> get_recipename_from_id(999)  # Non-existent ID
        'Unknown Recipe'
    
    Notes:
        - Uses try/except to handle DoesNotExist exception
        - Prevents application crashes from invalid IDs
    """
    try:
        # Query database for recipe with given ID
        recipename = Recipe.objects.get(id=val)
        # Return the name attribute of the recipe
        return recipename.name
    except Recipe.DoesNotExist:
        # Return fallback string if recipe not found
        return "Unknown Recipe"


def get_graph():
    """
    Convert current matplotlib plot to base64-encoded string.
    
    This function handles the low-level image processing needed to
    embed matplotlib charts in HTML templates:
    
    Process:
    1. Create BytesIO buffer (in-memory bytes buffer)
    2. Save current matplotlib plot to buffer as PNG
    3. Extract PNG bytes from buffer
    4. Encode bytes to base64 (ASCII-safe format)
    5. Decode to UTF-8 string for HTML embedding
    6. Clean up buffer memory
    
    Returns:
        str: Base64-encoded PNG image as string
    
    Example:
        >>> plt.plot([1, 2, 3], [4, 5, 6])
        >>> graph_string = get_graph()
        >>> # Use in template: <img src="data:image/png;base64,{{ graph_string }}">
    
    Notes:
        - Must be called AFTER creating a plot with matplotlib
        - Image is temporary (stored in memory, not on disk)
        - Base64 encoding allows embedding in HTML/CSS
        - Buffer.close() frees memory after encoding
    """
    # Create a BytesIO buffer (in-memory binary stream) for the image
    # This avoids writing to disk
    buffer = BytesIO()
    
    # Save the current matplotlib plot to the buffer in PNG format
    # format='png': Specifies PNG image format (could be jpg, svg, etc.)
    plt.savefig(buffer, format='png')
    
    # Set cursor to the beginning of the stream
    # Required before reading data from buffer
    buffer.seek(0)
    
    # Retrieve the entire content of the buffer as bytes
    # This is the raw PNG image data
    image_png = buffer.getvalue()
    
    # Encode the bytes-like object to base64
    # Base64 encoding converts binary data to ASCII characters
    # Necessary for embedding images in HTML/JSON
    graph = base64.b64encode(image_png)
    
    # Decode from bytes to UTF-8 string
    # Required for template rendering (templates expect strings, not bytes)
    graph = graph.decode('utf-8')
    
    # Free up the memory allocated for the buffer
    # Good practice to prevent memory leaks
    buffer.close()
    
    # Return the base64-encoded image string
    # Can be used in HTML: <img src="data:image/png;base64,{graph}">
    return graph


def get_chart(chart_type, data, **kwargs):
    """
    Generate data visualization chart based on recipe data.
    
    Creates one of three chart types (bar, pie, line) using matplotlib
    and returns it as a base64-encoded string for HTML embedding.
    
    Chart Types:
    - '#1': Bar chart - Shows cooking time for each recipe
    - '#2': Pie chart - Shows distribution by difficulty level
    - '#3': Line chart - Shows cooking time trend across recipes
    
    Args:
        chart_type (str): Chart type identifier ('#1', '#2', or '#3')
        data (DataFrame): pandas DataFrame with recipe data
            Required columns vary by chart type:
            - Bar/Line: 'name', 'cooking_time'
            - Pie: 'difficulty'
        **kwargs: Additional keyword arguments
            labels (list): Custom labels for charts (optional)
    
    Returns:
        str: Base64-encoded PNG image string for HTML embedding
        None: If chart_type is invalid or data is empty
    
    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'name': ['Pasta', 'Salad'],
        ...     'cooking_time': [15, 5],
        ...     'difficulty': ['Easy', 'Easy']
        ... })
        >>> chart = get_chart('#1', data)
        >>> # Use in template: <img src="data:image/png;base64,{{ chart }}">
    
    Notes:
        - Uses 'AGG' backend (Anti-Grain Geometry) for file output
        - All charts use consistent styling (colors, fonts, sizes)
        - Clears previous plots with plt.clf() to prevent overlap
        - Layout is tight to prevent label cutoff
    """
    # Switch plot backend to AGG (Anti-Grain Geometry)
    # AGG backend is non-interactive and designed for writing to files
    # Required for server-side rendering (no display needed)
    plt.switch_backend('AGG')
    
    # Clear any existing plots from memory
    # Prevents overlapping of multiple charts
    # Important when generating multiple charts in sequence
    plt.clf()
    
    # Create a new figure with specified dimensions
    # figsize=(width, height) in inches
    # 8x5 provides good balance for web display
    fig = plt.figure(figsize=(8, 5))
    
    # Select chart type based on user input
    # Each chart type has different visualization purpose
    
    if chart_type == '#1':
        # BAR CHART: Recipes vs Cooking Time
        # Best for comparing cooking times across different recipes
        
        # Create vertical bar chart
        # x-axis: recipe names, y-axis: cooking times
        # color: Material Design blue (#3498db)
        plt.bar(data['name'], data['cooking_time'], color='#3498db')
        
        # Set x-axis label with font size
        plt.xlabel('Recipe Name', fontsize=12)
        
        # Set y-axis label with font size
        plt.ylabel('Cooking Time (minutes)', fontsize=12)
        
        # Set chart title with larger, bold font
        plt.title('Cooking Time by Recipe', fontsize=14, fontweight='bold')
        
        # Rotate x-axis labels for readability
        # rotation=45: 45-degree angle
        # ha='right': horizontal alignment right (prevents overlap)
        plt.xticks(rotation=45, ha='right')
        
    elif chart_type == '#2':
        # PIE CHART: Distribution by Difficulty Level
        # Best for showing proportions of recipe difficulties
        
        # Extract custom labels if provided (not currently used)
        labels = kwargs.get('labels')
        
        # Define colors for difficulty levels
        # Green (Easy), Orange (Medium), Dark Orange (Intermediate), Red (Hard)
        colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
        
        # Create pie chart from difficulty value counts
        # value_counts() counts occurrences of each difficulty level
        # autopct: Display percentage with 1 decimal place
        # startangle: Start first slice at 90 degrees (top of circle)
        plt.pie(data['difficulty'].value_counts(), 
                labels=data['difficulty'].value_counts().index,  # Use difficulty names as labels
                autopct='%1.1f%%',  # Format: "25.5%"
                colors=colors,       # Custom color scheme
                startangle=90)       # Start from top (12 o'clock position)
        
        # Set chart title
        plt.title('Recipe Distribution by Difficulty', fontsize=14, fontweight='bold')
        
    elif chart_type == '#3':
        # LINE CHART: Cooking Time Trend
        # Best for showing trends or patterns across recipes
        
        # Create line plot
        # x-axis: recipe names, y-axis: cooking times
        # marker='o': Circle markers at each data point
        # color: Material Design purple (#9b59b6)
        # linewidth: Line thickness (2 pixels)
        # markersize: Size of circle markers (8 pixels)
        plt.plot(data['name'], data['cooking_time'], 
                marker='o',      # Circle markers at data points
                color='#9b59b6', # Purple line color
                linewidth=2,     # Line thickness
                markersize=8)    # Marker size
        
        # Set x-axis label
        plt.xlabel('Recipe Name', fontsize=12)
        
        # Set y-axis label
        plt.ylabel('Cooking Time (minutes)', fontsize=12)
        
        # Set chart title
        plt.title('Cooking Time Trend', fontsize=14, fontweight='bold')
        
        # Rotate x-axis labels for readability
        plt.xticks(rotation=45, ha='right')
        
        # Add grid lines for easier reading
        # alpha=0.3: Semi-transparent grid (30% opacity)
        plt.grid(True, alpha=0.3)
        
    else:
        # Handle invalid chart type
        # Prints to console (useful for debugging)
        print('Unknown chart type')
    
    # Adjust layout to prevent label cutoff
    # tight_layout() automatically adjusts subplot params
    # Prevents x-axis labels from being cut off at bottom
    plt.tight_layout()
    
    # Render the graph to base64 string using get_graph() helper
    # Returns base64-encoded PNG image
    chart = get_graph()
    
    # Return the chart image string for HTML embedding
    return chart
