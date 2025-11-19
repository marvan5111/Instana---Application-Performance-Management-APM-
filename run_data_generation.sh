 #!/bin/bash
 
 # This script automates the generation of all synthetic monitoring data.
 # It should be run from the root of the project directory.
 
 echo "Starting scheduled data generation run at $(date)..."
 
 # Run the main Python script that orchestrates all data generators
 python3 scripts/generate_instana_all.py
 
 echo "Data generation run completed at $(date)."