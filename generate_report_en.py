from fpdf import FPDF
import os
import json
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, 'GLOBAL CO2 EMISSIONS ANALYSIS', 0, 1, 'C')
        self.set_font('Arial', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, 'A Comprehensive Data Science Study on Climate Change Indicators', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | CO2 Data Analysis Report | 2024', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 13)
        self.set_text_color(0, 51, 102)
        self.set_fill_color(230, 240, 250)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(3)

    def section_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, body)
        self.ln(3)

    def add_image(self, image_path, title=""):
        if os.path.exists(image_path):
            self.image(image_path, w=165)
            self.ln(2)
            if title:
                self.set_font('Arial', 'I', 9)
                self.set_text_color(80, 80, 80)
                self.cell(0, 5, f'Figure: {title}', 0, 1, 'C')
            self.ln(4)
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f"[Image not found: {image_path}]", 0, 1)
            self.set_text_color(0, 0, 0)

    def add_table_row(self, col1, col2, header=False):
        if header:
            self.set_font('Arial', 'B', 10)
            self.set_fill_color(0, 51, 102)
            self.set_text_color(255, 255, 255)
        else:
            self.set_font('Arial', '', 10)
            self.set_fill_color(245, 245, 245)
            self.set_text_color(0, 0, 0)
        self.cell(60, 7, col1, 1, 0, 'L', 1)
        self.cell(110, 7, col2, 1, 1, 'L', 1)

pdf = PDF()
pdf.set_margins(20, 20, 20)
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=25)

# ============== COVER PAGE ==============
pdf.set_font('Arial', 'B', 28)
pdf.set_text_color(0, 51, 102)
pdf.ln(30)
pdf.cell(0, 15, 'GRADUATION PROJECT', 0, 1, 'C')
pdf.ln(5)
pdf.set_font('Arial', 'B', 22)
pdf.cell(0, 12, 'Global CO2 Emissions Analysis', 0, 1, 'C')
pdf.set_font('Arial', 'I', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, 'Data-Driven Insights into Climate Change', 0, 1, 'C')
pdf.ln(20)

pdf.set_draw_color(0, 51, 102)
pdf.set_line_width(1)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(20)

pdf.set_font('Arial', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, 'A Comprehensive Study on:', 0, 1, 'C')
pdf.set_font('Arial', 'I', 11)
pdf.cell(0, 7, '- Historical CO2 Emission Trends (1990-2024)', 0, 1, 'C')
pdf.cell(0, 7, '- Country-Specific Comparative Analysis', 0, 1, 'C')
pdf.cell(0, 7, '- Machine Learning Based Forecasting', 0, 1, 'C')
pdf.cell(0, 7, '- Interactive 3D Visualization', 0, 1, 'C')
pdf.ln(30)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, f'Report Date: {datetime.now().strftime("%B %Y")}', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Arial', 'I', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, 'Technologies: Python | Pandas | Scikit-learn | Plotly | Machine Learning', 0, 1, 'C')

# ============== INTRODUCTION ==============
pdf.add_page()

pdf.chapter_title("1. EXECUTIVE SUMMARY")
pdf.chapter_body("This comprehensive research report presents an in-depth analysis of global carbon dioxide (CO2) emissions, one of the most critical indicators of human impact on Earth's climate system. The study examines historical emission trends spanning over three decades (1990-2024), analyzes current patterns across major economies, and provides data-driven projections for the near future (2025-2028).\n\n"
"The research employs advanced data science methodologies, including machine learning algorithms for predictive modeling and interactive 3D visualization techniques for enhanced data exploration. A key innovation of this study is the implementation of 'time-safe' data preprocessing methods that prevent information leakage in time-series analysis, ensuring more reliable and realistic model performance estimates.\n\n"
"The analysis encompasses six major nations - China, United States, India, Russia, Germany, and Turkey - which together represent approximately 60% of global CO2 emissions. These countries were selected to represent diverse economic development stages, energy consumption patterns, and climate policy approaches. Through rigorous statistical analysis and predictive modeling, this study aims to contribute to evidence-based climate policy discussions.")

