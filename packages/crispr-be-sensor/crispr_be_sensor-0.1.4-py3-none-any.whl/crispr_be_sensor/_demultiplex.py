import gzip
from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd
import glob
import os
import contextlib
import multiprocessing

from dataclasses import dataclass
from typing import Union, List, Tuple
from functools import partial
from collections import defaultdict

@dataclass
class ReadDemultiplexStrategy:
    read1_match_string: List
    read2_match_string: Union[List,None]
    output_dir: str 
    U6PE1_handle_long: str = "GGAAAGGACGAAACACCG"
    U6PE1_handle_short: str = "GGAAAGG"
    
# EXPORT IN __init__.py
##
# sample_indices_df_subset: DATAFRAME CONTAINING i5_INDEX DEMULTIPLEX SAMPLES - Must contain column "sub_library_name", "i5_index"
# sample_pooling_df_subset: DATAFREAME CONTAINING U6PE1_BARCODE DEMULTIPLE SAMMPLES - Must contain column "i5_index" and U6PE1_Barcode
##
def main_perform_demultiplex(read_demultiplex_strategy: ReadDemultiplexStrategy, data_root_dir:str, sample_sub_dirs: List[str], sample_indices_df_subset: pd.DataFrame, sample_pooling_df_subset: pd.DataFrame, read_cores: int = 1):
    
    # Start by creating the directory for the demultiplexed FASTQS
    if not os.path.exists(read_demultiplex_strategy.output_dir):
        os.makedirs(read_demultiplex_strategy.output_dir)


    #def process_sample_subdir(sample_sub_dir, read_demultiplex_strategy, sample_indices_df_subset, sample_pooling_df_subset):
    process_sample_subdir_p = partial(process_sample_subdir, data_root_dir=data_root_dir, read_demultiplex_strategy=read_demultiplex_strategy, sample_indices_df_subset=sample_indices_df_subset, sample_pooling_df_subset=sample_pooling_df_subset)

    if read_cores == 1:
        for sample_sub_dir in sample_sub_dirs:
            process_sample_subdir_p(sample_sub_dir)
    else:
        n_processes = min(len(sample_sub_dirs)+1, read_cores)
        with multiprocessing.Pool(processes=n_processes) as pool:
            _ = pool.map(process_sample_subdir_p, sample_sub_dirs)



# EXPORT IN __init__.py
def main_perform_demultiplex_qc(sample_sub_dirs: List[str], read_demultiplex_strategy: ReadDemultiplexStrategy, sample_indices_df_subset: pd.DataFrame, sample_pooling_df_subset: pd.DataFrame, read_cores: int = 1) -> dict:
    
    ###
    ### Get counts of unrecognized barcodes
    ###
    process_demultiplex_qc_p = partial(process_demultiplex_qc, read_demultiplex_strategy=read_demultiplex_strategy, sample_indices_df_subset=sample_indices_df_subset, sample_pooling_df_subset=sample_pooling_df_subset)
    unique_barcode_counts_list = None
    if read_cores == 1:
        unique_barcode_counts_list = [process_demultiplex_qc_p(sample_sub_dir) for sample_sub_dir in sample_sub_dirs]
    else:
        n_processes = min(len(sample_sub_dirs)+1, read_cores)
        with multiprocessing.Pool(processes=n_processes) as pool:
            unique_barcode_counts_list = pool.map(process_demultiplex_qc_p, sample_sub_dirs)

    unique_barcode_counts_samples_dict = dict(unique_barcode_counts_list)



    ###
    ### Get read counts for each demultiplexed files
    ###
    process_demultiplex_files_p = partial(process_demultiplex_files, read_demultiplex_strategy=read_demultiplex_strategy, sample_indices_df_subset=sample_indices_df_subset, sample_pooling_df_subset=sample_pooling_df_subset)
    demultiplex_barcode_counts_list = None
    if read_cores == 1:
        demultiplex_barcode_counts_list = [process_demultiplex_files_p(sample_sub_dir) for sample_sub_dir in sample_sub_dirs]
    else:
        n_processes = min(len(sample_sub_dirs)+1, read_cores)
        with multiprocessing.Pool(processes=n_processes) as pool:
            demultiplex_barcode_counts_list = pool.map(process_demultiplex_files, sample_sub_dirs)

    demultiplex_barcode_counts_samples_dict = dict(demultiplex_barcode_counts_list)


    return {"unique_barcode_counts_samples_dict": unique_barcode_counts_samples_dict, 
            "demultiplex_barcode_counts_samples_dict": demultiplex_barcode_counts_samples_dict}




