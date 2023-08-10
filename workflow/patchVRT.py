import secondaryFeatures
import sys

if len(sys.argv) < 3:
    print("not enough args")

secondaryFeatures.patchVRTPixelFunction(sys.argv[1], sys.argv[2])