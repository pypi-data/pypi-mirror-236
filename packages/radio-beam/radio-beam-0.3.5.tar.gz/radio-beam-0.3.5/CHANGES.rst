0.3.4 (2022-09-23)
------------------
 - Simplified two-beam common beam determination (https://github.com/radio-astro-tools/radio-beam/pull/102)
 - Allow non-arcsecond units in beam tables (https://github.com/radio-astro-tools/radio-beam/pull/98)
 - Support for beam initialization from area (https://github.com/radio-astro-tools/radio-beam/pull/94)
 - Drop support for python3.6

0.3.3 (2021-03-19)
------------------
 - Optimized the deconvolution operation to avoid extra unit conversions and creation of new `Beam` objects. (https://github.com/radio-astro-tools/radio-beam/pull/87)

 0.3.2 (2019-08-27)
 ------------------
 

0.3.1 (2019-02-20)
------------------
 - Set mult/div for convolution/deconvolution in `Beam` and `Beams`.
   The `==` and `!=` operators also work with `Beams` now.
   (https://github.com/radio-astro-tools/radio-beam/pull/75)
 - Added common beam operations to `Beams`.
   (https://github.com/radio-astro-tools/radio-beam/pull/67)
 - Fix PA usage for plotting and kernel routines.
   (https://github.com/radio-astro-tools/radio-beam/pull/65)

0.2 (2017-10-25)
----------------
 - Changed repo name to `radio-beam` from `radio_beam`.
   (https://github.com/radio-astro-tools/radio-beam/pull/59)
 - Enhancement: Added support for multiple beams through the `Beams` class.
   (https://github.com/radio-astro-tools/radio-beam/pull/51)


0.1 (2017-09-08)
----------------
First release
