# Manim Animations
Scientifc animations done using manim (https://www.manim.community/)

to launch run:
* `manim -pqh 1D_Beam_Manim.py `
* * `h` stands for high export quality

## Example

<video width="640" height="480" controls>
  <source src="https://marion-alexandre.freeboxos.fr/owncloud/index.php/s/w8PkrXwRA9xDLLE/download" type="video/mp4">
</video>



## Folder structure:
``````
.
├── Figures
│   └── Code_Bg_Bleu_dark.png
│
├── 1D_Beam_Manim.py
│
├── README.md
│
├── .gitignore
│
└── media
    ├── Tex
    └── videos

``````
## Usefull tips

Groups of object can be grouped using `VGroup(object1, object2)` and played with as a python list. Operations done on the VGroup is done on all its component
    the method `.copy()` is very pratical also to add a new object as if it comes from the first one without deleting the first one:

`
        Obect_1 = Circle(radius=0.5,color=BLUE_C)
        Object_2 = Object_1.copy().shift(UP)
        self.play(ReplacementTransform(Obect_1.copy(),Object_2)) `

## Usefull doc
* https://docs.manim.community/en/stable/reference/manim.utils.color.manim_colors.html
* https://azarzadavila-manim.readthedocs.io/en/latest/animation.html
* https://www.manim.community/    
