# The Smarty Pins Editor: New Heights

An editor that is used to modify the questions in (now dead) [Smarty Pins](https://smartypins.withgoogle.com).
It supports outputing to CSV, and HTML.

We also has included 2 smarty pins dataset: The original version, and the punny version.  
The original version is a version that is ripped directly from Smarty Pins, while the punny version is very modified version of the original one.

The editor is mostly complete, but some features were not implemented or incomplete.

If you want all the pre-exported HTML question database, please click [here](https://crawlerop.github.io/everysmartypinsquestions/).

# Why New Heights?

Because the master repo is a release repo, while the New Heights was a developement repo.  
The New Heights version no longer uses StaticMaps module as MapBox has a StaticMap API, which fixes many pin alignment issues in this editor.

# Comparision

Before            |  After
:----------------:|:-------------------------:
![Wrong 1](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/wrong1.png)  |  ![Correct 1](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/correct1.png)
The pre-NH version has a location misalignment on the preview screen. | The preview works as expected!
![Wrong 2](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/wrong2.png)  |  ![Correct 2](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/correct2.png)
When zooming in and out, location misalignment got even worse. | It's better, but atleast there is aurelia now!
![Rename Wrong](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/renamewring.gif)  |  ![Rename Correct](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/renamecorrect.gif)
Do you think that saving and reloading the file after editing the question title is a chore? | Thank's, it saved a lot of time when editing the questions title.