pdf.chapter_title("2. INTRODUCTION & RESEARCH OBJECTIVES")
pdf.section_title("2.1 Background and Motivation")
pdf.chapter_body("Climate change, driven primarily by anthropogenic greenhouse gas emissions, represents one of the defining challenges of the 21st century. According to the Intergovernmental Panel on Climate Change (IPCC), atmospheric CO2 concentrations have increased by over 50% since the pre-industrial era, from approximately 280 parts per million (ppm) to over 420 ppm in 2024. This unprecedented rise in greenhouse gas concentrations is directly linked to global temperature increases, extreme weather events, and ecosystem disruptions.\n\n"
"Carbon dioxide emissions from fossil fuel combustion account for approximately 75% of total greenhouse gas emissions. Understanding the patterns, drivers, and trajectories of these emissions is essential for developing effective mitigation strategies and informing international climate agreements such as the Paris Agreement, which aims to limit global warming to 1.5-2 degrees Celsius above pre-industrial levels.\n\n"
"This research project was conducted as part of a graduation thesis, demonstrating the application of modern data science techniques to real-world environmental challenges. The study showcases how machine learning, statistical analysis, and interactive visualization can be combined to derive actionable insights from complex climate data.")

pdf.section_title("2.2 Research Objectives")
pdf.chapter_body("The primary objectives of this research are:\n\n"
"1. Historical Trend Analysis: Examine and quantify CO2 emission trends from 1990 to 2024, identifying key inflection points and growth patterns across different regions and time periods.\n\n"
"2. Driver Identification: Identify and analyze the key socioeconomic factors driving emissions, including GDP growth, population dynamics, energy consumption patterns, and industrial development.\n\n"
"3. Predictive Modeling: Develop machine learning models to forecast future emission trajectories (2025-2028), providing quantitative estimates with confidence intervals.\n\n"
"4. Comparative Analysis: Compare emission profiles across six major economies, highlighting differences in carbon intensity, energy mix, and decoupling success.\n\n"
"5. Interactive Visualization: Create innovative 3D visualizations that allow dynamic exploration of spatial and temporal emission patterns.\n\n"
"6. Policy Recommendations: Synthesize findings into evidence-based policy recommendations for each analyzed country.")

pdf.chapter_title("3. DATA STORY & DATASET OVERVIEW")
pdf.section_title("3.1 Data Source and Provenance")
pdf.chapter_body("The primary dataset utilized in this analysis is sourced from 'Our World in Data' (OWID), a scientific online publication affiliated with the University of Oxford. OWID is widely recognized as one of the most comprehensive and reliable sources for global development and environmental data, with datasets regularly cited in academic publications, policy documents, and international reports.\n\n"
"The CO2 emissions dataset (owid-co2-data.csv) aggregates data from multiple authoritative sources including:\n"
"- Global Carbon Project: Primary source for territorial CO2 emissions\n"
"- International Energy Agency (IEA): Energy consumption and fuel-specific emissions\n"
"- World Bank: GDP and population statistics\n"
"- BP Statistical Review: Historical energy data\n\n"
"Data Characteristics:\n"
"- Temporal Coverage: 1750 - 2024 (Analysis focuses on 1990-2024)\n"
"- Geographic Coverage: 200+ countries and territories\n"
"- Total Observations: Approximately 60,000+ data points\n"
"- Update Frequency: Annual, with latest data typically available within 6-12 months of the reference year")

pdf.section_title("3.2 Variables Used in Analysis")
pdf.chapter_body("The following table presents the key categorical and numerical variables employed in this study. Variables were selected based on their relevance to emission analysis and their availability across the analyzed time period and countries:")
pdf.ln(2)

# Variables Table
pdf.add_table_row("Variable", "Description", header=True)
pdf.add_table_row("co2", "Total CO2 emissions (Million tonnes per year)")
pdf.add_table_row("country", "Country or region name (categorical)")
pdf.add_table_row("year", "Year of observation (1750-2024)")
pdf.add_table_row("gdp", "Gross Domestic Product in USD (PPP adjusted)")
pdf.add_table_row("population", "Total population count")
pdf.add_table_row("co2_per_capita", "CO2 emissions per person (tonnes/person)")
pdf.add_table_row("co2_per_gdp", "Carbon intensity (kg CO2 per $ GDP)")
pdf.add_table_row("energy_per_capita", "Primary energy consumption per person (kWh)")
pdf.add_table_row("coal_co2", "CO2 emissions from coal combustion")
pdf.add_table_row("oil_co2", "CO2 emissions from oil combustion")
pdf.add_table_row("gas_co2", "CO2 emissions from natural gas combustion")
pdf.add_table_row("consumption_co2", "Consumption-based CO2 (includes imports)")
pdf.ln(5)

