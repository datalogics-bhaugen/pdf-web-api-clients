<!-- use Mou to export .../doc/html/image/parameters.pdf from this document -->

## Image request parameters
<br>
Parameter names are case-insensitive.
All boolean parameters default to __false__.

### colorModel: string
The colorModel setting sets the target output colorspace for drawing PDF pages.

* __rgb__ (default): draw 24-bit RGB images, using 8 bits/channel
* __gray__: draw 8-bit grayscale images
* __rgba__: draw 32-bit RGBA images, using 8 bits/channel
* __cmyk__: draw 32-bit CMYK images, using 8 bits/channel

Gray and RGB format are valid for all output formats. RGBA format is valid only for TIFF and PNG output formats. CMYK format is only valid for TIFF output format. When drawing to CMYK format, note that CMYK channels with color values of 0 are drawn in knockout mode, not as transparent pixels.

### compression: string
The compression setting controls the compression algorithm used by a TIFF file written by the PDF Web API.

* __lzw__ (default): create a file compressed via the LZW algorithm. Such files are compressed with a lossless algorithm, resulting in files larger than those compressed with JPEG but without any loss of image quality.
* __jpg__: create a file compressed via the DCT (JPEG) algorithm. This file is compressed in a lossy manner, trading image quality for a significant reduction in file size.

### disableColorManagement: boolean
Changing this setting is recommended only in rare cases where your workflow manages colors in a downstream process or engine and is using PDF files that are intentionally expressed in device colors.

* __false__ (default): Color management is enabled for required color conversions of PDF elements to intermediate and blending color spaces, and from intermediate color spaces to the target output color space; color conversion is done via the Adobe Color Engine (ACE).
* __true__: No color management is performed. Simple transforms are used between color models, with colors in the same family used verbatim regardless of actual calibration.

### disableThinLineEnhancement: boolean
Changing this setting is recommended only when creating high-resolution output files where line enhancement is not desired.

* __false__ (default): Thin line enhancement is performed with the goal of ensuring that very thin lines maintain their visibility in created output files. This can lead to some lines becoming slightly thicker than they are in the PDF file, in order to stay visible.
* __true__: No thin line enhancement is performed.

### OPP: boolean
When ink is placed by a printer, typically inks are layered over each other - rather than knocking out the color underneath, some blending of the color underneath takes place as inks are printed on top of each other (overprinted). Overprint Preview (OPP) may be used to simulate the effect of overprinting inks on devices that support overprinting. This can cause some conversion of black to gray in CMYK format output files.

* __false__ (default): No color blend conversion is performed.
* __true__: PDF elements are converted through an intermediate CMYK blending space, before being written to the target output colorspace.

Usually this will be used when generating previews or proofs of PDF files that will ultimately be printed on CMYK-format output devices where ink overprinting is supported.

### pages: string
The pages parameter specifies the set of pages to print. It is a list of comma-separated pages or page ranges to place in the output file, with the first page being page 1 and pages drawn in ascending order.

* [number]: a single page number to print
* [number]-[number]: a page range to print, inclusively
* __last__: special keyword to designate the last page of a PDF file

Default: all pages for TIFF, first page for other formats.

Example: for a 16 page PDF file _2-4,7,9,14-last_ will draw pages 2, 3, 4, 7, 9, 14, 15 and 16.
<br>
<br>
<br>
<br>
<br>
<br>

### password: string
The password parameter specifies a password to be used to open PDF files that have been protected by a password. If required by a PDF file for processing, the password supplied must be one that allows for document permission for export and for content copying.

Note that this API does not support opening certificate-protected PDF files; PDF files protected with the ADEPT DRM scheme (such as those protected by Adobe Content Server); nor PDF files protected by LiveCycle Policy Server.

Valid values: any string value (no default)

### pdfRegion: string
The pdfRegion parameter specifies the region of PDF pages to draw. See section 14.11.2 of ISO 32000-1:2008 for a discussion on these regions and their relation to PDF pages.

* __crop__ (default)
* __art__
* __bleed__
* __bounding__
* __media__
* __trim__

### printPreview: boolean
* __false__ (default): Annotations that have normal appearance streams defined are drawn if they are marked as for display.
* __true__: Annotations that have default appearance streams defined are drawn if they are marked as for printing.

This parameter has no effect if suppressAnnotations is __true__.

### resolution: integer
The resolution parameter specifies the horizontal and vertical resoultions used in drawing PDF pages to output pages, in pixels per inch. This information is written to the output image (except for GIF files, where this is not supported by the format) in order to preserve the physical dimensions of the image in the output. Note that this API draws square pixels, and has no support for non-square pixel rendering.

Valid values: 12 to 2400, inclusive (default=300)
<br>
<br>

### smoothing: string
The smoothing parameter specifies the types of elements that are antialiased when drawn.

* __all__ (default): antialias and smooth text, line elements and smooth images.
* __none__: do not smooth any elements. This is typically only desired when rendering to a high resolution.
* __text__: antialias and smooth text elements only. This can be useful when drawing PDF files with large amounts of line art, where sharp edges are required to be preserved.

### suppressAnnotations: boolean
* __false__ (default): Annotations that have normal appearance streams defined and that are defined as for display will be drawn to the output file.
* __true__: Annotation drawing is suppressed and only actual PDF page contents are drawn.

