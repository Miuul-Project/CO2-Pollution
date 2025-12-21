"""
3D Globe GIF Generator
Creates an animated GIF of the CO2 emissions globe from 2000-2024
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import imageio.v2 as imageio
import os
import warnings
warnings.filterwarnings('ignore')

# Country coordinates
COUNTRY_COORDS = {
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'Turkey': {'lat': 38.9637, 'lon': 35.2433},
    'India': {'lat': 20.5937, 'lon': 78.9629}
}

def get_pollution_color(co2_value, min_co2=100, max_co2=12000):
    """CO2 value to color (green to red)"""
    if co2_value <= 0:
        return 'rgb(100, 200, 100)'
    
    normalized = min(1, max(0, (co2_value - min_co2) / (max_co2 - min_co2)))
    
    if normalized < 0.25:
        r = int(100 + normalized * 4 * 155)
        g = int(200 + normalized * 4 * 55)
        b = int(100 - normalized * 4 * 100)
    elif normalized < 0.5:
        r = 255
        g = 255
        b = 0
    elif normalized < 0.75:
        t = (normalized - 0.5) * 4
        r = 255
        g = int(255 - t * 130)
        b = 0
    else:
        t = (normalized - 0.75) * 4
        r = 255
        g = int(125 - t * 125)
        b = 0
    
    return f'rgb({r}, {g}, {b})'

def load_data():
    """Load dataset"""
    try:
        data = pd.read_csv("Datasets/owid-co2-data.csv")
    except FileNotFoundError:
        data = pd.read_csv("Nature-Pollution/Datasets/owid-co2-data.csv")
    return data

def prepare_country_data(df, countries, start_year=1990, end_year=2024):
    """Prepare country data"""
    df_filtered = df[
        (df['country'].isin(countries)) & 
        (df['year'] >= start_year) & 
        (df['year'] <= end_year)
    ].copy()
    
    df_filtered = df_filtered.sort_values(['country', 'year'])
    df_filtered['co2'] = df_filtered.groupby('country')['co2'].transform(
        lambda x: x.interpolate(method='linear', limit_direction='both')
    )
    df_filtered['co2_per_capita'] = df_filtered.groupby('country')['co2_per_capita'].transform(
        lambda x: x.interpolate(method='linear', limit_direction='both')
    )
    
    return df_filtered

def create_globe_frame(df, year, countries):
    """Create a single globe frame for a specific year"""
    df_year = df[df['year'] == year]
    total_co2 = df_year['co2'].sum()
    
    lats, lons, texts, sizes, colors = [], [], [], [], []
    
    for country in countries:
        coords = COUNTRY_COORDS[country]
        country_data = df_year[df_year['country'] == country]
        
        if not country_data.empty:
            co2 = country_data['co2'].values[0] if pd.notna(country_data['co2'].values[0]) else 0
        else:
            co2 = 0
        
        lats.append(coords['lat'])
        lons.append(coords['lon'])
        colors.append(get_pollution_color(co2))
        sizes.append(max(25, min(70, co2 / 120)) if co2 > 0 else 25)
        
        # Marker text
        if co2 > 8000:
            texts.append("!!!")
        elif co2 > 4000:
            texts.append("!!")
        else:
            texts.append("!")
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='text+markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.9,
            line=dict(width=3, color='white'),
        ),
        textfont=dict(
            size=[s * 0.7 for s in sizes],
            color='white',
            family='Arial Black'
        ),
        textposition='middle center',
        showlegend=False
    ))
    
    # Globe projection - rotated to show all analyzed countries
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor='rgb(60, 80, 60)',
        showocean=True,
        oceancolor='rgb(40, 60, 100)',
        showlakes=True,
        lakecolor='rgb(50, 80, 120)',
        showcountries=True,
        countrycolor='rgb(120, 120, 120)',
        countrywidth=0.8,
        showcoastlines=True,
        coastlinecolor='rgb(140, 140, 140)',
        coastlinewidth=1.2,
        bgcolor='rgba(0,0,0,0)',
        # Rotation to show Europe, Asia, and parts of Americas
        projection_rotation=dict(lon=60, lat=25, roll=0)
    )
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f'<b>Global CO2 Emissions - {year}</b>',
            font=dict(size=28, color='white', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        paper_bgcolor='rgb(20, 25, 35)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=80, b=60),
        width=800,
        height=700,
        annotations=[
            dict(
                text=f"! Low | !! Medium | !!! High Pollution<br>Color: Green (low) to Red (high)",
                showarrow=False,
                x=0.5,
                y=0.02,
                xref='paper',
                yref='paper',
                font=dict(size=14, color='lightgray'),
                align='center'
            )
        ]
    )
    
    return fig

def generate_gif(start_year=2000, end_year=2024, output_path="img/3d_globe_animation.gif"):
    """Generate animated GIF from 3D globe frames"""
    print("[*] 3D Globe GIF Generator")
    print("="*50)
    
    # Load and prepare data
    df = load_data()
    countries = list(COUNTRY_COORDS.keys())
    df_prepared = prepare_country_data(df, countries)
    print("[OK] Data loaded and prepared")
    
    # Create temp directory for frames
    temp_dir = "img/temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate frames
    years = list(range(start_year, end_year + 1))
    frame_paths = []
    
    print(f"[*] Generating {len(years)} frames...")
    for i, year in enumerate(years):
        fig = create_globe_frame(df_prepared, year, countries)
        frame_path = f"{temp_dir}/frame_{year}.png"
        fig.write_image(frame_path, scale=2)
        frame_paths.append(frame_path)
        print(f"    Frame {i+1}/{len(years)}: {year}")
    
    print("[OK] All frames generated")
    
    # Create GIF
    print("[*] Combining frames into GIF...")
    images = []
    for path in frame_paths:
        images.append(imageio.imread(path))
    
    # Add pause at the end (repeat last frame)
    for _ in range(3):
        images.append(imageio.imread(frame_paths[-1]))
    
    # Save GIF (duration in seconds per frame)
    imageio.mimsave(output_path, images, duration=0.5, loop=0)
    print(f"[OK] GIF saved: {output_path}")
    
    # Cleanup temp files
    print("[*] Cleaning up temporary files...")
    for path in frame_paths:
        try:
            os.remove(path)
        except:
            pass
    try:
        os.rmdir(temp_dir)
    except:
        pass
    print("[OK] Cleanup complete")
    
    print("="*50)
    print(f"[DONE] Animation created: {output_path}")
    print(f"       Years: {start_year} - {end_year}")
    print(f"       Countries: {', '.join(countries)}")
    
    return output_path

if __name__ == "__main__":
    generate_gif()