pdf.chapter_title("4. METHODOLOGY")
pdf.section_title("4.1 Data Preprocessing Pipeline")
pdf.chapter_body("A rigorous preprocessing pipeline was implemented to ensure data quality and prevent common pitfalls in time-series analysis:\n\n"
"1. Missing Value Treatment: A novel 'time-safe' linear interpolation method was developed specifically for this study. Unlike traditional interpolation that may use future values to fill past gaps (creating information leakage), our approach ensures that:\n"
"   - Training data (2000-2018): Uses bidirectional interpolation only within the training period\n"
"   - Test data (2019-2024): Uses only forward-fill from past observations, never accessing future information\n\n"
"2. Outlier Detection and Handling: Statistical methods including Interquartile Range (IQR) analysis and Z-score calculations were applied to identify and investigate potential outliers. In most cases, extreme values were verified against original sources before any corrections.\n\n"
"3. Feature Engineering: Several derived features were calculated to enhance analysis:\n"
"   - Year-over-year emission growth rates\n"
"   - Carbon intensity ratios (emissions per unit GDP)\n"
"   - Population-normalized metrics\n"
"   - Fuel mix percentages")

pdf.section_title("4.2 Machine Learning Approach")
pdf.chapter_body("Model Architecture:\n"
"- Algorithm: Multivariate Linear Regression was selected for interpretability and robust performance with limited training data\n"
"- Feature Set: Year, GDP, population, energy consumption, and fuel-specific emissions\n"
"- Training Period: 2000-2018 (19 years of data)\n"
"- Validation Period: 2019-2024 (5 years held out for testing)\n"
"- Prediction Horizon: 2025-2028 (4 years into future)\n\n"
"Key Methodological Innovation - Time-Safe Validation:\n"
"Traditional cross-validation methods may inadvertently leak future information into past predictions, leading to overoptimistic performance estimates. Our time-safe approach strictly maintains temporal ordering:\n"
"1. Data is split chronologically before any preprocessing\n"
"2. Imputation uses only contemporaneous or past information for test data\n"
"3. Model training never accesses test period data\n\n"
"This approach provides realistic estimates of how the model would perform on truly unseen future data.")

# Load time-safe metrics
try:
    with open("metrics_timesafe.json", "r") as f:
        metrics = json.load(f)
    
    pdf.section_title("4.3 Model Performance Metrics")
    pdf.chapter_body(f"The model was rigorously evaluated using standard regression metrics on the held-out test set (2019-2024):\n\n"
                        f"- Root Mean Square Error (RMSE): {metrics['rmse']:.4f}\n"
                        f"  Interpretation: On average, predictions deviate from actual values by approximately {metrics['rmse']:.2f} million tonnes\n\n"
                        f"- Mean Absolute Error (MAE): {metrics['mae']:.4f}\n"
                        f"  Interpretation: The average absolute prediction error is {metrics['mae']:.2f} million tonnes\n\n"
                        f"- R-squared (R2): {metrics['r2']:.4f}\n"
                        f"  Interpretation: The model explains approximately {metrics['r2']*100:.1f}% of the variance in CO2 emissions\n\n"
                        "These metrics, obtained through time-safe validation, provide realistic estimates of model performance on future data.")
except FileNotFoundError:
    pass

pdf.section_title("4.4 Technologies & Tools")
pdf.chapter_body("The following technology stack was employed:\n\n"
"- Python 3.x: Primary programming language, chosen for its rich ecosystem of data science libraries\n"
"- Pandas: High-performance data manipulation and analysis\n"
"- NumPy: Numerical computations and array operations\n"
"- Scikit-learn: Machine learning model development and evaluation\n"
"- Matplotlib & Seaborn: Publication-quality static visualizations\n"
"- Plotly: Interactive 3D globe visualization with animation capabilities\n"
"- FPDF: Automated PDF report generation")

