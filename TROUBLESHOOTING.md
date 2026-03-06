# Troubleshooting Guide

**All Three Value Factor Systems — WifOR · EPS (Steen / Stockholm) · UBA MC 4.0**
**Organization**: Transition Valuation Project under Greenings custodianship
**Version**: 2.0
**Last Updated**: 2026-03-06

This document provides solutions to common problems encountered when using any of the three value factor submodules. Sections 1–6 cover WifOR (`value-factors/`). Sections 7–8 cover EPS (`stockholm-value-factors/`) and UBA (`uba-value-factors/`) respectively.

---

## Table of Contents

**WifOR (`value-factors/`)**
1. [Installation Issues](#installation-issues)
2. [Data File Issues](#data-file-issues)
3. [Execution Errors](#execution-errors)
4. [Output Validation Issues](#output-validation-issues)
5. [Performance Issues](#performance-issues)
6. [Configuration Issues](#configuration-issues)

**EPS (`stockholm-value-factors/`)**
7. [EPS-Specific Issues](#eps-specific-issues)

**UBA (`uba-value-factors/`)**
8. [UBA-Specific Issues](#uba-specific-issues)

---

## Installation Issues

### Issue 1: License Not Accepted

**Symptom**:
```
License acceptance cancelled. Exiting...
```

**Cause**: Scripts require Apache 2.0 License acceptance before first run

**Solution**:
```bash
# Option 1: Run license_check.py directly
python license_check.py

# Option 2: Create acceptance file manually
echo "Y" > .license_accepted

# Option 3: Accept when prompted during first script run
python 007_241001_prepare_Waste_my.py
# Answer 'Y' when prompted
```

---

### Issue 2: Missing Dependencies

**Symptom**:
```
ModuleNotFoundError: No module named 'pandas'
```

**Cause**: Required Python packages not installed

**Solution**:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install pandas numpy openpyxl tables PyYAML
```

---

### Issue 3: Input Data Files Missing

**Symptom**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'input_data/...'
```

**Cause**: Input data files not downloaded

**Solution**:
```bash
# Download data files from Google Cloud Storage
python download_assets.py

# Verify files downloaded
ls -lh input_data/
# Should show 10 files (2 shared + 8 indicator-specific)
```

**Note**: Requires `gsutil` (Google Cloud SDK) installed and configured

---

## Data File Issues

### Issue 4: Country Code Mismatch

**Symptom**: Some countries missing in output or script crashes with country code error

**Cause**: Country codes differ between Model_definitions and indicator data

**Known Mappings**:
- SSD (South Sudan old) → SDS (South Sudan current)
- SDN (Sudan old) → SUD (Sudan current)

**Solution**:
Scripts handle these automatically. If you see new mismatches:

1. Check error message for country codes
2. Add mapping in affected script:
   ```python
   raw_data = raw_data.rename(columns={"OLD_CODE": "NEW_CODE"})
   ```
3. Report issue on GitHub for permanent fix

---

### Issue 5: Excel Sheet Not Found

**Symptom**:
```
ValueError: Worksheet named 'WifOR_form' not found
```

**Cause**: Excel file structure changed or wrong file version

**Solution**:
1. Open Excel file and verify sheet names
2. Check file date matches config.yaml
3. Re-download original file if corrupted:
   ```bash
   python download_assets.py --force
   ```

---

### Issue 6: HDF5 Key Error

**Symptom**:
```
KeyError: 'No object named "coefficients" in the file'
```

**Cause**: HDF5 file missing expected key

**Solution**:
1. Check available keys:
   ```python
   import pandas as pd
   with pd.HDFStore('file.h5') as store:
       print(store.keys())
   ```
2. Update script to use correct key
3. Re-download file if corrupted

---

## Execution Errors

### Issue 7: All Scripts Fail Immediately

**Symptom**: `run_all_value_factors.py` shows all scripts failed in <2 seconds

**Likely Causes**:
1. License not accepted (see Issue 1)
2. Missing input files (see Issue 3)
3. Configuration error (see Issue 14)

**Diagnostic Steps**:
```bash
# Run single script with output visible
python 007_241001_prepare_Waste_my.py

# Check for specific error message
# Then consult relevant issue in this guide
```

---

### Issue 8: KeyError on Column Name

**Symptom**:
```
KeyError: 'costs'
```

**Cause**: Expected column not in input file

**Solution**:
1. Check input file structure:
   ```python
   import pandas as pd
   df = pd.read_excel('input_data/220509_Waste figures merged_update.xlsx',
                      sheet_name='Waste_hazardous_incinerated')
   print(df.columns)
   ```
2. Verify column name matches exactly (case-sensitive, check for spaces)
3. If column renamed in new version, update script

---

### Issue 9: Memory Error

**Symptom**:
```
MemoryError: Unable to allocate array
```

**Cause**: Insufficient RAM for large coefficient matrices

**Solution**:
```bash
# Option 1: Run scripts sequentially instead of parallel
python run_all_value_factors.py --max-workers 1

# Option 2: Run scripts individually
python 007_241001_prepare_Waste_my.py
python 008_241001_prepare_AirPollution_my.py
# etc.

# Option 3: Increase available memory
# Close other applications or upgrade system RAM
```

---

### Issue 10: Timeout Error

**Symptom**: Script times out after 3600 seconds (1 hour)

**Cause**: Script taking longer than default timeout

**Solution**:
```bash
# Increase timeout
python run_all_value_factors.py --timeout 7200  # 2 hours

# Or run individual script (no timeout)
python 008_241001_prepare_AirPollution_my.py
```

---

## Output Validation Issues

### Issue 11: Positive Coefficients in Damage Indicators

**Symptom**: Waste, Air Pollution, etc. show positive values

**Cause**: Sign convention error in script

**Solution**:
1. Check `coefficient_sign` parameter in script
2. Should be `-1.0` for all except Training
3. Verify input data doesn't have negative values (which would become positive after sign flip)

**Validation**:
```python
import pandas as pd
df = pd.read_excel('output/2024-10-01_coefficients_Waste.xlsx',
                   sheet_name='Coefficients', index_col=[0,1], header=[0,1])
positive_count = (df > 0).sum().sum()
print(f"Positive coefficients: {positive_count} (should be 0)")
```

---

### Issue 12: Negative Training Coefficients

**Symptom**: Training shows negative values (should be positive benefit)

**Cause**: Sign error in Training script

**Solution**:
1. Check `coefficient_sign = 1.0` in `014_241016_prepare_Training_my.py`
2. Verify input data is positive
3. Training is the ONLY positive indicator

---

### Issue 13: Missing Countries in Output

**Symptom**: Output has fewer than 188 countries

**Cause**: Input data missing some countries

**Solution**:
1. Check input file country coverage:
   ```python
   df = pd.read_excel('input_data/220509_Waste figures merged_update.xlsx',
                      sheet_name='Waste_hazardous_incinerated')
   print(f"Countries in input: {len(df)}")
   ```
2. Add missing countries with regional average or zero value
3. Report data gap on GitHub

---

## Performance Issues

### Issue 14: Scripts Running Very Slowly

**Symptom**: Individual scripts take >10 minutes

**Likely Causes**:
1. Large dataset
2. Slow disk I/O
3. Inefficient computation

**Solutions**:
```bash
# Monitor during execution
top  # Check CPU/memory usage

# Check disk speed
iotop  # Requires sudo

# Optimize:
# - Use SSD instead of HDD
# - Close other applications
# - Run on machine with more RAM
```

---

### Issue 15: Parallel Execution Not Faster

**Symptom**: `run_all_value_factors.py` not faster than sequential

**Cause**: I/O bottleneck or limited CPU cores

**Solution**:
```bash
# Check CPU cores
nproc  # Linux/Mac
echo %NUMBER_OF_PROCESSORS%  # Windows

# Adjust workers to match cores
python run_all_value_factors.py --max-workers $(nproc)

# If still slow, scripts may be I/O bound (disk speed limiting)
# Consider SSD upgrade
```

---

## Configuration Issues

### Issue 16: Config File Not Found

**Symptom**:
```
FileNotFoundError: config.yaml not found
```

**Cause**: Script run from wrong directory

**Solution**:
```bash
# Ensure you're in project root
cd /path/to/value-factors

# Verify config.yaml exists
ls config.yaml

# Run scripts from project root
python 007_241001_prepare_Waste_my.py
```

---

### Issue 17: Wrong Input File Path in Config

**Symptom**: Script can't find input file despite it existing

**Cause**: config.yaml has incorrect path

**Solution**:
1. Check config.yaml:
   ```yaml
   waste:
     input_file: "input_data/220509_Waste figures merged_update.xlsx"
   ```
2. Verify path relative to project root
3. Use forward slashes (/) not backslashes (\)
4. No leading slash (relative path, not absolute)

---

### Issue 18: Base Year Mismatch

**Symptom**: Units show unexpected year (e.g., "2019USD" instead of "2020USD")

**Cause**: Different base years for different indicators

**Explanation**: This is expected behavior
- GHG uses 2019 base year (DICE model reference)
- All others use 2020 base year

**Solution**: No action needed if GHG vs others. If within indicator group:
1. Check config.yaml base_year setting
2. Verify consistent across indicator

---

## Debugging Tips

### Enable Verbose Logging

Add logging to scripts:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug("Your debug message here")
```

### Check Intermediate Results

Add print statements to inspect data:

```python
print(f"Raw data shape: {raw_data.shape}")
print(f"Raw data columns: {raw_data.columns.tolist()}")
print(f"First few rows:\n{raw_data.head()}")
```

### Use Python Debugger

```python
import pdb; pdb.set_trace()  # Pauses execution here
# Inspect variables, step through code
```

### Validate Input Files

```bash
# Check file integrity
python -c "import pandas as pd; pd.read_excel('input_data/file.xlsx')"

# Check HDF5 structure
h5dump -H input_data/file.h5
```

---

---

## 7. EPS-Specific Issues

### Issue E1: `data/` folder missing

**Symptom**:
```
FileNotFoundError: No such file or directory: 'data/...'
```

**Cause**: The `stockholm-value-factors/data/` folder was not cloned or copied.

**Solution**: Copy the `data/` folder from the source repository or from a local reference copy:
```bash
# If you have a local reference copy (e.g. steen-vf1):
cp -r /path/to/steen-vf1/eps_value_factors/data/ stockholm-value-factors/data/
```

---

### Issue E2: ELU values appear as zero or NaN

**Symptom**: EPS output coefficients are 0.0 or NaN for all substances.

**Cause**: Substance characterisation factors not parsed correctly from source data.

**Solution**:
1. Verify that `data/` contains the correct EPS 2015d.1 source files.
2. Check that the source file encoding is UTF-8 (not Latin-1); some EPS CSV files use semicolons as delimiters:
   ```python
   pd.read_csv("data/eps_factors.csv", sep=";", encoding="utf-8")
   ```

---

### Issue E3: All countries show identical values

**Symptom**: Every country has the same coefficient for a given substance and year.

**Explanation**: This is **expected behaviour**. EPS 2015d.1 publishes globally uniform characterisation factors — no country differentiation is applied within the EPS pipeline. Country-specific values are produced only after value transfer (see `VALUE_TRANSFER.md`).

---

### Issue E4: Noise unit mismatch vs UBA noise

**Symptom**: EPS noise unit is `ELU/W` (relative acoustic power); UBA noise is `EUR/person/year`.

**Explanation**: These are fundamentally different emission units. EPS noise requires conversion via the WHO exposure-response function (% highly annoyed per dB(A)) before comparison with UBA noise values. See `VALUE_TRANSFER.md` section 4.2.

---

### Issue E5: HICP deflator frozen at 2023 for years 2024+

**Symptom**: EPS coefficients are identical for all years 2023–2100.

**Explanation**: This is **expected behaviour**. The EU HICP deflator is only available through 2023. For years 2024 and beyond, the deflator is frozen at the 2023 value (factor 1.241 relative to 2015 base). This is documented in `stockholm-value-factors/VALIDATION_REPORT.md`.

---

## 8. UBA-Specific Issues

### Issue U1: `openpyxl` not installed

**Symptom**:
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Solution**:
```bash
pip install openpyxl
```

---

### Issue U2: Row count mismatch

**Symptom**: A table group produces fewer rows than expected.

**Expected counts** (from `VALIDATION_REPORT.md` in `uba-value-factors/`):

| Key | Expected |
|-----|----------|
| ghg | 54 |
| air_pollutants | 133 |
| electricity | 45 |
| heat | 45 |
| refrigerants | 16 |
| transport_vehkm | 142 |
| transport_pkm_tkm | 38 |
| noise | 42 |
| nitrogen_phosphorus | 11 |
| agriculture | 20 |

**Solution**: Row counts are determined by the hard-coded data structures in `pipeline.py`. A mismatch means the data was edited incorrectly. Restore the original data tuples and re-run.

---

### Issue U3: Reference value does not match PDF

**Symptom**: CO₂ 2025 / 0 % PRTP ≠ 990 EUR/t, or PM₂.₅ health ≠ 128,200 EUR/t.

**Cause**: A value was accidentally changed in `pipeline.py`.

**Solution**: Cross-check the data tuple against the UBA MC 4.0 PDF (Table 1 for GHG, Table 2 for air pollutants). All data in `pipeline.py` is manually transcribed. See `uba-value-factors/VALIDATION_REPORT.md` for the full set of known-good reference values.

---

### Issue U4: Excel file not written

**Symptom**: CSV files are created but `.xlsx` files are absent.

**Cause**: `openpyxl` not installed, or `_write_excel()` raised an exception that was silently swallowed.

**Solution**:
```bash
pip install openpyxl
# Then re-run:
python extract_uba_values.py
```
Check the execution log (`execution_log_*.txt`) for `[FAIL]` entries with error messages.

---

### Issue U5: `tables/NN_key.py` script not found

**Symptom**:
```
python: can't open file 'tables/01_ghg.py': No such file or directory
```

**Cause**: The `tables/` subdirectory was not cloned correctly (possibly a shallow clone).

**Solution**:
```bash
git -C uba-value-factors/ fetch --unshallow
# Or run from the orchestrator instead:
python uba-value-factors/extract_uba_values.py --only ghg
```

---

## Getting Help

| System | First step | GitHub Issues | Email |
|--------|-----------|--------------|-------|
| WifOR | README.md → METHODOLOGY.md | github.com/wifor-impactanalysis/WifOR-Value-Factors/issues | dimitrij.euler@greenings.org |
| EPS (Steen) | stockholm-value-factors/README.md | github.com/d1mitrij/Stockholm_ValueFactors/issues | dimitrij.euler@greenings.org |
| UBA MC 4.0 | uba-value-factors/README.md | github.com/d1mitrij/UBA_ValueFactors/issues | dimitrij.euler@greenings.org |

When filing an issue include: full error traceback, script name, Python version (`python --version`), package versions (`pip list`), and operating system.

---

## Common Error Messages Reference

| Error Message | System | Issue # | Quick Fix |
|---------------|--------|---------|-----------|
| `License acceptance cancelled` | WifOR | E1 in WifOR | Run `python license_check.py` |
| `ModuleNotFoundError` | All | 2 / U1 | `pip install -r requirements.txt` |
| `FileNotFoundError: input_data/` | WifOR | 3 | `python download_assets.py` |
| `FileNotFoundError: data/` | EPS | E1 | Copy `data/` from reference |
| `KeyError: 'costs'` | WifOR | 8 | Check input file column names |
| `MemoryError` | WifOR | 9 | Reduce `--max-workers` |
| `Worksheet not found` | WifOR | 5 | Verify Excel sheet names |
| `KeyError: 'No object'` | WifOR | 6 | Check HDF5 keys |
| Positive damage coefficients | WifOR | 11 | Check `coefficient_sign = -1.0` |
| Negative training coefficients | WifOR | 12 | Check `coefficient_sign = 1.0` |
| All EPS countries identical | EPS | E3 | Expected — see E3 explanation |
| UBA row count mismatch | UBA | U2 | Restore `pipeline.py` data tuples |
| UBA reference value wrong | UBA | U3 | Cross-check against PDF Table 1/2 |

---

**Document Version**: 2.0
**Last Updated**: 2026-03-06
**Maintained by**: Dr Dimitrij Euler, Greenings
**Contact**: dimitrij.euler@greenings.org
