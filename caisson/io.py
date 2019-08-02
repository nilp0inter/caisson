import os
import shutil

from caisson import log


def final_path(source, destination):
    return os.path.join(destination, os.path.basename(source))


def decompress_file(source, destination, decompressors):
    log.info("analyzing file %r", source)
    for decompressor in decompressors:
        if decompressor.can_decompress(source):
            log.debug("found decompressor %r for %r",
                      decompressor.name,
                      source)

            new_destination = final_path(source, destination) + ".content"
            log.debug("creating directory %r for decompression",
                      new_destination)
            os.makedirs(new_destination, exist_ok=True)

            log.info("decompressing file %r with %r",
                     source,
                     decompressor.name)
            try:
                decompressor.decompress(source, new_destination)
            except:
                log.exception("error while decompressing %r into %r",
                              source,
                              new_destination)
            break
    else:
        log.debug(("no valid decompressor found for file %r should be "
                   "a regular file"),
                  source)
        if source == final_path(source, destination):
            log.debug("file %r already is in destination directory",
                      source)
        else:
            log.info("copying file %r to %r", source, destination)
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
    log.debug("looking into directory %r for compressed files for removal",
              path)
    for entry in os.scandir(path):
        if entry.is_file():
            for decompressor in decompressors:
                if decompressor.can_decompress(entry.path):
                    log.info("removing compressed file %r", entry.path)
                    os.unlink(entry.path)
        elif entry.is_dir():
            remove_compressed_files(entry.path, decompressors)
        else:
            pass