# ============== ANALYSIS SECTIONS ==============
pdf.add_page()
pdf.chapter_title("5. HISTORICAL TREND ANALYSIS")
pdf.section_title("5.1 Global CO2 Emissions Over Time")
pdf.chapter_body("Analysis of global CO2 emissions over the past three decades reveals a consistent upward trajectory, punctuated by brief interruptions during major economic events. Global emissions have increased from approximately 22 billion tonnes in 1990 to over 37 billion tonnes in 2023, representing a 68% increase.\n\n"
"Key observations from the historical trend:\n\n"
"1. Steady Growth (1990-2000): Annual growth rates of approximately 1.5% per year, driven primarily by industrialization in developing economies.\n\n"
"2. Accelerated Growth (2000-2010): The fastest growth decade, with China's rapid industrialization driving global emissions upward at nearly 3% annually.\n\n"
"3. Plateau Attempts (2014-2016): Brief stabilization attributed to China's economic rebalancing and expansion of renewable energy in developed nations.\n\n"
"4. COVID-19 Impact (2020): Unprecedented 5.4% decline due to global lockdowns, the largest single-year reduction in recorded history.\n\n"
"5. Post-Pandemic Rebound (2021-2024): Emissions quickly recovered and exceeded pre-pandemic levels, indicating that structural changes to the energy system are needed for lasting reductions.")
pdf.add_image("img/global_co2_trend.png", "Global Average CO2 Emissions Trend (1990-2024)")

pdf.section_title("5.2 Country-Specific Emission Profiles")
pdf.chapter_body("Comparative analysis of the six selected nations reveals dramatically different emission trajectories, reflecting their diverse economic development paths, energy policies, and demographic trends:\n\n"
"CHINA:\n"
"China has emerged as the world's largest CO2 emitter, currently responsible for approximately 30% of global emissions. Key characteristics include:\n"
"- Emissions increased nearly 400% between 1990 and 2024\n"
"- Coal remains the dominant energy source (>60% of primary energy)\n"
"- Recent years show signs of plateau as renewable capacity expands rapidly\n"
"- Per capita emissions now exceed EU average but remain below US levels\n\n"
"UNITED STATES:\n"
"Historically the largest emitter, the US now ranks second globally:\n"
"- Peak emissions occurred in 2007, with subsequent decline of ~15%\n"
"- Successful decoupling of emissions from GDP growth demonstrated\n"
"- Natural gas replacing coal has driven significant reductions\n"
"- Highest per capita emissions among major economies (approximately 15 tonnes/person)\n\n"
"INDIA:\n"
"As a rapidly developing economy, India shows strong emission growth:\n"
"- Emissions have tripled since 1990\n"
"- Now the third-largest emitter globally\n"
"- Per capita emissions remain very low (approximately 1.9 tonnes/person)\n"
"- Coal expansion continues despite significant solar investment\n\n"
"RUSSIA:\n"
"Russia's emissions show unique post-Soviet dynamics:\n"
"- Sharp decline in 1990s following economic collapse\n"
"- Gradual recovery since 2000, now approximately 15% below 1990 levels\n"
"- Heavy dependence on natural gas for domestic energy\n"
"- Significant exporter of fossil fuels\n\n"
"GERMANY:\n"
"Germany represents a European success story in emissions reduction:\n"
"- Emissions down approximately 40% from 1990 levels\n"
"- Ambitious 'Energiewende' (Energy Transition) policy driving change\n"
"- Challenges remain in phasing out coal while maintaining energy security\n"
"- Strong industrial base maintaining economic growth despite reductions\n\n"
"TURKEY:\n"
"Turkey shows characteristics of an emerging economy:\n"
"- Emissions have increased approximately 150% since 1990\n"
"- Growing economy drives increased energy demand\n"
"- Significant coal and natural gas consumption\n"
"- Developing domestic renewable energy capacity")
pdf.add_image("img/country_co2_trend.png", "CO2 Emissions by Country (1990-2024)")

