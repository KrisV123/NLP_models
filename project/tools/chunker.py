from conllu import parse_incr, TokenList
from pathlib import Path

def save_file(group: list[TokenList], file_count: int, output_dir: Path) -> None:
    with open(output_dir / f'file_{file_count}.conllu', 'w', encoding='utf-8') as f:
        f.write(''.join([sent.serialize() for sent in group]))


def chunk_files(file_path: Path, output_dir: Path, chunk_size: int) -> None:
    """
    separate big file into smaller chunks.
    Chunks size is ammount of sentences in one chunk
    """

    with open(file_path, 'r', encoding='utf-8') as conllu:
        group = list()
        sent_count = 0
        file_count = 1
        for sent in parse_incr(conllu):
            group.append(sent)
            sent_count += 1

            if sent_count == chunk_size:
                save_file(group, file_count, output_dir)
                group = list()
                sent_count = 0
                file_count += 1


def merge_files(input_dir: Path, output_file: Path) -> None:
    """
    merge smaller chunks into one file
    """

    for file_path in input_dir.iterdir():
        print(f'converting {str(file_path)}')
        with open(file_path, 'r', encoding='utf-8') as conllu:
            group = [sent for sent in parse_incr(conllu)]

        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(''.join([sent.serialize() for sent in group]))
