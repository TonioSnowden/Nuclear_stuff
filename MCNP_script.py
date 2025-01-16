import pandas as pd

data_path = "cmsr_dataset_material_movement.h5"
df_base = pd.read_hdf(data_path)

def get_high_sf_isotopes():
    """Returns a dictionary of isotopes with spontaneous fission neutron production > U-235"""
    # U-235 baseline: 3.0x10^-4 neutrons/(g·s)
    sf_data = {
        'U238' : 0.0136,
        'Pu236': 3.6e4,
        'Pu238': 2.7e3,
        'Pu239': 2.2e-2,
        'Pu240': 9.2e2,
        'Pu241': 0.05,
        'Pu242': 1.8e3,
        'Pu244': 1.9e3,
        'Am241': 1.18,
        'Cm242': 2.3e7,
        'Cm244': 1.1e7,
        'Cm246': 8.5e6,
        'Cm248': 4.1e12,
        'Cm250': 1.6e10,
        'Bk249': 1.1e5,
        'Cf246': 7.5e10,
        'Cf248': 5.1e9,
        'Cf250': 1.1e10,
        'Cf252': 2.3e12,
        'Cf254': 1.2e15,
        'Es253': 3.0e8,
        'Fm254': 3.0e14
    }
    return sf_data

def get_zaid(isotope):
    """Convert isotope name to ZAID number"""
    element = ''.join(filter(str.isalpha, isotope))
    mass_num = ''.join(filter(str.isdigit, isotope))
    
    z_numbers = {
        'U': 92, 'Pu': 94, 'Am': 95, 'Cm': 96, 
        'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100
    }
    
    if element in z_numbers:
        mass_num_int = int(mass_num)
        return f"{z_numbers[str(element)]}{mass_num_int:03d}"
    return None

def create_mcnp_input(row, high_sf_isotopes):
    """Creates MCNP input string for a given composition row"""
    mcnp_lines = []
    
    # Get fuel composition columns
    fuel_cols = [col for col in row.index if col.startswith('fuel_')]
    
    # First, find the maximum density to normalize others
    max_density = 0
    for col in fuel_cols:
        if row[col] > max_density:
            max_density = row[col]
    
    # Process each isotope
    for col in fuel_cols:
        if row[col] > 0:  # only include non-zero values
            isotope = col.split('_')[1]
            
            # Get ZAID number
            zaid = get_zaid(isotope)
            if zaid:
                # Normalize density relative to maximum
                relative_density = row[col] / max_density if max_density > 0 else 0
                mcnp_line = f"{zaid} {relative_density:.6f}"
                
                if isotope in high_sf_isotopes:
                    mcnp_lines.append(mcnp_line)
    
    # Join all lines with spaces
    return ' '.join(mcnp_lines) if mcnp_lines else ''

def process_dataframe(df):
    """Process dataframe and generate MCNP inputs for each row"""
    high_sf_isotopes = get_high_sf_isotopes()
    mcnp_inputs = []
    
    for idx, row in df.iterrows():
        mcnp_input = create_mcnp_input(row, high_sf_isotopes)
        if mcnp_input:  # Only append non-empty inputs
            mcnp_inputs.append(mcnp_input)
    
    return mcnp_inputs