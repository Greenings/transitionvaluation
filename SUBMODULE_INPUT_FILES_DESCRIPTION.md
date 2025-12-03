# Input Files Overview and Methodological Origins for WifOR Value Factors

This document provides a comprehensive overview of the input files used within the WifOR Impact Valuation framework, detailing their origins and the underlying methodologies (the "drafting" process) that produce the data.

## General Origin and Framework

The input files are an integral part of a sophisticated framework developed by the **WifOR Institute**, an independent economic research institute. The primary objective is to facilitate **Impact Valuation**, which involves monetizing the environmental and social impacts of various business activities.

The foundational principles guiding the origin and development of this data are:

*   **Value to Society Perspective**: All valuations prioritize capturing the holistic costs and benefits to society, extending beyond mere financial implications for businesses.
*   **Damage Cost Approach**: The predominant method involves estimating the monetary costs associated with the damages caused by a particular activity (e.g., health expenditures due to pollution). Where direct damage cost estimation is infeasible, alternative approaches such as "abatement cost" (the expense of preventing damage) or "willingness-to-pay" are employed.
*   **Academic and Institutional Foundation**: The methodologies are meticulously constructed upon research from authoritative bodies and academic institutions, including the German Federal Environment Agency (UBA), the World Health Organization (WHO), the Intergovernmental Panel on Climate Change (IPCC), and various peer-reviewed academic studies.
*   **Transparency**: A core tenet of WifOR's approach is transparency. All methodologies and their respective sources are thoroughly documented and publicly shared to foster open discussion and contribute to standardization efforts in impact valuation.

The input files therefore encapsulate the outcomes of these rigorous valuation exercises, presenting pre-calculated costs, coefficients, and data models. These serve as the essential "ingredients" that the Python scripts in this project utilize to compute the final monetized impact factors.

## Detailed Origin and Methodology ("Drafting" Process) by Input File Category

Below is a breakdown for each significant category of input file, elaborating on its origin and the specific methodological process used to generate its data.

### 1. Greenhouse Gases (GHG)

*   **Input File**: `20241022_scc_nordhaus.h5`
*   **Origin**: The data is derived from the **DICE model**, a renowned integrated assessment model. This particular dataset is based on the 2024 iteration of the model, developed by Barrage and Nobel laureate William Nordhaus.
*   **"Drafting" Process**: This file contains the **Social Cost of Carbon (SCC)**, which is a damage cost estimate quantifying the future economic harm resulting from emitting an additional ton of CO2 today. The value is globally consistent, as the impact of GHGs is global, irrespective of emission location. The methodology document outlines the specific assumptions from the DICE model that underpin these calculations, including the chosen social discount rate (e.g., 2%) for valuing future damages.

