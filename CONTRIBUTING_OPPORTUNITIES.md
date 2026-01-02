# Contributing Opportunities to the Transition Valuation Project

This document outlines potential alternative data sources and contribution opportunities for the input files used by the `value-factors` submodule, based on a comprehensive analysis of existing data, research from Nature and SSRN, and the project's overall goals. This aims to guide researchers, analysts, and developers in enhancing the project's data quality, granularity, and methodological robustness.

---

## Structure of the `value-factors` Input Data

The `value-factors` submodule (located in the `value-factors/` directory) contains Python scripts that calculate environmental and social value factors. These scripts rely on various input files, typically located in `value-factors/input_data/`. The goal is to process these inputs to generate monetized damage/benefit coefficients across countries and economic sectors.

Each primary input file is used by a specific `prepare_*.py` script within the `value-factors/` folder.

---

## Input Files: Alternatives and Contribution Opportunities

This section details each input file, its corresponding generator script, potential alternative data sources, how to acquire and transpose such data, and specific opportunities for contribution to the project.

### 1. `value-factors/input_data/241001_worldbank_deflator/241001_worldbank_deflator.h5`

*   **Generator Script:** Used by all `prepare_*.py` scripts in `value-factors/` (e.g., `007_241001_prepare_Waste_my.py`, `020_241024_prepare_GHG_my.py`).
*   **Current Data Source:** World Bank GDP deflator, used for inflation adjustment across years.
*   **Assessment:** The World Bank is a primary and highly reputable source for GDP deflator data. However, other international organizations also provide similar data, which might offer different methodologies or extended historical series.
*   **Alternative Data Sources:**
    *   **International Monetary Fund (IMF):** Provides its own comprehensive GDP data, including deflators.
        *   **URL:** [IMF Data Portal](https://data.imf.org/search?q=gdp%20deflator)
    *   **Organisation for Economic Co-operation and Development (OECD):** Maintains extensive economic datasets, including GDP deflators.
        *   **URL:** [OECD Data Portal](https://data.oecd.org/price-inflation/gdp-deflator.htm)
    *   **National Statistical Offices/Central Banks:** Primary sources for highly detailed, country-specific GDP data.
*   **How to Get Data from Alternatives:**
    *   Data can typically be downloaded from the respective online portals in various formats (e.g., CSV, Excel). Users can utilize their data explorers to select specific countries, years, and series.
*   **How to Transpose to Current Format:**
    *   A Python script would be needed to:
        1.  Read the downloaded file (e.g., CSV).
        2.  Process the data to ensure consistency (e.g., unit, base year, currency if applicable).
        3.  Pivot the data to a format where countries are rows and years are columns (or vice versa, aligning with the expected input structure).
        4.  Save the resulting DataFrame to an HDF5 file, mirroring the structure of the existing `241001_worldbank_deflator.h5` file.
*   **Contribution Opportunities:**
    *   **Methodological Comparison & Options:** Research how IMF or OECD deflator methodologies differ from the World Bank's. Contribute an option within the configuration to switch between different deflator sources, allowing for sensitivity analysis based on different inflation assumptions.
    *   **Historical Data Extension:** Investigate if alternative sources offer longer historical data series that could extend the project's temporal scope for more robust trend analysis.

---

### 2. `value-factors/input_data/20241022_scc_nordhaus/20241022_scc_nordhaus.h5` (Social Cost of Carbon)

*   **Generator Script:** `020_241024_prepare_GHG_my.py`
*   **Current Data Source:** Nordhaus DICE model, providing a single global SCC value.
*   **Assessment:** A foundational model, but more granular (country-level) and updated SCC estimates are available.
*   **Alternative Data Source:** "Country-level Social Cost of Carbon" database by Ricke et al. (2018). This dataset provides country-specific SCC estimates across various scenarios.
*   **How to Get Data from Alternatives:**
    *   The data (`cscc_db_v2.csv`) is available from the [country-level-scc/cscc-database-2018 GitHub repository](https://github.com/country-level-scc/cscc-database-2018).
*   **How to Transpose to Current Format:**
    *   A Python script is required to:
        1.  Read the CSV file.
        2.  Filter the data to select desired scenarios (e.g., `bhm_lr` run, `expected` climate, `SSP1`, `rcp45`) and discount rates (e.g., 3%).
        3.  Handle data inconsistencies, such as duplicate entries for countries (e.g., by selecting the first occurrence).
        4.  Convert units (e.g., from $/t CO2e to $/kg).
        5.  Save the processed data into the required HDF5 and Excel formats.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature:** Recent research (e.g., from the Climate Impact Lab) published in *Nature* often suggests higher SCC estimates than older models, indicating a greater urgency for climate action. Studies also highlight the importance of country-level SCC.
    *   **SSRN:** Hosts numerous papers on SCC methodologies, including discussions on global vs. domestic SCC (Kotchen, 2018), simplified calculation models (Newbold et al.), and comprehensive literature reviews (Tol, 2008, 2011).
*   **Contribution Opportunities:**
    *   **Scenario Expansion:** Implement options within the configuration (e.g., `config.yaml`) to allow users to select different scenarios (e.g., `SSP`, `RCP`, `prtp`, `eta`) from the Ricke et al. dataset, enabling more nuanced analysis.
    *   **Integration of Latest Research:** Incorporate findings from the latest academic literature on SCC (e.g., from *Nature* or SSRN) to continuously update and refine the SCC estimates used in the project. This would involve adapting the data processing logic to new data structures.
    *   **Sensitivity Analysis Tool:** Develop a utility or an extension to the script that allows for easy sensitivity analysis of the SCC to different discount rates or other key parameters, demonstrating the range of potential impact valuations.

---

### 3. `value-factors/input_data/220707_Air_pollution_update/220707_Air pollution_update.xlsx`

*   **Generator Script:** `008_241001_prepare_AirPollution_my.py`
*   **Current Data Source:** Pre-calculated air pollution health damage costs, likely from the German Environment Agency (UBA) or similar source, with inherent assumptions for geographical distribution.
*   **Assessment:** This data is highly specialized and pre-processed, representing monetized damage costs rather than raw emissions or exposure data. Replacing it requires significant methodological work.
*   **Alternative Data Sources:**
    *   **World Bank:** Provides country-level PM2.5 exposure data (micrograms per cubic meter).
        *   **URL:** [World Bank Open Data - PM2.5 air pollution](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)
    *   **German Environment Agency (UBA):** Publishes "Methodological Convention for Estimating Environmental Costs" which includes cost rates for various air pollutants (PM2.5, PM10, NOx, SO2, NMVOC, NH3).
        *   **URL:** [UBA Publications on Methodological Conventions](https://www.umweltbundesamt.de/en/topics/economics-consumption/environmental-economic-accounting/environmental-damage-costs) (Note: Specific PDF links can change, search UBA site for "Methodological Convention" and version number like "3.1" or "3.2").
*   **How to Get Data from Alternatives:**
    *   World Bank data is downloadable from their Open Data portal. UBA documents are typically available as PDF publications on their website.
*   **How to Transpose to Current Format (Highly Complex):** This is not a straightforward data transposition. It requires implementing a sophisticated modeling approach:
    1.  **Data Harmonization:** Aligning World Bank exposure data with UBA cost rates (which are often per tonne of emission, not per unit of exposure). This may necessitate finding or developing emission factors per unit of economic activity or population.
    2.  **Impact Pathway Modeling:** Developing or acquiring a model that translates air pollution exposure/emissions into health impacts (e.g., premature mortality, morbidity) using concentration-response functions.
    3.  **Economic Valuation:** Applying economic valuation techniques (e.g., Value of Statistical Life/Years, Willingness to Pay) to monetize these health impacts.
    4.  **Geographical Disaggregation:** Reconciling country-level exposure with potentially more granular UBA cost rates, or developing methods for spatial downscaling of costs.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Research in these outlets often provides high-level economic overviews of air pollution impacts and discussions of valuation methodologies rather than ready-to-use datasets. They highlight the complexity of quantifying health damage costs and the need for robust models.
*   **Contribution Opportunities:**
    *   **Methodology Implementation (Specialized):** For users with expertise in environmental modeling or economics, a significant contribution would be to implement a new `prepare_*.py` script that performs the full calculation from raw exposure data (e.g., World Bank) and UBA cost rates to generate the damage coefficients. This is a research-level task.
    *   **Geographical Refinement:** Research methods to refine the geographical assumptions inherent in global or national-level damage cost estimates, possibly integrating local air quality data.

---

### 4. `value-factors/input_data/220509_Waste_figures_merged_update/220509_Waste figures merged_update.xlsx`

*   **Generator Script:** `007_241001_prepare_Waste_my.py`
*   **Current Data Source:** Pre-processed academic research, with specific categories (hazardous/non-hazardous, incinerated/landfill/recovered) and geographical assumptions.
*   **Assessment:** Extremely specific and highly granular data, making a direct replacement very challenging without replicating the original research methodology.
*   **Alternative Data Sources:**
    *   **OECD/Eurostat:** May offer aggregated waste management statistics (generation, treatment types), but likely not monetized damage costs per category and country.
    *   **National Environmental Agencies:** Could provide country-specific waste data and sometimes cost estimates, but harmonization would be difficult.
*   **How to Get Data from Alternatives:** Requires extensive search across national and international environmental statistics databases.
*   **How to Transpose to Current Format (Very Complex):** This involves:
    1.  Finding granular data for waste generation and treatment by hazardousness.
    2.  Developing methodologies to calculate specific damage costs (e.g., greenhouse gas emissions from incineration, leachate pollution from landfill, resource depletion from non-recovery).
    3.  Harmonizing data across numerous countries and economic sectors.
    4.  Structuring the data into the four-sheet format (or similar) used by the existing script.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Research typically focuses on life cycle assessments of waste management systems, economic models for internalizing waste externalities, or specific waste streams. Direct, universally applicable damage cost datasets are rare.
*   **Contribution Opportunities:**
    *   **Literature Review & Data Synthesis:** Conduct a comprehensive review of academic and institutional research on waste damage costs. Synthesize findings to propose a new, transparent methodology and identify suitable data proxies.
    *   **Methodology Development:** For experts, develop a script that implements a new, more transparent methodology for calculating waste damage coefficients based on publicly available data, possibly for a subset of waste types or countries.

---

### 5. `value-factors/input_data/220511_Water_consumption_update/220511_Water consumption_update.xlsx`

*   **Generator Script:** `009_241001_prepare_WaterConsumption_my.py`
*   **Current Data Source:** Experimental academic research with high uncertainty, providing "Total damages" for blue water consumption.
*   **Assessment:** The "experimental" nature suggests the methodology might be novel or less widely accepted, making replication or finding direct alternatives difficult.
*   **Alternative Data Sources:**
    *   **World Resources Institute's AQUEDUCT:** Provides data on water risk, scarcity, and stress by basin.
        *   **URL:** [WRI Aqueduct Water Risk Atlas](https://www.wri.org/applications/aqueduct/water-risk-atlas/)
    *   **Academic Databases:** Research on the economic valuation of water scarcity, water footprint, or blue water consumption impacts.
*   **How to Get Data from Alternatives:** AQUEDUCT data is downloadable. Academic papers would require extracting methodologies and potentially localized data.
*   **How to Transpose to Current Format (Complex):**
    1.  **Methodology Development:** A robust methodology is needed to translate water risk or scarcity metrics (e.g., from AQUEDUCT) into monetary damage costs for blue water consumption.
    2.  **Data Mapping:** Map basin-level AQUEDUCT data to country and sector-level economic activities.
    3.  **Modeling:** Develop a script to implement this methodology and calculate "Total damages" per country.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Papers often discuss the economic impacts of water scarcity (especially droughts), the concept of water externalities, and methods for valuing water resources. Direct monetary damage costs per unit of water consumption are less common as readily available datasets.
*   **Contribution Opportunities:**
    *   **Robust Methodology for Water Valuation:** Contribute by researching and implementing a more transparent and widely accepted methodology for valuing water consumption damages, potentially utilizing WRI AQUEDUCT data or other global water stress indicators.
    *   **Uncertainty Analysis:** Develop tools to analyze and communicate the high uncertainty associated with water consumption damage cost estimates.

---

### 6. `value-factors/input_data/230317_Landuse_update_ZK/230317_Landuse_update_ZK.xlsx`

*   **Generator Script:** `010_241001_prepare_LandUse_my.py`
*   **Current Data Source:** Pre-processed data, specific to the WifOR methodology, for habitat conversion and ecosystem impacts.
*   **Assessment:** Similar to waste, this data is highly specific and likely derived from a complex, proprietary methodology.
*   **Alternative Data Sources:**
    *   **OECD:** May have data on land use change, land cover, and related environmental pressures.
    *   **The Economics of Ecosystems and Biodiversity (TEEB):** A global initiative that publishes reports and data on ecosystem service valuation.
        *   **URL:** [TEEB Reports and Publications](http://www.teebweb.org/resources/teeb-reports/)
    *   **Academic Databases:** Research on the economic valuation of ecosystem services due to land use change.
*   **How to Get Data from Alternatives:** Data from OECD or TEEB reports would need to be extracted and potentially harmonized.
*   **How to Transpose to Current Format (Complex):** This would require:
    1.  Identifying relevant ecosystem services affected by land use change (e.g., biodiversity, soil quality, carbon sequestration).
    2.  Finding methodologies and data to monetize the damage costs associated with the degradation or loss of these services.
    3.  Mapping these damages to specific land use types, countries, and NACE sectors.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Research emphasizes the importance of land use planning for mitigating damage costs, especially in climate change adaptation (e.g., flood protection). Papers also discuss the estimation of marginal damage costs associated with the loss of ecosystem services due to land-use change.
*   **Contribution Opportunities:**
    *   **Ecosystem Service Valuation Module:** Develop a dedicated module that implements a recognized ecosystem service valuation methodology (e.g., based on TEEB frameworks) to derive land use damage costs from publicly available land cover and economic data.
    *   **Spatial Data Integration:** Explore the use of spatial data (GIS) for more granular land use impact assessments.

---

### 7. `value-factors/input_data/230324_WaterPollution_Mon_Coef_Final_DC/230324_WaterPollution_Mon_Coef_Final_DC.xlsx`

*   **Generator Script:** `013_241014_prepare_WaterPol_my.py`
*   **Current Data Source:** Experimental and pre-processed coefficients for various water pollutants (nitrogen, phosphorus, heavy metals).
*   **Assessment:** Similar to water consumption, the "experimental" nature suggests a complex and potentially less standardized methodology.
*   **Alternative Data Sources:**
    *   **World Bank/WHO:** May have data on water quality parameters and health impacts related to water pollution.
    *   **EPA (US), EEA (Europe), National Environmental Agencies:** Provide data on water quality standards, pollutant levels, and sometimes economic valuations of pollution.
*   **How to Get Data from Alternatives:** Requires extracting data from various reports and databases from environmental agencies.
*   **How to Transpose to Current Format (Very Complex):** This involves:
    1.  Identifying specific pollutants and their impact pathways on human health and ecosystems.
    2.  Finding methodologies and data to quantify and monetize these impacts per unit of pollutant emitted or per level of concentration.
    3.  Mapping these to countries and economic sectors.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Research typically covers the health, ecological, and economic consequences of water pollution, and methodologies for assessing damage costs (e.g., through sewage treatment costs, or averted market costs). Direct, broad-scale damage cost datasets are generally not available.
*   **Contribution Opportunities:**
    *   **Pollutant-Specific Modeling:** Develop models for specific water pollutants (e.g., nitrogen, heavy metals) to calculate damage costs based on publicly available data on emissions, water quality, and health impacts.
    *   **Comparative Methodology:** Implement and compare different methodologies for valuing water pollution damages.

---

### 8. `value-factors/input_data/220529_training_value_per_hour_bysector/220529_training_value_per_hour_bysector.h5`

*   **Generator Script:** `014_241016_prepare_Training_my.py`
*   **Current Data Source:** Data on "training value per hour by sector," based on "return to education research" with open methodological questions.
*   **Assessment:** Highly specific data point (monetary value per hour of training, disaggregated by country and sector) that requires complex econometric modeling to derive.
*   **Alternative Data Sources:**
    *   **OECD Programme for the International Assessment of Adult Competencies (PIAAC):** Provides data on adult skills and their economic outcomes.
        *   **URL:** [OECD PIAAC Data](https://www.oecd.org/skills/piaac/data/)
    *   **International Labour Organization (ILO):** Offers statistics on wages, employment, and education levels.
        *   **URL:** [ILOSTAT Database](https://www.ilo.org/ilostat-web/welcome/home.do)
    *   **National Labor Statistics Agencies:** Provide detailed country-specific data on wages, education, and employment by sector.
*   **How to Get Data from Alternatives:** Data can be extracted from PIAAC reports, ILOSTAT, or national agency websites.
*   **How to Transpose to Current Format (Complex):** This would involve:
    1.  Finding granular data on returns to education or vocational training, disaggregated by country and sector.
    2.  Developing a robust econometric model to convert these returns into a "value per hour of training" that accounts for various factors (e.g., skill premiums, productivity gains).
    3.  Making explicit assumptions to address any data gaps or methodological questions.
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Research emphasizes the importance of human capital and the economic returns to education and training. However, direct datasets with monetized "value per hour of training" at the required granularity are not common, and the focus is more on the macro- or individual-level returns rather than a standardized damage/benefit coefficient.
*   **Contribution Opportunities:**
    *   **Econometric Modeling:** For experts in labor economics or econometrics, contribute by developing a new `prepare_*.py` script that implements a transparent and robust econometric model to estimate the "value per hour of training" using publicly available data from OECD, ILO, or national sources.
    *   **Methodological Clarification:** Contribute by addressing the "open methodological questions" through a clear, documented approach.

---

### 9. `value-factors/input_data/220616_monetization_value_per_incident_NEW/220616_monetization_value_per_incident_NEW.xlsx`

*   **Generator Script:** `015_241016_prepare_OHS_my.py`
*   **Current Data Source:** Data on monetized occupational health and safety (OHS) damage coefficients, based on the Value of a Statistical Life (VSL) and implicit values for non-fatal incidents.
*   **Assessment:** While VSL is a well-established concept, obtaining comprehensive, disaggregated data for both fatal and non-fatal incidents (injuries and illnesses) by country and sector is challenging.
*   **Alternative Data Sources:**
    *   **OECD:** Provides VSL estimates for many countries.
        *   **URL:** [OECD - Environmental Health and Safety Publications](https://www.oecd.org/chemicalsafety/risk-assessment/) (search for VSL related documents).
    *   **World Health Organization (WHO):** May provide VSL estimates or methodologies.
        *   **URL:** [WHO Publications](https://www.who.int/publications) (search for VSL or health economic valuation).
    *   **International Labour Organization (ILO):** Publishes statistics on occupational accidents and diseases, sometimes with economic cost estimates.
        *   **URL:** [ILOSTAT Database](https://www.ilo.org/ilostat-web/welcome/home.do)
    *   **National Health and Safety Agencies:** Provide country-specific data on incident rates and associated costs.
*   **How to Get Data from Alternatives:** Data can be found in reports and databases from these organizations.
*   **How to Transpose to Current Format (Complex):** This involves:
    1.  **VSL Data:** Sourcing country-specific VSL data.
    2.  **Non-Fatal Incident Costs:** Identifying methodologies and data for the monetary cost of non-fatal injuries and illnesses (which is often less standardized than VSL).
    3.  **Data Integration & Disaggregation:** Combining these datasets and disaggregating by sector if required, ensuring consistency with the existing structure (Fatal/Non-fatal, Injury/Illness).
*   **Relevant Research (Nature/SSRN):**
    *   **Nature/SSRN:** Research discusses the economic costs of occupational incidents (direct, indirect, human, societal) and challenges in quantification. Papers often focus on methodological advancements or specific case studies rather than readily available, granular global datasets of monetized damage costs per incident.
*   **Contribution Opportunities:**
    *   **Comprehensive OHS Cost Model:** Develop a new `prepare_*.py` script that integrates publicly available VSL data with robust methodologies for estimating the costs of non-fatal incidents, disaggregated by country and sector.
    *   **Data Harmonization:** Focus on harmonizing OHS data from multiple international and national sources to create a more comprehensive input.

---

### 11. `value-factors/input_data/Model_definitions_owntable/Model_definitions_owntable.h5`

*   **Generator Script:** Used by all `prepare_*.py` scripts in `value-factors/`.
*   **Current Data Source:** Model-specific definitions, including lists of countries (ISO3 codes) and NACE economic sectors.
*   **Assessment:** This file is fundamental to the internal structure and functioning of the WifOR model. It defines the universe of entities (countries and sectors) the model operates on and cannot be replaced with an external alternative without fundamentally altering the model.
*   **Alternative Data Sources:** Not applicable for direct replacement.
*   **How to Get Data from Alternatives:** Not applicable.
*   **How to Transpose to Current Format:** Not applicable.
*   **Relevant Research (Nature/SSRN):** Not directly applicable, as this is a model internal definition.
*   **Contribution Opportunities:**
    *   **Expansion of Definitions:** Research and propose additions to the country list (e.g., more granular sub-national regions) or NACE sector classification (e.g., more detailed sub-sectors), with clear justifications for the changes and how they align with international standards. This would require updating the HDF5 structure.
    *   **Mapping Tools:** Develop tools or documentation that map alternative classification systems (e.g., ISIC, GICS) to the NACE sectors used in the project, enhancing interoperability.

---

## General Contribution Opportunities

Beyond specific data replacements, here are broader ways to contribute:

*   **Code Modernization and Best Practices:** Review existing scripts for opportunities to implement more modern Python practices, improve performance, and enhance readability (e.g., leveraging `pandas` functionalities more efficiently).
*   **Automated Data Acquisition:** Develop scripts or tools that automate the download and initial parsing of data from identified online sources (e.g., using APIs where available, or web scraping with appropriate ethical considerations).
*   **Testing and Validation:** Expand the test suite for existing and new scripts to ensure data integrity, methodological correctness, and consistency of outputs.
*   **Documentation Refinement:** Continuously improve all project documentation, focusing on clarity, completeness, and ease of understanding for new contributors.
*   **Educational Materials:** Create tutorials, examples, or case studies demonstrating how to use the `value-factors` submodule with alternative data or how to extend its functionalities.

By focusing on these areas, contributors can significantly enhance the robustness, applicability, and user-friendliness of the Transition Valuation project.

This document will be saved as `CONTRIBUTING_OPPORTUNITIES.md` in the `tvp1` root directory.
