# Step041 outer audit — 自审
The P1 worker ratio uses matching complete captured event IDs, not a sum with
missing CPU shards. It still describes full worker lifetime, not exact check
CPU. Instrumented time is kept separate from ordinary timing. No foreign path,
runtime source, memory bound, lock protocol or acceptance criterion changed.
This is evidence collection within the existing admitted finite matrix.
