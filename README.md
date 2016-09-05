# video-based cardiac gating (vbcg) [![Build Status](https://travis-ci.org/nspi/vbcg.svg?branch=master)](https://travis-ci.org/nspi/vbcg)

This is a prototype demonstrating our research activities concerning *video-based vital sign monitoring*. 

We aim to apply this techniques in the context of ultra-high-field MRI but other scenarios are possible (e.g. gaming, sports)

## About

#### Software description
The aim of our research is to overcome the limitations of contact-based hardware for MRI patient monitoring (e.g. pulse oximetry) as they are error-prone, especially during ultra-high-field MRI. Instead, we develop video-based (and therefore contact-free) real-time methods based on recent findings in remote vital sign measurement. A valuable overview of this topic (unrelated to MRI) can be found in [1] and a summary of our current state of research (early 2016) can be found in [2]. This prototype will be used to demonstrate some of the algorithms we have developed so far.

Regarding video-based heart rate frequency estimation, there are other valuable open-source projects (e.g. [webcam-pulse-detector](https://github.com/thearn/webcam-pulse-detector)) or commercial products (e.g. [Philips Vital Signs Camera](http://www.ip.philips.com/licensing/program/115)). This aspect is part of our past work [4]; however we are more interested in developing methods for estimating the current phase of the cardiac cycle accurately.

> This software can NOT be used for diagnosis. Results are estimated and for entertainment purposes only!

#### License
GNU GPL v3.0

#### Features
- Read video stream from OpenCV compatible camera *or* read video stream from hard disk

- Crop video to manually-defined ROI *or* use Viola-Jones algorithm for face detection [3]

- Store frames from camera on hard disk

- Heart rate estimation as described in [4] 

- ''Prediction'' of next cardiac cycle as described in [5]

## Screenshots
| Screenshot (click to enlarge) | Screenshot (click to enlarge) | Video (click to play) |
| ------------- |-------------| -----|
| <a href="http://www.fh-dortmund.de/spicher/screenshot_1.png"> <img src="http://www.fh-dortmund.de/spicher/screenshot_1.png" width="256"></a>     | <a href="http://www.fh-dortmund.de/spicher/screenshot_2.png"> <img src="http://www.fh-dortmund.de/spicher/screenshot_2.png" width="256"></a> | <a href="https://fh-dortmund.sciebo.de/index.php/s/kc4xA39mpfN2c8f"> <img src="http://www.fh-dortmund.de/spicher/screenshot_3.png" width="256"></a> |

**Important notice:** For most accurate results, place your finger tip directly on the camera sensor (see screenshot 1). The higher the distance to the camera sensor, the lower the signal-to-noise ratio. If you want to obtain accurate results from remote skin, good illumination conditions and minimal subject motion is crucial. Additionally, there may be artefacts by other biosignals such as respiration (see screenshot 2, there are four well-pronounced breathing cycles). Comparing the results of heart rate estimation to a pulse oximeter from clinical practice (see screenshot 3), underlines the accuracy of the algorithm under adequate conditions.

## Installation and usage

#### Required software
- Python 2.7
  - numpy >= 1.8.2
  - matplotlib >= 1.3.1
  - scipy >= 0.13.3
  - several other modules
- TK toolkit python bindings (tkInter >= 2.7.5)
- OpenCV 2.4 python bindings

#### Installation

Run `make` (which is at the moment basically `pip install -r requirements.txt`  and installs required packages via pip).
OpenCV/TK bindings have to be installed manually (e.g. by `sudo apt-get install python-opencv python-tk`).

#### Usage

`cd src;` `python main.py`

#### Compatibility
The current master branch has been tested on Ubuntu 14.04 and Microsoft Windows 7.

## Available data
| Information   								  | FPS | Duration | Resolution | Download 	    |
|---------------------------------------------------------------------------------|:---:|:--------:|:-------:|:-------:|
| The finger of a volunteer was placed directly on the camera of an off-the-shelf smartphone (see screenshot 1). | 25 | 2:00 | 640x360 |  [here](https://fh-dortmund.sciebo.de/index.php/s/HtU70L5jz73wOJd/download)    |
| The forehead of a volunteer undergoing MRI examination was recorded with a MRI-compatible camera (see screenshot 2).| 25 | 2:00 | 720x480 | [here](https://fh-dortmund.sciebo.de/index.php/s/nuQtY1f8x31FYqc/download)    |
| A volunteer was recorded during office work using the webcam of an off-the-shelf business laptop. A pulse oximeter was applied as reference (see screenshot 3). | 30 | 1:00 | 640x480 | [here](https://fh-dortmund.sciebo.de/index.php/s/Q3pmdOvhDInk5oi/download)    |

## Credits
heart.png and heartbeat.png: Icons made by <a href="http://www.flaticon.com/authors/madebyoliver" title="Madebyoliver">Madebyoliver</a> from <a href="http://www.flaticon.com" title="Flaticon">www.flaticon.com</a> are licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>

## Contact
Nicolai Spicher ([http://fh-dortmund.de/spicher](http://fh-dortmund.de/spicher))

See website for email address and please use my [PGP key](http://www.fh-dortmund.de/spicher/pgp_pub.asc).

Department of Computer Science, University of Applied Sciences and Arts Dortmund

## References
[1] Sun Y. and Thakor N. *Photoplethysmography Revisited: From Contact
to Noncontact, From Point to Imaging* IEEE Transactions on Biomedical
Engineering, Vol. 63 (3), 2016 [(PDF)](https://www.researchgate.net/profile/Yu_Sun27/publication/282047098_Photoplethysmography_Revisited_From_Contact_to_Noncontact_From_Point_to_Imaging/links/5603f85608aefaf89ef9d0dc.pdf)

[2] Spicher N. *Cardiac activity measurement from video signals of the
human skin in ultra-high-field magnetic resonance imaging* Proceedings
of the 46nd Annual Meeting of the German Informatics Society,
Klagenfurt, Austria, 26.-30.09.2016. [(URL)](http://www.informatik2016.de/1227.html)

[3] Viola P., Jones M. *Rapid object detection using a boosted cascade
of simple features* Proceedings of the 2001 IEEE Computer Society 
Conference on on Computer Vision and Pattern Recognition, Kauai, USA, 
08.-14.12.2001 [(PDF)](https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf)

[4] Spicher N, Maderwald S, Ladd ME and Kukuk M. *Heart rate monitoring
in ultra-high-field MRI using frequency information obtained from video
signals of the human skin compared to electrocardiography and pulse
oximetry* Proceedings of the 49th Annual Conference of the German
Society for Biomedical Engineering, Luebeck, Germany, 16.-18.09.2015. [(PDF)](http://www.degruyter.com/view/j/cdbme.2015.1.issue-1/cdbme-2015-0018/cdbme-2015-0018.pdf)

[5] Spicher N, Maderwald S, Ladd ME and Kukuk M. *High-speed, contact-
free measurement of the photoplethysmography waveform for MRI triggering*
Proceedings of the 24th Annual Meeting of the ISMRM, Singapore, Singapore,
07.05.-13.05.2016. [(PDF)](http://www.fh-dortmund.de/spicher/1861.pdf)

[6] Spicher N, Kukuk M, Ladd ME and Maderwald S. *In vivo 7T MR imaging
triggered by phase information obtained from video signals of the human
skin* Proceedings of the 23nd Annual Meeting of the ISMRM, Toronto,
Canada, 30.05.-05.06.2015. [(PDF)](http://www.fh-dortmund.de/spicher/2548.pdf)