#### Public Databases
*   **DICE Model**: [http://www.williamnordhaus.com/dice-rice-models](http://www.williamnordhaus.com/dice-rice-models)

### 2. Air Pollution

*   **Input File**: `220707_Air pollution_update.xlsx`
*   **Origin**: The valuation methodology adheres to the recommendations of the **German Federal Environment Agency (UBA)**. The foundational data is sourced from **NEEDS**, a comprehensive EU project.
*   **"Drafting" Process**: This methodology employs a damage cost approach to monetize four distinct categories of harm:
    1.  **Health Damages**: Monetary costs associated with respiratory and cardiovascular diseases.
    2.  **Biodiversity Loss**: Costs linked to the reduction in biodiversity, including species extinction.
    3.  **Crop Damages**: Economic losses incurred due to diminished agricultural yields.
    4.  **Material Damages**: Costs related to the corrosion and aesthetic degradation of infrastructure and buildings.
    The Excel file contains these pre-calculated damage costs per ton for various pollutants (e.g., PM2.5, NOx). These costs are subsequently adjusted for different countries, considering factors such as population density, following detailed methodological guidelines.

#### Public Databases
*   **German Federal Environment Agency (UBA)**: [https://www.probas.umweltbundesamt.de/](https://www.probas.umweltbundesamt.de/)
*   **NEEDS Project (CORDIS)**: [https://cordis.europa.eu/project/id/502687](https://cordis.europa.eu/project/id/502687)
*   **NEEDS Database (openLCA)**: [https://www.openlca.org/project/needs/](https://www.openlca.org/project/needs/)

### 3. Waste

*   **Input File**: `220509_Waste figures merged_update.xlsx`
*   **Origin**: This category utilizes a mixed-method approach, integrating data from diverse sources including the **Intergovernmental Panel on Climate Change (IPCC)**, **EXIOPOL** (a European Union project), and **PricewaterhouseCoopers (PwC)**.
*   **"Drafting" Process**: The valuation disaggregates impacts by type:
    *   **Air Emissions & GHG**: Damage costs are calculated for pollutants released during waste incineration and greenhouse gases emitted from landfills.
    *   **Disamenity**: The reduction in property values around waste management sites is estimated using a "willingness-to-pay" (hedonic pricing) method.
    *   **Leachate**: The costs associated with soil and water contamination are estimated through a risk-based model (HARAS), based on clean-up expenses.
    The Excel file aggregates these pre-calculated costs for the various waste-related impacts.

#### Public Databases
*   **IPCC Emission Factor Database**: [https://www.ipcc-nggip.iges.or.jp/EFDB/main.php](https://www.ipcc-nggip.iges.or.jp/EFDB/main.php)
*   **IPCC Data Distribution Centre**: [https://www.ipcc-data.org/](https://www.ipcc-data.org/)
*   **EXIOBASE**: [https://www.exiobase.eu/](https://www.exiobase.eu/)

### 4. Water Consumption

*   **Input File**: `220511_Water consumption_update.xlsx`
*   **Origin**: This combines economic damage models from academic research (Ligthart & van Harmelen, 2019) with human health impact assessments (Debarre et al., 2022).
*   **"Drafting" Process**: Valuation is conducted across two primary dimensions:
    1.  **Economic Damages**: This quantifies the agricultural output lost due to water scarcity. It leverages a global "shadow price" for water, which is then refined for local conditions using country-specific **AWARE** factors.
    2.  **Health Damages**: The impact of domestic water deprivation on human health is measured in **Disability-Adjusted Life Years (DALYs)**, subsequently converted into a monetary value.

#### Public Databases
*   **AWARE Model**: [https://wulca-waterlca.org/aware/](https://wulca-waterlca.org/aware/)

### 5. Land Use

*   **Input File**: `230317_Landuse_update_ZK.xlsx`
*   **Origin**: The foundational methodology is the **Environmental Priority Strategies (EPS)** system, originally developed in 1992 and updated in 2015.
*   **"Drafting" Process**: This values the impacts of converting natural land to various other uses (e.g., agriculture, urban development). It monetizes effects on:
    *   Working capacity (e.g., due to the urban heat island effect).
    *   Drinking water treatment costs.
    *   Crop growth capacity.
    *   Biodiversity preservation costs.
    These values are then customized for specific countries using **LANCA** characterization factors.

#### Public Databases
*   **Environmental Priority Strategies (EPS)**: [https://lifecyclecenter.se/projects/eps-environmental-priority-strategies-in-product-development/](https://lifecyclecenter.se/projects/eps-environmental-priority-strategies-in-product-development/)
*   **LANCA**: [https://www.ibp.fraunhofer.de/en/expertise/life-cycle-engineering/applied-methods/lanca.html](https://www.ibp.fraunhofer.de/en/expertise/life-cycle-engineering/applied-methods/lanca.html)

### 6. Water Pollution

*   **Input File**: `230324_WaterPollution_Mon_Coef_Final_DC.xlsx`
*   **Origin**: The methodology is primarily based on the extensive work of **Steen (2020)** for valuing specific substances (e.g., Nitrogen, Phosphorus), complemented by the **USEtox model** for other pollutants.
*   **"Drafting" Process**: This approach quantifies the damage costs of various pollutants (e.g., Nitrogen, Phosphorus, heavy metals) on freshwater ecosystems. The impacts assessed include biodiversity loss, reduced fish production capacity, and detrimental effects on human health. Global values are regionalized by incorporating a country's water scarcity level as a scaling factor.

#### Public Databases
*   **USEtox Model**: [https://usetox.org](https://usetox.org)

### 7. Training

*   **Input File**: `220529_training_value_per_hour_bysector.h5`
*   **Origin**: The methodology is grounded in academic literature concerning the economic **returns to schooling** (Psacharopoulos & Patrinos, 2018).
*   **"Drafting" Process**: Corporate training is conceptualized as an investment in human capital. The process involves estimating the percentage increase in productivity resulting from one hour of training (approximated from the return on one year of schooling) and projecting this increase over an employee's remaining working life. This capital-centric perspective mirrors the valuation of tangible assets.

#### Public Databases
*   **OECD Education Data**: [https://www.oecd.org/education/data/](https://www.oecd.org/education/data/)
*   **Nationmaster Education Statistics**: [https://www.nationmaster.com/country-info/stats/Education](https://www.nationmaster.com/country-info/stats/Education)

### 8. Occupational Health & Safety (OHS)

*   **Input File**: `220616_monetization_value_per_incident_NEW.xlsx`
*   **Origin**: The methodology is rooted in principles of health economics, leveraging data from **Eurostat** and the **Global Burden of Disease** study.
*   **"Drafting" Process**: Health impacts stemming from occupational injuries and illnesses are converted into **Disability-Adjusted Life Years (DALYs)**.
    *   For **fatal incidents**, this measures the "years of life lost" due to premature mortality.
    *   For **non-fatal incidents**, this quantifies the "years lived with a disability."
    These DALYs are then translated into a monetary value using a standard coefficient for a year of healthy life (e.g., $200,000), yielding the final impact cost.

#### Public Databases
*   **Eurostat - Health and safety at work**: [https://ec.europa.eu/eurostat/web/health/health-safety-work](https://ec.europa.eu/eurostat/web/health/health-safety-work)
*   **Global Burden of Disease (GBD) Study**: [https://www.healthdata.org/gbd](https://www.healthdata.org/gbd)
