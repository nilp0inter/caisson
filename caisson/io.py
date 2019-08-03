import os
import shutil

from caisson import log


def final_path(source, destination):
    return os.path.join(destination, os.path.basename(source))


def decompress_file(source, destination, decompressors, remove_source=False):
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
            else:
                if remove_source:
                    os.unlink(source)
            return True

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

    return False


def decompress(sources, destination, decompressors, subdir=True,
               remove_source=False):
    any_decompression = False
    for source in sources:
        if os.path.isdir(source):
            if subdir:
                new_destination = final_path(source, destination)
                os.makedirs(new_destination, exist_ok=True)
            else:
                new_destination = destination
            for entry in os.scandir(source):
                if entry.is_file():
                    any_decompression |= decompress_file(entry.path,
                                                         new_destination,
                                                         decompressors,
                                                         remove_source=remove_source)
                else:
                    any_decompression |= decompress([entry.path],
                                                    new_destination,
                                                    decompressors,
                                                    subdir=True,
                                                    remove_source=remove_source)
        else:
            any_decompression |= decompress_file(source,
                                                 destination,
                                                 decompressors,
                                                 remove_source=remove_source)
    return any_decompression
