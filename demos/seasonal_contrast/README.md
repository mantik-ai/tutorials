## Integrating the Seasonal Contrast project into the AI-platform.

This project is focused on atmospheric transformation used to generate views for contrastive self-supervised learning on multi-spectralimages. Here, the experiments are benchmarked on the SeCo algorithm. By using atmospheric transformation as an alternative to color jittering, all the experiments conducted by authors of SeCo can be extended to multiple channels instead of RGB. The pre-trained models trained using atmospheric transformation shows higher accuracy over the two downstream tasks i.e. EuroSAT and Bigearthnet when compared with one trained with color jittering and grayscaling. The experiments run on both Juwels Booster and Juwels Cluster. Through the AI-platform it is possible to manage the pretraining and the training workflows and also to track the experiments and their results.<br/>

Related papers: Atmospheric Correction for Contrastive Self-supervised Learning of Multi-spectral Images (planned to be submit this year: 2022)<br/>
Original author of the code: Ankit Patnala<br/>
Gitlab link of the repository: https://gitlab.jsc.fz-juelich.de/patnala1/seasonal-contrast/-/tree/main
