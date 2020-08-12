# python3

import os
import argparse
from PIL import Image


# checks to see if directory
def confirm_directory(directory,):
    if os.path.isdir(directory) is False:
        print(f':::\tINFO: {directory} does not exist. Creating directory.')
        try:
            os.mkdir(directory)
        except Exception as e:
            print(f':::\tERROR: {directory} could not be created due to error {e}. Exiting.')
            exit()
        print(f':::\tINFO: Created directory: {directory}')


def perform_crop(img, box, file):
    try:
        imgCrop = img.crop(box)
    except Exception as e:
        img.close()
        print(f':::\tERROR: Failed to crop {file}.')
        raise e

    return imgCrop


def save_crop(imgCrop, outFile, img):
    try:
        imgCrop.save(outFile)
    except Exception as e:
        print(f':::\tERROR: Failed to save {outFile} with error {e}. Exiting.')
        img.close()
        exit()


# only handles png right now
# TODO figure out a way to split this
def create_crops(sourcepath, splits, outpath, buffer):
    path, file = os.path.split(sourcepath)
    fileName, fileExt = os.path.splitext(file)

    if fileExt != '.png':
        print(':::\tWARNING: Script can only handle png files')
        return

    print(f':::\tINFO: Opening file {sourcepath}')
    img = Image.open(sourcepath)
    width, height = img.size

    left = 0
    right = width

    for i in range(splits):
        top = (height*i)/splits
        bottom = height*(i+1)/splits

        # handle buffer pixels for images
        # add buffer to the top if the image isn't the first
        if top != 0:
            top -= buffer
        # add buffer to the bottom if image isn't the last
        if bottom + buffer <= height:
            bottom += buffer
        box = (left, top, right, bottom)

        print(f':::\tINFO: Attemping crop {i+1} of {sourcepath}')
        imgCrop = perform_crop(img, box, file)
        print(f':::\tINFO: Succeeded in crop {i+1} of {sourcepath}')

        outFile = os.path.join(outpath, f'{fileName}_{i+1}{fileExt}')
        print(f':::\tINFO: Attemping to save crop {outFile}')
        save_crop(imgCrop, outFile, img)
        print(f':::\tINFO: Succeeded in saving {outFile}')


def png_split(sourcepath, splits, outpath, buffer=0):
    # get absolute paths for source and output
    sourcepath = os.path.abspath(sourcepath)
    outpath = os.path.abspath(outpath)
    # confirm that the ourput is a directory, if it doesn't exist, create it
    confirm_directory(outpath)

    if os.path.isdir(sourcepath):
        directoryContents = os.listdir(sourcepath)
        for item in directoryContents:
            item = os.path.join(sourcepath, item)
            if os.path.isfile(item):
                file = os.path.abspath(item)
                create_crops(file, splits, outpath, buffer)
            else:
                print(f':::\tWARNING: {item} is not a file. Skipping.')
    elif os.path.isfile(sourcepath):
        create_crops(sourcepath, splits, outpath, buffer)
    else:
        print(f':::\tERROR: {sourcepath} is not a directory or file.')
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a png horizontally.')
    parser.add_argument('-s', '--source', type=str, dest='source', required=True, help='sourcepath to file that will be split.')
    parser.add_argument('-S, --splits', type=int, dest='splits', required=True, help='Number of desired splits for file.')
    parser.add_argument('-t', '--target', type=str, dest='target', default=os.path.join(os.getcwd(), 'outputs'), help='Target file path for output.')
    parser.add_argument('-b', '--buffer', type=int, dest='buffer', default=0, help='Buffer to add space to the beginning and end of screenshots. Greater buffer means greater overlap.')
    args = parser.parse_args()

    png_split(args.source, args.splits, args.target, buffer=args.buffer)
