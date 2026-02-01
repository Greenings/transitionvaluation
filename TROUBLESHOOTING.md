# Troubleshooting Guide

**WifOR Value Factors - Common Issues and Solutions**
**Organization**: Transition Valuation Project under Greenings custodianship
**Version**: 1.0
**Last Updated**: 2026-01-02

This document provides solutions to common problems encountered when using the WifOR Value Factors scripts.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Data File Issues](#data-file-issues)
3. [Execution Errors](#execution-errors)
4. [Output Validation Issues](#output-validation-issues)
5. [Performance Issues](#performance-issues)
6. [Configuration Issues](#configuration-issues)

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

## Getting Help

If issues persist:

1. **Check Existing Documentation**:
   - README.md
   - METHODOLOGY.md
   - DATA_UPDATES.md

2. **Search GitHub Issues**:
   - https://github.com/wifor-impactanalysis/WifOR-Value-Factors/issues

3. **Create New Issue**:
   Include:
   - Error message (full traceback)
   - Script being run
   - Python version: `python --version`
   - Package versions: `pip list`
   - Operating system

4. **Email Support**:
   - dimitrij.euler@greenings.org

---

## Common Error Messages Reference

| Error Message | Issue # | Quick Fix |
|---------------|---------|-----------|
| `License acceptance cancelled` | 1 | Run `python license_check.py` |
| `ModuleNotFoundError` | 2 | Run `pip install -r requirements.txt` |
| `FileNotFoundError: input_data/` | 3 | Run `python download_assets.py` |
| `KeyError: 'costs'` | 8 | Check input file column names |
| `MemoryError` | 9 | Reduce `--max-workers` |
| `Worksheet not found` | 5 | Verify Excel sheet names |
| `KeyError: 'No object'` | 6 | Check HDF5 keys |
| Positive damage coefficients | 11 | Check `coefficient_sign = -1.0` |
| Negative training coefficients | 12 | Check `coefficient_sign = 1.0` |

---

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
