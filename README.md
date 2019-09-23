# power_to_the_blind

## MakeMIT Hackathon Submission

### Problem Statement:

People with visual impairment may have trouble identifying people in their immediate vicinity. We built a Raspberry Pi-equipped hat that can feed people's names and relative locations into a user's earphones.

### Details:

We trained a Convolutional Neural Network  on a custom dataset of people's faces. The python-based immage classification model is then ported into a Raspberry Pi. We connected a mini camera to the Pi and ran the classification model. When a face is detected, the name of the person is read aloud out through the Pi's headpone jack, along with their relative position (left, middle, or right of image frame). The Pi setup is elegantly and discreetly attached to a baseball cap.
