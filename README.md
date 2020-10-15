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
It also fixes many problems, such as Save button not changing window title, Windows not saving some json files, and the most annoyingly, question title not updating the listbox.

# Comparision

Before            |  After
:----------------:|:-------------------------:
![Wrong 1](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/wrong1.png)  |  ![Correct 1](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/correct1.png)
The pre-NH version has a location misalignment on the preview screen. | Eventhrough the pin itself is little bit misaligned, the preview works as expected!
![Wrong 2](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/wrong2.png)  |  ![Correct 2](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/correct2.png)
When zooming in and out, location misalignment got even worse. | It's better, but not perfect. Atleast there is aurelia now!
![Rename Wrong](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/renamewrong.gif)  |  ![Rename Correct](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/renamecorrect.gif)
Do you think that saving and reloading the file after editing the question title is a chore? | Now, it's fixed. The item name syncs when the question title was changed.

# Features

### Easily Edit Smarty Pins Questions

![File Loaded](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/feat1.png)

Finally, with Smarty Pins Editor, you can easily create better Smarty Pins Quiz for everyone.

### Tons of Search Features

![SearchBar](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/feat2.png)

With many search features, you can easily find anything by questions, hints, and answer.

### The Debugging, is easy for everyone!

![HTMLOut](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/feat3.png)

With HTML output feature out of the box, You can easily export to html to check boundings for Smarty Pins  
So you never had to mess up with region to make question easier.

Here are some example output with HTML, produced with this editor.

![MapsOut](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/maps1.png)

![PinOpen](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/maps2.png)

![Style1](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/maps3.png)

![Style2](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/maps4.png)

![Style3](https://raw.githubusercontent.com/Crawlerop/everysmartypinsquestions/newheights/imgs/maps5.png)

# Wiki

Yes, we have a wiki. Please click [here](https://github.com/Crawlerop/everysmartypinsquestions/wiki).