####
#### BELOW - FOR main_perform_demultiplex
####
def get_matching_files(data_root_dir: str, sample_sub_dir: str, match_str: str):
    matching_files = glob.glob(f"{data_root_dir}/{sample_sub_dir}/*{match_str}*")
    assert len(matching_files) == 1, "Expected exactly one file, but found {} files.".format(len(matching_files))
    return matching_files[0]

def parse_fastq(fastq_file):
    for record in SeqIO.parse(fastq_file, "fastq"):
        yield record
        
 # Get index of U6PE1 handle
def process_record(r1_record, r2_record, sample_pooling_df_subset_i5subset_barcodes, r1_demult_handlers, r2_demult_handlers, r1_demult_unknown_handler, r2_demult_unknown_handler):
    U6PE1_handle_index = r1_record.seq.find(read_demultiplex_strategy.U6PE1_handle_long)
    if U6PE1_handle_index == -1:
        U6PE1_handle_index = r1_record.seq.find(read_demultiplex_strategy.U6PE1_handle_short)

    # Get the Barcode
    found_barcode = False
    if U6PE1_handle_index != -1:
        U6PE1_barcode = str(r1_record.seq[:U6PE1_handle_index]).upper()
        
        for subdir_barcode_index, subdir_barcode in enumerate(sample_pooling_df_subset_i5subset_barcodes):
            if subdir_barcode.upper() == U6PE1_barcode:
                r1_demult_handler_barcode = r1_demult_handlers[subdir_barcode_index]
                r2_demult_handler_barcode = r2_demult_handlers[subdir_barcode_index]

                SeqIO.write(r1_record, r1_demult_handler_barcode, "fastq")
                SeqIO.write(r2_record, r2_demult_handler_barcode, "fastq")
                found_barcode = True
                break # Added read to correct barcode FASTQ, break
    if found_barcode is False:  
        SeqIO.write(r1_record, r1_demult_unknown_handler, "fastq")
        SeqIO.write(r2_record, r2_demult_unknown_handler, "fastq")

# TODO 20230328: When creating a package for this, I am able to determine whether read2_fn_list is available based on the provided inputs, yet I still iterate through the R2 reads later on, which would throw an error if no R2 is provided. This needs to be fixed when moving to a package

###
# sample_indices_df_subset: DATAFRAME CONTAINING i5_INDEX DEMULTIPLEX SAMPLES - Must contain column "sub_library_name", "i5_index"
# sample_pooling_df_subset: DATAFREAME CONTAINING U6PE1_BARCODE DEMULTIPLE SAMMPLES - Must contain column "i5_index" and U6PE1_Barcode
####
def process_sample_subdir(sample_sub_dir, data_root_dir, read_demultiplex_strategy, sample_indices_df_subset, sample_pooling_df_subset):
    print(f"Processing sub directory {sample_sub_dir}")
    

    i5_index_demultiplexed = sample_indices_df_subset.loc[sample_indices_df_subset["sub_library_name"] == sample_sub_dir, "i5_index"].iloc[0]
    sample_pooling_df_subset_i5subset = sample_pooling_df_subset[sample_pooling_df_subset["i5_index"] == i5_index_demultiplexed]
    sample_pooling_df_subset_i5subset_barcodes = sample_pooling_df_subset_i5subset["U6PE1_Barcode"]

    # Create output sub directory
    output_sub_dir = f"{read_demultiplex_strategy.output_dir}/{sample_sub_dir}"
    print(f"Creating output sub directory {output_sub_dir}")
    if not os.path.exists(output_sub_dir):
        os.makedirs(output_sub_dir)
    
    
    # Get the input read1 and read2 files (for all lanes)
    read1_fn_list = [get_matching_files(data_root_dir, sample_sub_dir, read1_match_str) for read1_match_str in read_demultiplex_strategy.read1_match_string]
    read2_fn_list = None
    if read_demultiplex_strategy.read2_match_string is not None:
        read2_fn_list = [get_matching_files(data_root_dir, sample_sub_dir, read2_match_str) for read2_match_str in read_demultiplex_strategy.read2_match_string]

    # Setup outputs of demultiplex fastqs
    # Prepare the output handlers
    
    r1_demult_fns = [f"{output_sub_dir}/{sample_sub_dir}_#{sample_for_barcode}_R1.fastq" for sample_for_barcode in sample_pooling_df_subset_i5subset_barcodes]
    r2_demult_fns = [f"{output_sub_dir}/{sample_sub_dir}_#{sample_for_barcode}_R2.fastq" for sample_for_barcode in sample_pooling_df_subset_i5subset_barcodes]

    r1_demult_unknown_fn = f"{output_sub_dir}/{sample_sub_dir}_#unknown_R1.fastq"
    r2_demult_unknown_fn = f"{output_sub_dir}/{sample_sub_dir}_#unknown_R2.fastq"

    # Remove old files
    with contextlib.suppress(FileNotFoundError):
        os.remove(r1_demult_unknown_fn)
        os.remove(r2_demult_unknown_fn)

        for fn in r1_demult_fns:
            os.remove(fn)
        for fn in r2_demult_fns:
            os.remove(fn)

    # Create and open files
    r1_demult_handlers = [open(r1_demult_fn, "a") for r1_demult_fn in r1_demult_fns]
    r2_demult_handlers = [open(r2_demult_fn, "a") for r2_demult_fn in r2_demult_fns]

    r1_demult_unknown_handler = open(r1_demult_unknown_fn, "a")
    r2_demult_unknown_handler = open(r2_demult_unknown_fn, "a")
        
    # Iterate through each lane
    for lane_index, read1_fn in enumerate(read1_fn_list):
        print(f"Processing lane index {lane_index} for {sample_sub_dir}")
        
        # Open the input R1 and R2 file for the lane
        with gzip.open(read1_fn_list[lane_index], "rt") as read1_handle, gzip.open(read2_fn_list[lane_index], "rt") as read2_handle:
           # Define function to use with map
            def process_records(args):
                r1_record, r2_record = args
                return process_record(r1_record, r2_record, sample_pooling_df_subset_i5subset_barcodes, r1_demult_handlers, r2_demult_handlers, r1_demult_unknown_handler, r2_demult_unknown_handler)

            ## Iterate through all reads to perform the demultiplex
            #with multiprocessing.Pool(processes=read_cores) as pool:
            #    _ = pool.map(process_records, zip(SeqIO.parse(read1_handle, "fastq"), SeqIO.parse(read2_handle, "fastq")))
            # LEFTOFF - Fix multiprocessing issue, not actually writing into  
            
            for record in zip(SeqIO.parse(read1_handle, "fastq"), SeqIO.parse(read2_handle, "fastq")):
                process_records(record)
                              
    for handler in r1_demult_handlers:
        handler.close()
    for handler in r2_demult_handlers:
        handler.close()
    r1_demult_unknown_handler.close()
    r2_demult_unknown_handler.close()
    
    print(f"Finished subdir: {sample_sub_dir}")
