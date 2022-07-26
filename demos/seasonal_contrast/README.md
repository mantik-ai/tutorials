## Integrating the Seasonal Contrast project into the AI-platform.

This project is focused on atmospheric transformation used to generate views for contrastive self-supervised learning on multi-spectral images. The experiments are benchmarked on the SeCo algorithm. By using atmospheric transformation as an alternative to color jittering, all the experiments conducted by authors of SeCo can be extended to multiple channels instead of RGB. The pre-trained models trained using atmospheric transformation show higher accuracy over the two downstream tasks i.e. EuroSAT and Bigearthnet when compared with one trained with color jittering and greyscaling. The experiments run on both JUWELS Booster and JUWELS Cluster. Through the AI-platform it is possible to manage the pretraining and the training workflows and also to track the experiments and their results.<br/>

**Project author:** Ankit Patnala<br/>
**Related papers:** Atmospheric Correction for Contrastive Self-supervised Learning of Multi-spectral Images (planned to be submit this year: 2022)<br/>
**Gitlab link of the repository:** https://gitlab.jsc.fz-juelich.de/patnala1/seasonal-contrast/-/tree/main

The code of this project is also copied in the following repository which contains a collection of several KI:STE projects: https://gitlab.jsc.fz-juelich.de/kreshpa1/ai-platform-demos.git.<br/>
_Note_: The user needs a GitLab account in the GitLab instance of JSC in order to download all the necessary packages for creating the container and running the code.
