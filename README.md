# video-based cardiac gating (vbcg) 

This is a freely available hardware and software prototype demonstrating our research activities concerning processing of video signals from human skin.
We apply this technique in the context of ultra-high-field MRI for heart rate measurement and image acquisition but other scenarios are possible (e.g. gaming, sports).

#### News 
- **Feb. 2017:**
I am pleased to announce that this project will be presented at the <a href="http://www.ismrm.org/2017-annual-meeting-exhibition/">ISMRM 25th Annual Meeting & Exhibition</a> as a Power Pitch presentation. Additionally, I present our recent investigation of local skin color phase variations. 
- **Dec 2016:**
Our initial study on video-based MRI triggering has been accepted recently for open-access publication in <a href="http://biomedical-engineering-online.biomedcentral.com/articles/10.1186/s12938-016-0245-3">Biomedical Engineering Online</a>.


## About

#### Software

The aim of our research is to overcome the limitations of contact-based hardware for MRI patient monitoring (e.g. electrocardiography, pulse oximetry) as they are error-prone, especially during long or ultra-high-field MRI examinations. Instead, we develop video-based (and therefore contact-free) real-time methods based on recent findings in remote vital sign measurement. A valuable overview of this field of research (unrelated to MRI) can be found in <a href=#1>[1]</a>. So far, journal papers within the context of MRI were published by a Stanford group <a href=#2>[2]</a> and our group <a href=#3>[3]</a>. 