####
#### ABOVE - FOR main_perform_demultiplex
####    



####
#### BELOW - FOR main_process_demultiplex_qc
####
def process_demultiplex_qc(sample_sub_dir, read_demultiplex_strategy, sample_indices_df_subset, sample_pooling_df_subset) -> Tuple[str, defaultdict]:
    print(f"Started demultiplex QC for {sample_sub_dir}")
    
    # PREPARE BARCODES
    i5_index_demultiplexed = sample_indices_df_subset.loc[sample_indices_df_subset["sub_library_name"] == sample_sub_dir, "i5_index"].iloc[0]
    sample_pooling_df_subset_i5subset = sample_pooling_df_subset[sample_pooling_df_subset["i5_index"] == i5_index_demultiplexed]
    sample_pooling_df_subset_i5subset_barcodes = sample_pooling_df_subset_i5subset["U6PE1_Barcode"]
    
    # GET THE DIR OF THE DEMULTIPLEXED FASTQS
    output_sub_dir = f"{read_demultiplex_strategy.output_dir}/{sample_sub_dir}"
    
    # Get filenames of outputs - 20230621 not needed unless required for another QC metric
    #r1_demult_fns = [f"{output_sub_dir}/{sample_sub_dir}_#{sample_for_barcode}_R1.fastq" for sample_for_barcode in sample_pooling_df_subset_i5subset_barcodes]
    #r2_demult_fns = [f"{output_sub_dir}/{sample_sub_dir}_#{sample_for_barcode}_R2.fastq" for sample_for_barcode in sample_pooling_df_subset_i5subset_barcodes]

    # GET THE READ_1 WHICH CONTAINS THE U6PE1_BARCODE
    r1_demult_unknown_fn = f"{output_sub_dir}/{sample_sub_dir}_#unknown_R1.fastq"
    #r2_demult_unknown_fn = f"{output_sub_dir}/{sample_sub_dir}_#unknown_R2.fastq"
    
    # Create file handlers - 20230621 not needed unless required for another QC metric
    #r1_demult_handlers = [open(r1_demult_fn, "rt") for r1_demult_fn in r1_demult_fns]
    #r2_demult_handlers = [open(r2_demult_fn, "rt") for r2_demult_fn in r2_demult_fns]

    # OPEN FILE HANDLER OFF READ 1 UNKNOWN FASTQ
    r1_demult_unknown_handler = open(r1_demult_unknown_fn, "rt")
    #r2_demult_unknown_handler = open(r2_demult_unknown_fn, "rt")
    
    # GENERATE INDICES FOR QUICK READ ACCESS
    #r1_demult_indices = [SeqIO.index(r1_demult_fn, "fastq") for r1_demult_fn in r1_demult_fns]
    r1_demult_unknown_index = SeqIO.index(r1_demult_unknown_fn, "fastq")
    
    # CALCULATE NUMBER OFF UNMAPPED READS
    #r1_demult_indices_len = [len(index) for index in r1_demult_indices]
    r1_demult_unknown_index_len = len(r1_demult_unknown_index)
    
    # COUNT EACH UNIQUE BARCODE THAT WAS UNMAPPED
    unique_barcode_counts = defaultdict(int)
    for r1_record in SeqIO.parse(r1_demult_unknown_handler, "fastq"):
        # Get index of U6PE1 handle
        U6PE1_handle_index = r1_record.seq.find(read_demultiplex_strategy.U6PE1_handle_long)
        if U6PE1_handle_index == -1:
            U6PE1_handle_index = r1_record.seq.find(read_demultiplex_strategy.U6PE1_handle_short)
            
        # Get the Barcode
        if U6PE1_handle_index != -1:
            U6PE1_barcode = str(r1_record.seq[:U6PE1_handle_index]).upper()
            unique_barcode_counts[U6PE1_barcode] += 1
        else:
            unique_barcode_counts["NO_HANDLE"] += 1
    
    
    # CLOSE THE HANDLERS
    #for handler in r1_demult_handlers:
    #    handler.close()
    #for handler in r2_demult_handlers:
    #    handler.close()
    r1_demult_unknown_handler.close()
    #r2_demult_unknown_handler.close()

    print(f"Finished {sample_sub_dir}")
    return (sample_sub_dir, unique_barcode_counts)



