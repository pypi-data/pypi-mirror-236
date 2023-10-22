import click
import csv

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_prefix', type=click.STRING)
@click.argument('chunk_size', type=click.INT)
def split_csv(input_file, output_prefix, chunk_size):
    """
    A tool to split a CSV file into smaller chunks.

    INPUT_FILE: Path to the input CSV file.
    OUTPUT_PREFIX: Prefix for the output files.
    CHUNK_SIZE: Number of rows per output file (default: 100).
    """
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Assuming the first row is the header
        rows = list(reader)  # Read all rows into a list

    total_rows = len(rows)

    if chunk_size > total_rows:
        click.echo(f"Error: Chunk size ({chunk_size}) is greater than the total number of rows ({total_rows}) in the input CSV.")
        return

    # Proceed with splitting the CSV as before
    for i, row in enumerate(rows):
        if i % chunk_size == 0:
            if i > 0:
                outfile.close()
            chunk_num = i // chunk_size + 1
            outfile = open(f'{output_prefix}_{chunk_num}.csv', 'w', newline='')
            writer = csv.writer(outfile)
            writer.writerow(header)
        writer.writerow(row)

if __name__ == '__main__':
    split_csv()





