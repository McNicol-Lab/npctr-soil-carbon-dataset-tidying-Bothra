# North Pacific Coastal Temperate Rainforest (NPCTR) Pedon and Soil Carbon Database

Access this dataset on Dryad: <https://doi.org/10.5061/dryad.5jf6j1r>

This README.md and the main database `McNicoletal-2024-NPCTR-Pedon-SOC-Database.xlsx` was substantially updated in August 2024 by [Aarin Bothra](https://github.com/AarinBothra). 

This database compiles pedon data and soil organic carbon stock data (ca. 1300 soil profile descriptions) from various sources across coastal British Columbia and southeast Alaska. 

## Description of the data and file structure

The file entitled *McNicoletal-2024-NPCTR-Pedon-SOC-Database.xlsx* contains the data for all of the soil pedons and coresponding soil organic carbon stock data. The file has four tables: a master table with all the data, a pedon table with pedon-specific data, a horizon table with horizon-specific data, and a summary table. 

*McNicoletal-2024-NPCTR-Pedon-SOC-Database.xlsx* contains the following columns:
*   source: source reference (see Source References tab) for the pedon data. In most cases these are published database data (e.g. Shaw et al. 2018), or published manuscripts, but includes one thesis and unpublished data from the Hakai Institute. 
*   pedon_id: this is the identifer extracted from the source reference. In many cases these are named pedon locations, but sometimes they are pedon codes (e.g. NRCS data) or numeric identifiers (e.g. Shaw et al. 2018).
*   order: this is the soil order using the fullest taxonomic classification available in the source reference. It has not yet been simplified for aggregation, down to the singular order designations (e.g. HISTOSOL).
*   lat: the most accurate latitude value reported for the pedon location.
*   lon: the most accurate longitude value reported for the pedon location.
*   latlon_q: the quality flag for the LAT and LON values based upon criteria described in the manuscript (doi: 10.1088/1748-9326/aaed52). Generally, too few decimal places (low precision), obvious inaccuary, or pre-gps sampling received LOW.
*   horizon: the detailed horizon designation from the source reference with as many suffixes (e.g. Bh…) as was reported.
*   horizon_number: indicates the order of horizons within the master table. A horizon can be uniquely identified using its pedon id and horizon number. 
*   horizon_type: organic or mineral horizon.
*   depth2: the depth of the top of the soil horizon.
*   depth1: the depth of the bottom of the soil horizon.
*   depth: the depth of the soil horizon (DEPTH2-DEPTH1)
*   bulk_density: the measured or estimated/assigned (in beige) dry bulk density value in g cm-3. The Supplementary Information provides a breakdown of steps to estimate bulk density. Most values are taken from Shaw et al. 2015 (Table 8).
*   bd_method: whether the assigned value was measured or estimated. 0 indicates that the value is measured. 1 indicates that the value is estimated using a lookup table. This procedure was replicated to fill data gaps in multiple datasets. (More information in manuscript supplement).
*   cf: the mineral coarse fragment content in percent. Generally these values are reported, but where filled, they are highlighted and the Supplementay Information explains how.
*   cf_method: whether the assigned value was measured or estimated. 0 indicates that the value is measured. 1 indicates that the value is estimated using a lookup table or other methods. This procedure was replicated to fill data gaps in multiple datasets. (More information in manuscript supplement). 2 indicates that the cf was originally null and 0 was assumed for calculation purposes. 
*   cconc: the reported or estimated horizon carbon concentration. Where estimated, these values are highlighted in color and source reference-specific methods are described in Supplementary Info.
*   cconc_method: whether the assigned value was measured or estimated. 0 indicates that the value is measured. 1 indicates that the value is estimated using a lookup table or other methods. This procedure was replicated to fill data gaps in multiple datasets. 2 indicates that the cconc was estimated using linear regression. (More information in manuscript supplement).  
*   mineral_d: the deepest depth of the subsurface mineral horizons (maximum value 100 cm). 
*   ff_d: the total depth of forest floor organic horizons or Histosol depth (no maximum value).
*   total_d: the total depth of soil accounted for in SOC stock estimate (Mineral_D + FF_D).
*   ccontent: calculated carbon content (g C m-2) for the horizon.
*   total_c: summed carbon content across all reported horizons. (g C m-2)
*   ccontent_1m: calculated carbon content (g C) for the horizon. Horizons below 100 cm in the subsurface mineral soil are assigned zero, while horizons that traverse this threshold are reduced proportionally by the fraction of the horizon below it.
*   total_c_1m: summed carbon content across all reported horizons down to 1 m in the subsurface mineral soils and 1 m in histosols.  (Mg C ha-1)
*   pedon_start: a boolean value which, if true, indicates that the row contains pedon-specific data and is the master row for that pedon.

The value "NA" correspond to any missing information in columns of type *object*. For columns that are *float64* or *int*, any empty cells represent missing information. 

## Version changes
**18-aug-2024:** The original database was updated and cleaned using Python Pandas to create a standardized database that combined all data sources into one. Along with all of the original data characteristics, the database now denotes how missing data was gap-filled and includes other added columns to create a more user-friendly experience. The database includes four tables: a master table, a pedon-specific table, a horizon-specific table, and a summary table. References, acknowledgments, and field descriptors can be found within *McNicoletal-2024-NPCTR-Pedon-SOC-Database.xlsx* and *README.md* file. The original data and the script used to clean the data can be found on GitHub (see below).

## Sharing/Access information

Links to other publicly accessible locations of the data.

Raw and Cleaned Data and Code can be found on Github:
 - Github: <https://doi.org/10.5061/dryad.5jf6j1r>

Sources from which the data was derived can be found in *McNicoletal-2024-NPCTR-Pedon-SOC-Database.xlsx* and the primary article:
 - Primary article: <https://doi.org/10.1088/1748-9326/aaed52>