# ============== 3D VISUALIZATION SECTION - MOVED HERE ==============
pdf.add_page()
pdf.chapter_title("6. INTERACTIVE 3D VISUALIZATION")
pdf.chapter_body("A key innovation of this research project is the development of an interactive 3D globe visualization that allows users to explore CO2 emission data dynamically. This visualization represents a novel approach to presenting climate data, moving beyond static charts to immersive spatial analysis.\n\n"
"The visualization transforms abstract emission statistics into an intuitive, engaging format that makes it easy to:\n"
"- Compare emission levels across countries at a glance\n"
"- Observe temporal changes through animated playback\n"
"- Identify patterns and outliers in the data\n"
"- Communicate findings to non-technical audiences effectively\n\n"
"KEY VISUALIZATION FEATURES:\n\n"
"1. 3D Rotating Globe: An orthographic projection of Earth that provides a realistic spatial context. The globe displays country boundaries and terrestrial features with a contrast-optimized theme suitable for professional presentations.\n\n"
"2. Dynamic Markers: Each analyzed country is represented by a circular marker positioned at its geographic center. Marker characteristics encode multidimensional emission data:\n"
"   - Size: Proportional to total CO2 emissions (larger markers indicate higher emissions)\n"
"   - Color: Gradient scale shifting from green (lower impact) to red (critical impact)\n"
"   - Severity Indicators: Visual cues denoting pollution intensity levels\n\n"
"3. Temporal Evolution: The visualization includes a temporal dimension, allowing observers to witness the evolution of emissions from 2000 to 2024. This animated view reveals the shifting center of global emissions over time.\n\n"
"4. Data-Rich Interaction: The system provides detailed analytical data on demand, including:\n"
"   - Total annual CO2 emissions\n"
"   - Global contribution percentages\n"
"   - Per capita emission metrics\n"
"   - Demographic context\n\n"
"This interactive tool serves as a bridge between complex statistical data and public understanding, facilitating more informed discussions about climate trends.")

# Add the 2024 static globe image
pdf.add_image("img/3d_globe_2024_static.png", "3D Globe: CO2 Emissions 2024 - Visualization Snapshot")

pdf.chapter_title("7. STATISTICAL CORRELATION ANALYSIS")
pdf.chapter_body("To identify the key drivers of CO2 emissions, a comprehensive correlation analysis was conducted on post-1990 data. The correlation matrix reveals the strength and direction of relationships between emissions and various socioeconomic indicators.\n\n"
"Key Findings:\n\n"
"1. GDP-Emission Relationship (r = 0.95+): A very strong positive correlation exists between economic output and CO2 emissions at the global level. This relationship, however, varies significantly by country development stage.\n\n"
"2. Population-Emission Correlation (r = 0.85+): Population size is strongly correlated with total emissions, though per capita metrics show wide variation across countries.\n\n"
"3. Energy-Emission Link (r = 0.90+): Primary energy consumption is perhaps the strongest predictor of emissions, highlighting the central role of energy systems in climate mitigation.\n\n"
"4. Decoupling Evidence: Advanced economies (US, Germany) show declining correlation strength in recent years, indicating successful partial decoupling of economic growth from emissions growth.\n\n"
"These correlations informed the selection of features for our predictive models and highlight the key intervention points for policy action.")
pdf.add_image("img/correlation_matrix.png", "Correlation Matrix of Key Variables")

pdf.add_page()
pdf.chapter_title("8. PREDICTIVE MODELING & FORECASTS")
pdf.section_title("8.1 Global Emission Forecast (2025-2028)")
pdf.chapter_body("Based on multivariate regression modeling and trend analysis, global CO2 emissions are projected to continue their gradual increase through 2028, absent major policy interventions or technological breakthroughs.\n\n"
"Forecast Methodology:\n"
"The forecast combines polynomial trend extrapolation for driving variables (GDP, population, energy) with the trained regression model to predict future emissions. Confidence intervals were calculated based on historical prediction errors.\n\n"
"Key Projections:\n"
"- 2025: Modest increase of 1-2% over 2024 levels\n"
"- 2026-2028: Continued gradual growth, with potential for plateau if current renewable energy expansion continues\n"
"- Cumulative 2025-2028: Approximately 145-155 billion tonnes of additional CO2\n\n"
"Uncertainty Factors:\n"
"Forecasts carry significant uncertainty due to:\n"
"- Geopolitical events affecting energy markets\n"
"- Speed of renewable energy deployment\n"
"- Policy changes (carbon pricing, regulations)\n"
"- Technological breakthroughs in clean energy or carbon capture")
pdf.add_image("img/global_forecast_multivariate.png", "Global CO2 Emissions Forecast (2025-2028)")

