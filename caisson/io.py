import os
import shutil


def final_path(source, destination):
    return os.path.join(destination, os.path.basename(source))


def decompress_file(source, destination, decompressors):
    print(source, destination)
    for decompressor in decompressors:
        if decompressor.can_decompress(source):
            new_destination = final_path(source, destination) + ".content"
            os.makedirs(new_destination, exist_ok=True)
            try:
                decompressor.decompress(source, new_destination)
            except Exception as e:
                print(e)
            # os.unlink(source)
            break
    else:
        if source == final_path(source, destination):
            pass
        else:
            try:
                shutil.copy(source, destination)
            except PermissionError:
                pass



def decompress(sources, destination, decompressors, subdir=True):
    for source in sources:
        if os.path.isdir(source):
            if subdir:
                new_destination = final_path(source, destination)
                os.makedirs(new_destination, exist_ok=True)
            else:
                new_destination = destination
            for entry in os.scandir(source):
                if entry.is_file():
                    decompress_file(entry.path, new_destination, decompressors)
                else:
                    decompress([entry.path], new_destination, decompressors)
        else:
            decompress_file(source, destination, decompressors)


def remove_compressed_files(path, decompressors):
    for entry in os.scandir(path):
        if entry.is_file():
            for decompressor in decompressors:
                if decompressor.can_decompress(entry.path):
                    print("Removing", entry.path)
                    os.unlink(entry.path)
        elif entry.is_dir():
            remove_compressed_files(entry.path, decompressors)
        else:
            pass