The software presented here will be used to demonstrate some of the methods we have developed so far. Regarding video-based heart rate frequency estimation, there are other valuable open-source projects (e.g. [webcam-pulse-detector](https://github.com/thearn/webcam-pulse-detector)) or commercial products (e.g. [Philips Vital Signs Camera](http://www.ip.philips.com/licensing/program/115)). This aspect is part of our past work <a href=#5>[5]</a>; however we are more interested in developing methods for estimating the current phase of the cardiac cycle accurately. See the literature list if you are interested in the scientific background.

#### Hardware

Next to the software, you can find information on a low-cost device, based on an <a href="https://www.arduino.cc/en/Main/ArduinoBoardNano">Arduino Nano</a>, for sending triggers from the software to the MR scanner. This is needed, when applying algorithms for video-based cardiac gating. Additionally, you can find the schematics of an LED array for increasing illumination of the skin.

> Proposed software and hardware can NOT be used for diagnosis or treatment. Results are estimated and for entertainment purposes only!

#### License

GNU GPL v3.0

#### Build status

Develop branch [![Build Status](https://travis-ci.org/nspi/vbcg.svg?branch=develop)](https://travis-ci.org/nspi/vbcg) [![Coverage Status](https://coveralls.io/repos/github/nspi/vbcg/badge.svg?branch=develop)](https://coveralls.io/github/nspi/vbcg?branch=develop) [![Dependency Status](https://www.versioneye.com/user/projects/57db0c3c037c20002d0d963a/badge.svg)](https://www.versioneye.com/user/projects/57db0c3c037c20002d0d963a)

Master branch&nbsp;&nbsp; [![Build Status](https://travis-ci.org/nspi/vbcg.svg?branch=master)](https://travis-ci.org/nspi/vbcg) [![Coverage Status](https://coveralls.io/repos/github/nspi/vbcg/badge.svg?branch=master)](https://coveralls.io/github/nspi/vbcg?branch=master)  [![Dependency Status](https://www.versioneye.com/user/projects/57db0c44037c2000475cbfc7/badge.svg)](https://www.versioneye.com/user/projects/57db0c44037c2000475cbfc7)

Latest release&nbsp;&nbsp; [![Build Status](https://travis-ci.org/nspi/vbcg.svg?branch=v0.2-beta)](https://travis-ci.org/nspi/vbcg)  [![GitHub tag](https://img.shields.io/github/tag/nspi/vbcg.svg?maxAge=2592000)](https://github.com/nspi/vbcg/releases/tag/v0.2-beta) 

Use the *release* version if you want to use a manually tested and stable version. The *master* branch contains the most current version that **should** be stable and the *develop* branch contains the current bleeding-edge development version.

#### Features

- Read video stream from OpenCV compatible camera *or* read video stream from hard disk

- Crop video to manually-defined ROI *or* use Viola-Jones algorithm for face detection <a href=#4>[4]</a>

- Store frames from camera on hard disk

- A virtual serial device is used if the trigger device is not available
(Please note that the emulation decreases performance)

- Heart rate estimation as described in <a href=#5>[5]</a>
 
- Signal filtering as described in <a href=#6>[6]</a>

- MRI triggering by phase information as described in <a href=#7>[7]</a>

## Screenshots
| **HR estimation** | **MRI triggering** |
|:-------------:|:-------------:| 
| <a href="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_1.png"> <img src="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_1.png" width="200"></a>     | <a href="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_2.png"> <img src="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_2.png" width="200"></a> | 
| **Signal filtering** | **HR estimation** |
| <a href="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_3.png"> <img src="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_3.png" width="200"></a> | <a href="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_4.png"> <img src="http://www.fh-dortmund.de/spicher/screenshots/v0.2-beta/screenshot_4.png" width="200"></a> |

**Video Demonstration:** You can find a video of v0.1-beta here: <a href="https://fh-dortmund.sciebo.de/index.php/s/kc4xA39mpfN2c8f">here</a>

**Important notice:** For most accurate results, place your finger tip directly on the camera sensor (see screenshot 1). The higher the distance to the camera sensor, the lower the signal-to-noise ratio. If you want to obtain accurate results from remote skin, good illumination conditions and minimal subject motion is crucial. Additionally, there may be artefacts by other biosignals such as respiration. Comparing the results of heart rate estimation to a pulse oximeter from clinical practice (see screenshot 3), underlines the accuracy of the algorithm under adequate conditions. Additionally, we used the videos from the [Eulerian Video Magnification](http://people.csail.mit.edu/mrub/evm/) website for evaluation (see screenshot 4).


## Installation and usage

#### Required software

- Python 2.7
	- modules: scipy, numpy, matplotlib, pillow, pyserial, and several other modules
	- see <a href="https://github.com/nspi/vbcg/blob/master/requirements.txt">requirements.txt</a> for detailed information
- TK toolkit python bindings (tkInter >= 2.7.5)
- OpenCV 2.4 python bindings

#### Installation

Run `make` (which is at the moment basically `pip install -r requirements.txt`  and installs required packages via pip).
OpenCV/TK bindings have to be installed manually (e.g. by `sudo apt-get install python-opencv python-tk`).

#### Usage

`cd src;` `python main.py`

#### Compatibility

The current development branch is tested on Ubuntu 14.04 (and on Ubuntu 12.04 using [Travis-CI](https://travis-ci.org/nspi/vbcg)). The current master branch is additionally tested on Windows 7 but the performance on Windows is inferior.

## Available data
| Information   								  | FPS | Duration | Resolution | Download 	    |
|---------------------------------------------------------------------------------|:---:|:--------:|:-------:|:-------:|
| The finger of a volunteer was placed directly on the camera of an off-the-shelf smartphone (see screenshot 1). | 25 | 2:00 | 640x360 |  [here](https://fh-dortmund.sciebo.de/index.php/s/HtU70L5jz73wOJd/download)    |
| The forehead of a volunteer undergoing MRI examination was recorded with a MRI-compatible camera (see screenshot 2).| 25 | 2:00 | 720x480 | [here](https://fh-dortmund.sciebo.de/index.php/s/nuQtY1f8x31FYqc/download)    |
| A volunteer was recorded during office work using the webcam of an off-the-shelf business laptop. A pulse oximeter was applied as reference (see screenshot 3). | 30 | 1:00 | 640x480 | [here](https://fh-dortmund.sciebo.de/index.php/s/Q3pmdOvhDInk5oi/download)    |

More videos from persons in different situations can be found on the [Eulerian Video Magnification](http://people.csail.mit.edu/mrub/evm/) website. More videos from subjects inside the MR bore can be found in the [supplemental material](https://dx.doi.org/10.1002%2Fmrm.25781) of the paper by Maclaren et al. <a id="2">[2]</a> 

## Credits
heart.png and heartbeat.png: Icons made by <a href="http://www.flaticon.com/authors/madebyoliver" title="Madebyoliver">Madebyoliver</a> from <a href="http://www.flaticon.com" title="Flaticon">www.flaticon.com</a> are licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>

## Contact
Nicolai Spicher ([http://fh-dortmund.de/spicher](http://fh-dortmund.de/spicher))

See website for email address and please use my [PGP key](http://www.fh-dortmund.de/spicher/pgp_pub.asc).

Department of Computer Science, University of Applied Sciences and Arts Dortmund

## References
<a id="1">[1]</a> Sun Y. and Thakor N. *Photoplethysmography Revisited: From Contact
to Noncontact, From Point to Imaging* IEEE Transactions on Biomedical
Engineering, Vol. 63 (3), 2016 [(PDF)](https://www.researchgate.net/profile/Yu_Sun27/publication/282047098_Photoplethysmography_Revisited_From_Contact_to_Noncontact_From_Point_to_Imaging/links/5603f85608aefaf89ef9d0dc.pdf)

<a id="2">[2]</a>  Maclaren J., Aksoy M. and Bammer R. *Contact-free physiological 
monitoring using a markerless optical system.* Magnetic resonance in medicine. 74(2):571-7 2015. [(PDF)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4515196/pdf/nihms687662.pdf)

<a id="3">[3]</a>  Spicher N., Kukuk M., Maderwald S., Ladd ME. *Initial evaluation of prospective cardiac triggering using photoplethysmography signals recorded with a video camera compared to pulse oximetry and electrocardiography at 7T MRI* Biomedical Engineering Online. 15(1):126, 2016. [(PDF)](http://biomedical-engineering-online.biomedcentral.com/track/pdf/10.1186/s12938-016-0245-3?site=biomedical-engineering-online.biomedcentral.com)

<a id="4">[4]</a>  Viola P., Jones M. *Rapid object detection using a boosted cascade
of simple features* Proceedings of the 2001 IEEE Computer Society 
Conference on on Computer Vision and Pattern Recognition, Kauai, USA, 
08.-14.12.2001. [(PDF)](https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf)

<a id="5">[5]</a>  Spicher N., Maderwald S., Ladd ME. and Kukuk M. *Heart rate monitoring
in ultra-high-field MRI using frequency information obtained from video
signals of the human skin compared to electrocardiography and pulse
oximetry* Proceedings of the 49th Annual Conference of the German
Society for Biomedical Engineering, Luebeck, Germany, 16.-18.09.2015. [(PDF)](http://www.degruyter.com/view/j/cdbme.2015.1.issue-1/cdbme-2015-0018/cdbme-2015-0018.pdf)

<a id="6">[6]</a>  Spicher N., Maderwald S., Ladd ME. and Kukuk M. *High-speed, contact-
free measurement of the photoplethysmography waveform for MRI triggering*
Proceedings of the 24th Annual Meeting of the ISMRM, Singapore, Singapore,
07.05.-13.05.2016. [(PDF)](http://www.fh-dortmund.de/spicher/1861.pdf)

<a id="7">[7]</a>  Spicher N., Kukuk M., Ladd ME. and Maderwald S. *In vivo 7T MR imaging
triggered by phase information obtained from video signals of the human
skin* Proceedings of the 23nd Annual Meeting of the ISMRM, Toronto,
Canada, 30.05.-05.06.2015. [(PDF)](http://www.fh-dortmund.de/spicher/2548.pdf)


