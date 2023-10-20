import matplotlib.pyplot as plt


def visualize_expected_vs_observed_reads(sample_sub_dirs, demultiplex_barcode_counts_samples_dict, sample_indices_df_subset, sample_pooling_df):
    for sample_sub_dir in sample_sub_dirs:
        demultiplex_barcode_counts = demultiplex_barcode_counts_samples_dict[sample_sub_dir]
        i5_index_demultiplexed = sample_indices_df_subset.loc[sample_indices_df_subset["sub_library_name"] == sample_sub_dir, "i5_index"].iloc[0]
        sample_pooling_df_i5subset = sample_pooling_df[sample_pooling_df["i5_index"] == i5_index_demultiplexed]
        expected_reads = sample_pooling_df_i5subset["Recommended_Reads_for_gRNA_amplification_"].str.replace(',', '').astype(float) # NOTE 20230621: This line was added in the package since expected_reads was not assigned in the Jupyter notebook
        plt.scatter(expected_reads, demultiplex_barcode_counts[0], label=sample_sub_dir, alpha=0.7)
        plt.xlabel("Expected reads")
        plt.ylabel("Observed reads")
    
    plt.title("Expected vs. Observed Reads - All Sub-Libraries")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    x = [0, 7e6]
    y = [0, 7e6]
    plt.plot(x, y)
    plt.xlim(0, 7e6)
    plt.ylim(0, 7e6)
    plt.show()