pdf.section_title("8.2 Country-Level Projections")
pdf.chapter_body("Individual country forecasts reveal divergent trajectories:\n\n"
"- China: Projection suggests potential peak and initial decline as renewable capacity offsets coal\n"
"- India: Continued growth expected as development proceeds, though growth rate may slow\n"
"- USA: Gradual decline projected to continue with ongoing coal-to-gas and renewable transitions\n"
"- Germany: Strong decline trajectory expected to accelerate with coal phase-out\n"
"- Russia: Relatively stable emissions projected, with modest variation\n"
"- Turkey: Moderate growth projected, with potential for faster reduction if renewable investment accelerates")
pdf.add_image("img/country_forecasts_multivariate.png", "Country-Specific Emission Forecasts")

pdf.chapter_title("9. PER CAPITA EMISSION ANALYSIS")
pdf.chapter_body("Examining per capita emissions provides crucial perspective on individual responsibility and development equity:\n\n"
"Current Per Capita Emissions (2024 estimates):\n"
"- United States: ~15 tonnes CO2 per person (highest among major economies)\n"
"- Russia: ~12 tonnes CO2 per person\n"
"- Germany: ~8 tonnes CO2 per person (declining)\n"
"- China: ~8 tonnes CO2 per person (now exceeding EU average)\n"
"- Turkey: ~5 tonnes CO2 per person\n"
"- India: ~2 tonnes CO2 per person (lowest, reflecting development stage)\n\n"
"Policy Implications:\n"
"The wide disparity in per capita emissions raises important questions about equitable burden-sharing in climate mitigation. Developing nations argue that their low per capita emissions justify continued growth, while developed nations face pressure to achieve deeper cuts given their historical responsibility and current high consumption levels.")
pdf.add_image("img/co2_per_capita_trend.png", "Per Capita CO2 Emissions by Country")

pdf.chapter_title("10. DEMOGRAPHIC DYNAMICS & EMISSIONS")
pdf.chapter_body("The relationship between population growth and emissions varies dramatically across countries, reflecting different development models and policy choices:")
pdf.add_image("img/pop_vs_co2_China.png", "China: Population vs CO2 Growth Index (2004=100)")
pdf.add_image("img/pop_vs_co2_United States.png", "USA: Population vs CO2 Growth Index (2004=100)")

pdf.add_page()
pdf.chapter_title("11. ENERGY MIX & CARBON INTENSITY")
pdf.section_title("11.1 Fossil Fuel Dependency Analysis")
pdf.chapter_body("The composition of fossil fuel consumption reveals distinct energy profiles that inform mitigation strategies:\n\n"
"Coal-Dominant Countries (China, India):\n"
"Coal represents the largest source of emissions (60-70% of fossil CO2). These countries face the greatest challenge in decarbonization, as coal is deeply embedded in industrial processes and power generation. However, both are also seeing rapid renewable deployment.\n\n"
"Oil-Dominant Countries (USA):\n"
"Transportation-sector oil consumption is the primary challenge. Electric vehicle adoption and efficiency standards are key levers.\n\n"
"Gas-Dominant Countries (Russia):\n"
"Natural gas, while cleaner than coal, still produces significant emissions. Russia's economy is heavily dependent on gas exports, creating complex incentive structures.\n\n"
"Mixed Profiles (Germany, Turkey):\n"
"These countries use significant amounts of all three fossil fuels, requiring comprehensive strategies addressing power generation, industry, transport, and heating.")
pdf.add_image("img/fossil_fuel_mix.png", "Fossil Fuel Emission Composition by Country")

pdf.section_title("11.2 Carbon Intensity Trends")
pdf.chapter_body("Carbon intensity (CO2 emissions per unit GDP) measures the 'greenness' of economic activity. Declining intensity indicates successful decoupling of economic growth from emissions:\n\n"
"Notable Trends:\n"
"- Global carbon intensity has declined approximately 35% since 1990\n"
"- China shows the fastest improvement rate, with intensity dropping over 60% despite massive emission growth\n"
"- Advanced economies maintain low, stable intensity levels\n"
"- Further intensity improvements are possible and necessary through energy efficiency and clean energy deployment")
pdf.add_image("img/carbon_intensity_trend.png", "Carbon Intensity (CO2/GDP) Trend Analysis")

