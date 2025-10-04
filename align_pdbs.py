"""
Align all PDB files sequentially (each frame to the previous frame).
"""
from Bio.PDB import PDBParser, Superimposer, PDBIO
import os

# Configuration
pdb_dir = "pdb_files"
output_dir = "pdb_files_aligned"
start_frame = 0
end_frame = 191

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Initialize parser and superimposer
parser = PDBParser(QUIET=True)
super_imposer = Superimposer()
io = PDBIO()

print("Sequential alignment: each frame aligned to the previous frame\n")

# Track the previous frame's model for sequential alignment
prev_model = None

# Align all structures
for frame_num in range(start_frame, end_frame + 1):
    pdb_file = f"{pdb_dir}/fold_block_{frame_num:02d}.pdb"
    output_file = f"{output_dir}/fold_block_{frame_num:02d}.pdb"

    # Load structure
    structure = parser.get_structure(f"frame_{frame_num}", pdb_file)
    model = structure[0]

    if frame_num == start_frame:
        # First frame - just copy as-is
        io.set_structure(structure)
        io.save(output_file)
        print(f"Frame {frame_num}: First frame (copied)")
        prev_model = model
    else:
        # Align to previous frame using CA atoms
        ref_ca = [atom for atom in prev_model.get_atoms() if atom.get_name() == "CA"]
        mobile_ca = [atom for atom in model.get_atoms() if atom.get_name() == "CA"]

        # Check if we have matching CA atoms
        if len(ref_ca) != len(mobile_ca):
            print(f"Warning: Frame {frame_num} has {len(mobile_ca)} CA atoms vs previous {len(ref_ca)}")
            # Use minimum length for alignment
            min_len = min(len(ref_ca), len(mobile_ca))
            ref_ca = ref_ca[:min_len]
            mobile_ca = mobile_ca[:min_len]

        # Perform superposition
        super_imposer.set_atoms(ref_ca, mobile_ca)
        super_imposer.apply(model.get_atoms())

        # Save aligned structure
        io.set_structure(structure)
        io.save(output_file)
        print(f"Frame {frame_num}: Aligned to frame {frame_num-1} (RMSD: {super_imposer.rms:.3f} Å)")

        # Update previous model for next iteration
        prev_model = model

print(f"\nSequential alignment complete! Aligned PDB files saved to: {output_dir}/")
print(f"Each frame is now aligned to its previous frame for smooth transitions.")
