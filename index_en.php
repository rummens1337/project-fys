<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="Homepage_styles.css">

        <title>Photo booth</title>

    </head>
    <body>

        <img src="images/corendonTransparant.png" alt="Logo Corendon" style="width:262px;height:48px;">
        <br></br><br></br>
        <nav>
            <ul>
                <li><a class="active" href="index_en.php">Homepage</a></li>
                <li><a href="gallerij_en.php">Gallery</a></li>
                <li><a href="contact_en.php">Contact</a></li>
                <li style="float:right"><a href="index.php"><img src="images/Netherlands-Flag.png" alt="NL_vlag" class="t-image" style="width:30px;height:30px;border:0"></a></li>
                <li style="float:right"><a href="index_en.php"><img src="images/United-Kingdom-flag-icon.png" alt="UK_vlag" class="t-image" style="width:30px;height:30px;border:0"></a></li>

            </ul>
        </nav>
        <br>
        <form action="includes/upload.inc.php" method ="POST" enctype= "multipart/form-data">
            <input type ="file" name="file">
            <button type="submit" name="submit">upload</button>
            <div id="divhome">
        </form>         
        <br><p>Enter your unique code here.</p>
        <form action="uwfoto_en.php" method="POST">

            <input type ="text" name="usercode" placeholder="Enter code">
            <button type="submit" name="code">Request photo</button>

        </form>

        <div class="slideshow-container">
            <div class="mySlides fade">
                <div class="numbertext">1 / 3</div>
                <img src="images/gallerij1.jpg" style="width:100%">
                <div class="text">This photo was shot in Dusseldorf</div>
            </div>

            <div class="mySlides fade">
                <div class="numbertext">2 / 3</div>
                <img src="images/gallerij2.jpg" style="width:100%">
                <div class="text">This phot was shot in Parris</div>
            </div>

            <div class="mySlides fade">
                <div class="numbertext">3 / 3</div>
                <img src="images/gallerij3.jpg" style="width:100%">
                <div class="text">This photo was shot in Madrid</div>
            </div>
        </div>
        <br>

        <div style="text-align:center">
            <span class="dot" onclick="currentSlide(1)"></span> 
            <span class="dot" onclick="currentSlide(2)"></span> 
            <span class="dot" onclick="currentSlide(3)"></span> 
        </div>

        <br><br><br><br>
        <script>
            var slideIndex = 0;
            showSlides();

            function showSlides() {
                var i;
                var slides = document.getElementsByClassName("mySlides");
                for (i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";
                }
                slideIndex++;
                if (slideIndex > slides.length) {
                    slideIndex = 1;
                }
                slides[slideIndex - 1].style.display = "block";
                setTimeout(showSlides, 5000); // Change image every 2 seconds
            }
        </script>
        <div class="footer">
            <p><a href=http://www.corendon.nl/>www.corendon.nl</a> | Corendon Copyright© 2017 | <a href="tel:023-7510606">023-7510606</a></p>
        </div>



    </body>
</html>