def process_demultiplex_files(sample_sub_dir, read_demultiplex_strategy, sample_indices_df_subset, sample_pooling_df_subset) -> Tuple[str, dict]:
    print(f"Started {sample_sub_dir}")
    
    # Prepare barcodes
    i5_index_demultiplexed = sample_indices_df_subset.loc[sample_indices_df_subset["sub_library_name"] == sample_sub_dir, "i5_index"].iloc[0]
    sample_pooling_df_subset_i5subset = sample_pooling_df_subset[sample_pooling_df_subset["i5_index"] == i5_index_demultiplexed]
    sample_pooling_df_subset_i5subset_barcodes = sample_pooling_df_subset_i5subset["U6PE1_Barcode"]
    
    output_sub_dir = f"{read_demultiplex_strategy.output_dir}/{sample_sub_dir}"
    
    # Get filenames of outputs
    r1_demult_fns = [f"{output_sub_dir}/{sample_sub_dir}_#{sample_for_barcode}_R1.fastq" for sample_for_barcode in sample_pooling_df_subset_i5subset_barcodes]
    r2_demult_fns = [f"{output_sub_dir}/{sample_sub_dir}_#{sample_for_barcode}_R2.fastq" for sample_for_barcode in sample_pooling_df_subset_i5subset_barcodes]

    r1_demult_unknown_fn = f"{output_sub_dir}/{sample_sub_dir}_#unknown_R1.fastq"
    r2_demult_unknown_fn = f"{output_sub_dir}/{sample_sub_dir}_#unknown_R2.fastq"
    
    # Create file handlers
    r1_demult_handlers = [open(r1_demult_fn, "rt") for r1_demult_fn in r1_demult_fns]
    r2_demult_handlers = [open(r2_demult_fn, "rt") for r2_demult_fn in r2_demult_fns]

    r1_demult_unknown_handler = open(r1_demult_unknown_fn, "rt")
    r2_demult_unknown_handler = open(r2_demult_unknown_fn, "rt")
    
    # Generate indices
    r1_demult_indices = [SeqIO.index(r1_demult_fn, "fastq") for r1_demult_fn in r1_demult_fns]
    r1_demult_unknown_index = SeqIO.index(r1_demult_unknown_fn, "fastq")
    
    # Calculate number of reads per output
    r1_demult_indices_len = [len(index) for index in r1_demult_indices]
    r1_demult_unknown_index_len = len(r1_demult_unknown_index)
    
    for handler in r1_demult_handlers:
        handler.close()
    for handler in r2_demult_handlers:
        handler.close()
    r1_demult_unknown_handler.close()
    r2_demult_unknown_handler.close()

    print(f"Finished {sample_sub_dir}")
    return (sample_sub_dir, 
            {"r1_demult_indices_len": r1_demult_indices_len, 
             "r1_demult_unknown_index_len": r1_demult_unknown_index_len}
             )
  
####
#### ABOVE - FOR main_process_demultiplex_qc
####