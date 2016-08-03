#video-based cardiac gating (vbcg)

This is a prototype demonstrating our
research activities concerning video-based vital sign monitoring in
ultra-high-field MRI.

##About
The aim of our research is to overcome the limitations of contact-based
hardware for MRI patient monitoring (e.g. pulse oximetry)
as they are error-prone, especially during ultra-high-field
MRI. Instead, we develop video-based (and therefore contact-free) 
real-time methods based on recent findings in remote vital sign measurement. 
A valuable overview of this topic (unrelated to MRI) can be found in
[0] and a summary of our current state of research (early 2016) can be found in [1].

#### Features
This prototypes demonstrates several algorithms that can be used for
processing videos obtained from the human skin inside the MRI bore for
HR monitoring or MRI triggering.

- Heart rate estimation as described in [3]
- MRI triggering as described in [2] and [4]

#### License
GNU GPL v3.0

#### Screenshot
...


##Installation and usage

#### Required software
- Python 2.7
  - numpy >= 1.8.2
  - matplotlib >= 1.3.1
  - scipy >= 0.13.3
  - several smaller modules
- TK toolkit python bindings (tkInter >= 2.7.5)
- OpenCV 2.4 python bindings

#### Installation
run `make`
(which is at the moment basically `pip install -r requirements.txt`  and installs required packages via pip).

OpenCV/TK bindings have to be installed manually (e.g. by `sudo apt-get install python-opencv python-tk`).

#### Usage
run `vbcg` without parameters

##Contact
Nicolai Spicher ([http://fh-dortmund.de/spicher](http://fh-dortmund.de/spicher))

See website for email address and please use PGP.

Department of Computer Science, University of Applied Sciences and Arts Dortmund

## References
[0] Sun Y. and Thakor N. *Photoplethysmography Revisited: From Contact
to Noncontact, From Point to Imaging* IEEE Transactions on Biomedical
Engineering, Vol. 63 (3), 2016

[1] Spicher N. *Cardiac activity measurement from video signals of the
human skin in ultra-high-field magnetic resonance imaging* Proceedings
of the 46nd Annual Meeting of the German Informatics Society,
Klagenfurt, Austria, 26.-30.09.2016.

[2] Spicher N, Maderwald S, Ladd ME and Kukuk M. *High-speed, contact-
free measurement of the photoplethysmography waveform for MRI triggering*
Proceedings of the 24th Annual Meeting of the ISMRM, Singapore, Singapore,
07.05.-13.05.2016.

[3] Spicher N, Maderwald S, Ladd ME and Kukuk M. *Heart rate monitoring
in ultra-high-field MRI using frequency information obtained from video
signals of the human skin compared to electrocardiography and pulse
oximetry* Proceedings of the 49th Annual Conference of the German
Society for Biomedical Engineering, Luebeck, Germany, 16.-18.09.2015.

[4] Spicher N, Kukuk M, Ladd ME and Maderwald S. *In vivo 7T MR imaging
triggered by phase information obtained from video signals of the human
skin* Proceedings of the 23nd Annual Meeting of the ISMRM, Toronto,
Canada, 30.05.-05.06.2015.
