"""
3D Dunya Gorsellestirmesi - CO2 Emisyon Analizi
Plotly ile interaktif 3D globe ve ulke marker'lari
Unlem isaretleri ile kirlilik gosterimi
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Ulke koordinatlari (enlem, boylam)
COUNTRY_COORDS = {
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'Turkey': {'lat': 38.9637, 'lon': 35.2433},
    'India': {'lat': 20.5937, 'lon': 78.9629}
}

# CO2 degerine gore renk hesapla (dusuk=yesil/sari, yuksek=turuncu/kirmizi)
def get_pollution_color(co2_value, min_co2=100, max_co2=12000):
    """
    CO2 degerine gore renk dondurur
    Dusuk kirlilik: Yesil -> Sari
    Yuksek kirlilik: Turuncu -> Kirmizi
    """
    if co2_value <= 0:
        return 'rgb(100, 200, 100)'  # Yesil (veri yok)
    
    # Normalizasyon (0-1 arasi)
    normalized = min(1, max(0, (co2_value - min_co2) / (max_co2 - min_co2)))
    
    # Renk gecisi: Yesil -> Sari -> Turuncu -> Kirmizi
    if normalized < 0.25:
        # Yesil -> Sari-yesil
        r = int(100 + normalized * 4 * 155)  # 100 -> 255
        g = int(200 + normalized * 4 * 55)   # 200 -> 255
        b = int(100 - normalized * 4 * 100)  # 100 -> 0
    elif normalized < 0.5:
        # Sari-yesil -> Sari
        t = (normalized - 0.25) * 4
        r = 255
        g = 255
        b = int(0)
    elif normalized < 0.75:
        # Sari -> Turuncu
        t = (normalized - 0.5) * 4
        r = 255
        g = int(255 - t * 130)  # 255 -> 125
        b = 0
    else:
        # Turuncu -> Kirmizi
        t = (normalized - 0.75) * 4
        r = 255
        g = int(125 - t * 125)  # 125 -> 0
        b = 0
    
    return f'rgb({r}, {g}, {b})'

def load_data():
    """Veri setini yukler"""
    try:
        data = pd.read_csv("Datasets/owid-co2-data.csv")
    except FileNotFoundError:
        data = pd.read_csv("Nature-Pollution/Datasets/owid-co2-data.csv")
    return data

def prepare_country_data(df, countries, start_year=1990, end_year=2024):
    """Ulke verilerini hazirlar"""
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

def create_3d_globe_visualization(df, year):
    """
    Belirli bir yil icin 3D dunya gorsellestirmesi olusturur
    Unlem isareti marker'lari ile
    """
    countries = list(COUNTRY_COORDS.keys())
    df_year = df[df['year'] == year]
    
    # Toplam CO2 ve diger metrikleri hesapla (yuzdelik icin)
    total_co2 = df_year['co2'].sum()
    total_pop = df_year['population'].sum() if 'population' in df_year.columns else 1
    max_co2_pc = df_year['co2_per_capita'].max() if 'co2_per_capita' in df_year.columns else 1
    
    # Veri hazirligi
    lats = []
    lons = []
    hover_texts = []
    marker_texts = []  # Unlem isaretleri
    sizes = []
    colors = []
    
    for country in countries:
        coords = COUNTRY_COORDS[country]
        country_data = df_year[df_year['country'] == country]
        
        if not country_data.empty:
            co2 = country_data['co2'].values[0]
            co2_pc = country_data['co2_per_capita'].values[0] if 'co2_per_capita' in country_data.columns else 0
            pop = country_data['population'].values[0] if 'population' in country_data.columns else 0
            gdp = country_data['gdp'].values[0] if 'gdp' in country_data.columns else 0
        else:
            co2 = 0
            co2_pc = 0
            pop = 0
            gdp = 0
        
        lats.append(coords['lat'])
        lons.append(coords['lon'])
        
        # Kirlilik rengini hesapla
        color = get_pollution_color(co2)
        colors.append(color)
        
        # Marker boyutu CO2 emisyonuna gore
        size = max(20, min(60, co2 / 150)) if co2 > 0 else 20
        sizes.append(size)
        
        # Unlem isareti (kirlilik seviyesine gore sayisi artar)
        if co2 > 8000:
            marker_texts.append("!!!")
        elif co2 > 4000:
            marker_texts.append("!!")
        else:
            marker_texts.append("!")
        
        # Yuzdelik hesaplamalar
        co2_pct = (co2 / total_co2 * 100) if total_co2 > 0 else 0
        pop_pct = (pop / total_pop * 100) if total_pop > 0 else 0
        co2_pc_pct = (co2_pc / max_co2_pc * 100) if max_co2_pc > 0 else 0
        
        # Hover text - yuzdelik oranlarla
        hover_text = f"<b>{country}</b><br>"
        hover_text += f"<b>Yil: {year}</b><br>"
        hover_text += f"<br><b>--- CO2 Emisyonu ---</b><br>"
        hover_text += f"Toplam: {co2:,.0f} Mt<br>"
        hover_text += f"Dunya Payi: <b>{co2_pct:.1f}%</b><br>"
        hover_text += f"<br><b>--- Kisi Basi ---</b><br>"
        hover_text += f"CO2/Kisi: {co2_pc:.2f} ton<br>"
        hover_text += f"En Yuksege Orani: {co2_pc_pct:.1f}%<br>"
        hover_text += f"<br><b>--- Diger ---</b><br>"
        hover_text += f"Nufus: {pop/1e6:,.1f} M ({pop_pct:.1f}%)<br>"
        hover_text += f"GDP: ${gdp/1e9:,.1f} B"
        hover_texts.append(hover_text)
    
    # 3D Globe Figure
    fig = go.Figure()
    
    # Unlem isaretleri olarak text marker'lar
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=marker_texts,
        hovertext=hover_texts,
        hoverinfo='text',
        mode='text+markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.9,
            line=dict(width=3, color='white'),
            symbol='circle'
        ),
        textfont=dict(
            size=[s * 0.8 for s in sizes],
            color='white',
            family='Arial Black'
        ),
        textposition='middle center',
        showlegend=False
    ))
    
    # Globe projection ayarlari
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor='rgb(40, 60, 40)',
        showocean=True,
        oceancolor='rgb(30, 50, 80)',
        showlakes=True,
        lakecolor='rgb(40, 70, 100)',
        showcountries=True,
        countrycolor='rgb(80, 80, 80)',
        countrywidth=0.5,
        showcoastlines=True,
        coastlinecolor='rgb(100, 100, 100)',
        coastlinewidth=1,
        bgcolor='rgba(0,0,0,0)',
        projection_rotation=dict(lon=50, lat=30, roll=0)
    )
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f'Dunya CO2 Emisyonlari - {year}',
            font=dict(size=24, color='white'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='rgb(20, 20, 30)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=60, b=0),
        height=700,
        annotations=[
            dict(
                text="! = Dusuk | !! = Orta | !!! = Yuksek Kirlilik<br>Renk: Yesil (dusuk) -> Kirmizi (yuksek)",
                showarrow=False,
                x=0.5,
                y=-0.05,
                xref='paper',
                yref='paper',
                font=dict(size=12, color='gray'),
                align='center'
            )
        ]
    )
    
    return fig

def create_animated_globe(df, start_year=2000, end_year=2024):
    """
    Yil slider'i ile animasyonlu 3D globe olusturur
    Unlem isaretleri ve kirlilik renkleri ile
    """
    countries = list(COUNTRY_COORDS.keys())
    years = list(range(start_year, end_year + 1))
    
    # Ilk frame icin veri
    df_first = df[df['year'] == start_year]
    
    lats, lons, marker_texts, hover_texts, sizes, colors = [], [], [], [], [], []
    
    for country in countries:
        coords = COUNTRY_COORDS[country]
        country_data = df_first[df_first['country'] == country]
        
        if not country_data.empty:
            co2 = country_data['co2'].values[0] if pd.notna(country_data['co2'].values[0]) else 0
            co2_pc = country_data['co2_per_capita'].values[0] if pd.notna(country_data['co2_per_capita'].values[0]) else 0
            pop = country_data['population'].values[0] if pd.notna(country_data['population'].values[0]) else 0
        else:
            co2, co2_pc, pop = 0, 0, 0
        
        lats.append(coords['lat'])
        lons.append(coords['lon'])
        colors.append(get_pollution_color(co2))
        sizes.append(max(20, min(60, co2 / 150)) if co2 > 0 else 20)
        
        if co2 > 8000:
            marker_texts.append("!!!")
        elif co2 > 4000:
            marker_texts.append("!!")
        else:
            marker_texts.append("!")
            
        hover_texts.append(f"<b>{country}</b><br>CO2: {co2:,.0f} Mt<br>Kisi Basi: {co2_pc:.2f} ton")
    
    # Ana figure
    fig = go.Figure()
    
    # Scatter marker
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=marker_texts,
        hovertext=hover_texts,
        hoverinfo='text',
        mode='text+markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.9,
            line=dict(width=3, color='white'),
        ),
        textfont=dict(
            size=[s * 0.8 for s in sizes],
            color='white',
            family='Arial Black'
        ),
        textposition='middle center',
        showlegend=False
    ))
    
    # Her yil icin frame olustur
    frames = []
    for year in years:
        df_year = df[df['year'] == year]
        
        # O yil icin toplamlar
        total_co2_year = df_year['co2'].sum()
        total_pop_year = df_year['population'].sum() if 'population' in df_year.columns else 1
        max_co2_pc_year = df_year['co2_per_capita'].max() if 'co2_per_capita' in df_year.columns else 1
        
        frame_sizes = []
        frame_colors = []
        frame_marker_texts = []
        frame_hover_texts = []
        
        for country in countries:
            country_data = df_year[df_year['country'] == country]
            
            if not country_data.empty:
                co2 = country_data['co2'].values[0] if pd.notna(country_data['co2'].values[0]) else 0
                co2_pc = country_data['co2_per_capita'].values[0] if pd.notna(country_data['co2_per_capita'].values[0]) else 0
                pop = country_data['population'].values[0] if pd.notna(country_data['population'].values[0]) else 0
                gdp = country_data['gdp'].values[0] if pd.notna(country_data['gdp'].values[0]) else 0
            else:
                co2, co2_pc, pop, gdp = 0, 0, 0, 0
            
            frame_sizes.append(max(20, min(60, co2 / 150)) if co2 > 0 else 20)
            frame_colors.append(get_pollution_color(co2))
            
            if co2 > 8000:
                frame_marker_texts.append("!!!")
            elif co2 > 4000:
                frame_marker_texts.append("!!")
            else:
                frame_marker_texts.append("!")
            
            # Yuzdelik hesaplamalar
            co2_pct = (co2 / total_co2_year * 100) if total_co2_year > 0 else 0
            pop_pct = (pop / total_pop_year * 100) if total_pop_year > 0 else 0
            co2_pc_pct = (co2_pc / max_co2_pc_year * 100) if max_co2_pc_year > 0 else 0
            
            frame_hover_texts.append(
                f"<b>{country}</b><br>"
                f"<b>Yil: {year}</b><br><br>"
                f"<b>CO2:</b> {co2:,.0f} Mt<br>"
                f"<b>Dunya Payi: {co2_pct:.1f}%</b><br><br>"
                f"Kisi Basi: {co2_pc:.2f} ton<br>"
                f"Nufus: {pop/1e6:,.1f} M"
            )
        
        frames.append(go.Frame(
            data=[go.Scattergeo(
                lon=lons,
                lat=lats,
                text=frame_marker_texts,
                hovertext=frame_hover_texts,
                hoverinfo='text',
                mode='text+markers',
                marker=dict(
                    size=frame_sizes,
                    color=frame_colors,
                    opacity=0.9,
                    line=dict(width=3, color='white'),
                ),
                textfont=dict(
                    size=[s * 0.8 for s in frame_sizes],
                    color='white',
                    family='Arial Black'
                ),
                textposition='middle center',
            )],
            name=str(year)
        ))
    
    fig.frames = frames
    
    # Slider ve animasyon butonlari
    sliders = [dict(
        active=0,
        yanchor='top',
        xanchor='left',
        currentvalue=dict(
            font=dict(size=16, color='white'),
            prefix='Yil: ',
            visible=True,
            xanchor='center'
        ),
        transition=dict(duration=300, easing='cubic-in-out'),
        pad=dict(b=10, t=50),
        len=0.9,
        x=0.05,
        y=0,
        steps=[dict(
            args=[[str(year)],
                  dict(frame=dict(duration=500, redraw=True),
                       mode='immediate',
                       transition=dict(duration=300))],
            label=str(year),
            method='animate'
        ) for year in years]
    )]
    
    updatemenus = [dict(
        type='buttons',
        showactive=False,
        y=0,
        x=0.05,
        xanchor='right',
        yanchor='top',
        pad=dict(t=50, r=10),
        buttons=[
            dict(
                label='Oynat',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=500, redraw=True),
                    fromcurrent=True,
                    transition=dict(duration=300, easing='quadratic-in-out')
                )]
            ),
            dict(
                label='Durdur',
                method='animate',
                args=[[None], dict(
                    frame=dict(duration=0, redraw=False),
                    mode='immediate',
                    transition=dict(duration=0)
                )]
            )
        ]
    )]
    
    # Globe projection
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor='rgb(50, 70, 50)',
        showocean=True,
        oceancolor='rgb(30, 50, 80)',
        showlakes=True,
        lakecolor='rgb(40, 70, 100)',
        showcountries=True,
        countrycolor='rgb(100, 100, 100)',
        countrywidth=0.5,
        showcoastlines=True,
        coastlinecolor='rgb(120, 120, 120)',
        coastlinewidth=1,
        bgcolor='rgba(0,0,0,0)',
        projection_rotation=dict(lon=50, lat=20, roll=0)
    )
    
    # Layout
    fig.update_layout(
        title=dict(
            text='Dunya CO2 Emisyonlari (2000-2024)',
            font=dict(size=26, color='white', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='rgb(15, 15, 25)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=20, r=20, t=80, b=120),
        height=800,
        sliders=sliders,
        updatemenus=updatemenus,
        annotations=[
            dict(
                text="! = Dusuk Kirlilik | !! = Orta Kirlilik | !!! = Yuksek Kirlilik<br>Renk Skalasi: Yesil (dusuk) -> Sari -> Turuncu -> Kirmizi (yuksek)",
                showarrow=False,
                x=0.5,
                y=-0.12,
                xref='paper',
                yref='paper',
                font=dict(size=13, color='lightgray'),
                align='center'
            )
        ]
    )
    
    return fig

def create_country_comparison_chart(df, countries, year):
    """Ulkeler arasi karsilastirma cubugu"""
    df_year = df[(df['year'] == year) & (df['country'].isin(countries))]
    
    fig = go.Figure()
    
    for country in countries:
        country_data = df_year[df_year['country'] == country]
        if not country_data.empty:
            co2 = country_data['co2'].values[0]
            color = get_pollution_color(co2)
            
            fig.add_trace(go.Bar(
                x=[country],
                y=[co2],
                name=country,
                marker_color=color,
                text=[f'{co2:,.0f} Mt'],
                textposition='outside',
                hovertemplate=f'<b>{country}</b><br>CO2: %{{y:,.0f}} Mt<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(
            text=f'Ulke Bazli CO2 Emisyonlari - {year}',
            font=dict(size=20, color='white'),
            x=0.5
        ),
        paper_bgcolor='rgb(20, 20, 30)',
        plot_bgcolor='rgb(30, 30, 45)',
        font=dict(color='white'),
        xaxis=dict(title='Ulke', gridcolor='rgb(50,50,60)'),
        yaxis=dict(title='CO2 Emisyonu (Mt)', gridcolor='rgb(50,50,60)'),
        showlegend=False,
        height=400
    )
    
    return fig

def main():
    """Ana fonksiyon - gorsellestirmeleri olusturur ve kaydeder"""
    print("[*] 3D Dunya CO2 Gorsellestirmesi Olusturuluyor...")
    print("[*] Unlem isaretleri ve kirlilik renkleri ile...")
    
    # Veri yukle
    df = load_data()
    countries = list(COUNTRY_COORDS.keys())
    df_prepared = prepare_country_data(df, countries)
    
    print("[OK] Veri yuklendi ve islendi")
    
    # Animasyonlu 3D Globe
    print("[*] Animasyonlu 3D Globe olusturuluyor...")
    fig_animated = create_animated_globe(df_prepared, 2000, 2024)
    fig_animated.write_html("img/3d_globe_animated.html")
    print("[OK] Kaydedildi: img/3d_globe_animated.html")
    
    # 2024 yili statik globe
    print("[*] 2024 yili 3D Globe olusturuluyor...")
    fig_2024 = create_3d_globe_visualization(df_prepared, 2024)
    fig_2024.write_html("img/3d_globe_2024.html")
    print("[OK] Kaydedildi: img/3d_globe_2024.html")
    
    # Ulke karsilastirma
    print("[*] Ulke karsilastirma grafikleri olusturuluyor...")
    fig_comparison = create_country_comparison_chart(df_prepared, countries, 2024)
    fig_comparison.write_html("img/country_comparison_2024.html")
    print("[OK] Kaydedildi: img/country_comparison_2024.html")
    
    print("\n" + "="*50)
    print("[DONE] Tum gorsellestirmeler basariyla olusturuldu!")
    print("="*50)
    print("\n[INFO] Ozellikler:")
    print("   - Unlem isaretleri: ! (dusuk) | !! (orta) | !!! (yuksek)")
    print("   - Renk skalasi: Yesil -> Sari -> Turuncu -> Kirmizi")
    print("   - Kirlilik arttikca renk kirmiziya kayar")
    print("\n[FILES] Olusturulan dosyalar:")
    print("   - img/3d_globe_animated.html - Animasyonlu 3D Dunya (2000-2024)")
    print("   - img/3d_globe_2024.html - 2024 Statik 3D Dunya")
    print("   - img/country_comparison_2024.html - Ulke Karsilastirma")

if __name__ == "__main__":
    main()
