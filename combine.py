import os
import PyPDF2

def prompt_user_for_order(pdf_files):
    print('Found the following PDFs:')
    for i, name in enumerate(pdf_files, start=1):
        print(f'  {i}. {name}')
    print('\nEnter the order from first to last as numbers separated by spaces or commas.')
    print(f'Example: 3 1 2 (must include each number 1..{len(pdf_files)} exactly once).')
    print("Press Enter to keep alphabetical order. Type 'q' to quit.\n")

    n = len(pdf_files)
    while True:
        raw = input('Order: ').strip()
        if raw == '':
            return pdf_files[:]
        low = raw.lower()
        if low in ('q', 'quit', 'exit'):
            raise SystemExit(0)
        tokens = [t for t in raw.replace(',', ' ').split() if t]
        if not tokens:
            print('Please enter some numbers, or press Enter to keep alphabetical.')
            continue
        if any(not t.isdigit() for t in tokens):
            print('Invalid input: only numbers allowed.')
            continue
        nums = [int(t) for t in tokens]
        out_of_range = [x for x in nums if x < 1 or x > n]
        if out_of_range:
            print(f'Out of range numbers: {sorted(set(out_of_range))}. Valid range is 1..{n}.')
            continue
        if len(nums) != n or len(set(nums)) != n:
            missing = [i for i in range(1, n + 1) if i not in nums]
            dups = sorted({x for x in nums if nums.count(x) > 1})
            if missing:
                print(f'Missing: {missing}')
            if dups:
                print(f'Duplicates: {dups}')
            print('Please include each number exactly once.')
            continue
        ordered = [pdf_files[i - 1] for i in nums]
        print('\nChosen order:')
        for i, name in enumerate(ordered, start=1):
            print(f'  {i}. {name}')
        confirm = input('Proceed with this order? [Y/n]: ').strip().lower()
        if confirm in ('', 'y', 'yes'):
            return ordered
        if confirm in ('n', 'no'):
            print("Okay, let's try again.")
            continue
        if confirm in ('q', 'quit', 'exit'):
            raise SystemExit(0)
        print('Please answer Y or N (or Q to quit).')

def combine_pdfs_in_folder(folder_path, output_filename):
    # List all PDF files in the folder, sorted alphabetically
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    pdf_files.sort()

    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'. Nothing to combine.")
        return

    try:
        ordered_files = prompt_user_for_order(pdf_files)
    except SystemExit:
        print('Cancelled. No file written.')
        return

    merger = PyPDF2.PdfMerger()
    for pdf in ordered_files:
        full_path = os.path.join(folder_path, pdf)
        merger.append(full_path)

    merger.write(output_filename)
    merger.close()
    print(f"Combined PDF saved as {output_filename}")

if __name__ == "__main__":
    folder = 'pdfs'
    output_pdf = 'combined.pdf'
    combine_pdfs_in_folder(folder, output_pdf)