pdf.chapter_title("12. POLICY RECOMMENDATIONS")
pdf.chapter_body("Based on the comprehensive analysis presented in this report, the following evidence-based policy recommendations are proposed for each analyzed country:\n\n"
"CHINA:\n"
"- Accelerate coal power phase-out while ensuring energy security\n"
"- Continue massive renewable energy deployment (solar, wind)\n"
"- Expand electric vehicle adoption and charging infrastructure\n"
"- Strengthen carbon market mechanisms and pricing\n\n"
"INDIA:\n"
"- Prioritize leap-frogging to renewable energy over coal expansion\n"
"- Implement aggressive solar and wind targets\n"
"- Develop clean cooking solutions to reduce biomass burning\n"
"- Invest in grid infrastructure for renewable integration\n\n"
"UNITED STATES:\n"
"- Strengthen federal climate policy and emissions standards\n"
"- Accelerate coal power plant retirements\n"
"- Expand electric vehicle incentives and infrastructure\n"
"- Invest in carbon capture technology for hard-to-abate sectors\n\n"
"GERMANY:\n"
"- Complete coal phase-out by 2030\n"
"- Expand renewable energy capacity and grid interconnections\n"
"- Develop green hydrogen for industrial applications\n"
"- Continue leadership in EU climate policy\n\n"
"RUSSIA:\n"
"- Diversify economy away from fossil fuel export dependence\n"
"- Improve domestic energy efficiency (significant potential)\n"
"- Reduce methane emissions from oil and gas operations\n"
"- Develop renewable resources in suitable regions\n\n"
"TURKEY:\n"
"- Accelerate domestic renewable energy development (excellent solar/wind potential)\n"
"- Reduce reliance on imported fossil fuels for energy security\n"
"- Implement carbon pricing mechanisms\n"
"- Improve building energy efficiency standards")

pdf.chapter_title("13. CONCLUSIONS")
pdf.chapter_body("This comprehensive analysis of global CO2 emissions yields several key conclusions:\n\n"
"1. Emissions Continue Rising: Despite growing awareness and policy efforts, global CO2 emissions continue to increase, driven primarily by developing economies. The brief COVID-19 dip demonstrated that only fundamental structural changes, not temporary disruptions, can achieve lasting reductions.\n\n"
"2. Divergent National Trajectories: The data reveals a clear divide between advanced economies successfully reducing emissions (US, Germany) and developing economies still experiencing growth (China, India, Turkey). Russia represents a unique case of economic maturity without significant emission reductions.\n\n"
"3. Decoupling is Possible: Several countries demonstrate that economic growth can continue while emissions decline, providing proof-of-concept for green growth strategies.\n\n"
"4. Energy System Transformation is Central: The analysis confirms that fossil fuel combustion, particularly coal, is the dominant source of emissions. Transforming energy systems to clean sources is the primary pathway to mitigation.\n\n"
"5. Predictive Models Provide Planning Value: While forecasts carry uncertainty, time-safe modeling approaches can provide useful guidance for policy planning and investment decisions.\n\n"
"6. Visualization Enhances Understanding: Interactive 3D visualizations make complex emission data accessible to broader audiences, supporting informed public discourse.\n\n"
"The urgency of climate action is underscored throughout this analysis. Without coordinated global efforts to accelerate clean energy deployment, improve efficiency, and phase out fossil fuels, emission trends will continue to exacerbate climate change impacts.")

pdf.chapter_title("14. REFERENCES & DATA SOURCES")
pdf.chapter_body("1. Our World in Data - CO2 and Greenhouse Gas Emissions Dataset\n"
"   Ritchie, H., Roser, M., & Rosado, P. (2024)\n"
"   https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions\n\n"
"2. Global Carbon Project - Annual Carbon Budget Reports\n"
"   Friedlingstein et al. (2023)\n"
"   https://www.globalcarbonproject.org/\n\n"
"3. IPCC Sixth Assessment Report (AR6)\n"
"   Intergovernmental Panel on Climate Change (2021-2023)\n\n"
"4. International Energy Agency - World Energy Outlook\n"
"   IEA (2024)\n\n"
"5. World Bank Development Indicators Database\n"
"   https://data.worldbank.org/")

pdf.output("CO2_Analysis_Report_Professional.pdf")
print("PDF created: CO2_Analysis_Report_Professional.pdf")
