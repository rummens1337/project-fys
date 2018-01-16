<?php
//zet het weergeven van errors aan
ini_set('display_errors', false);

//maakt het mogelijk om "$conn" te gebruiken, dit is als het ware de verbinding
//tussen de database en de pi. hierin staat ook het wachtwoord beschreven.
include_once '/var/www/html/includes/dbconn.inc.php';

//Slaat de opgegeven code op in "$code" 
$code = mysqli_real_escape_string($conn, $_POST['usercode'] ?: $_GET['code']);

//als er een error is stopt het programma en geeft de error weer.
if ($conn->connect_error) {
    DIE("Connection failed: " . $conn->connect_error);
}

//template voor de sql query 
$sql = "SELECT path FROM imagedb WHERE uid=$code";

//voert de query uit in de database, en haalt dus het pad aan wat bij de opgegeven
//code hoort
$result = $conn->query($sql);
?>


<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="uwfoto.css">
        <title>Fotokiosk</title>
    </head>
    <body>

        <img src="images/corendonTransparant.png" alt="Logo Corendon" style="width:262px;height:48px;">
        <br></br><br></br>
        <nav>
            <ul>
                <li><a href="index.php">Homepage</a></li>
                <li><a href="gallerij.php">Gallerij</a></li>
                <li><a href="contact.php">Contact</a></li>
                <li style="float:right"><a href="uwfoto.php"><img src="images/Netherlands-Flag.png" alt="NL_vlag" class="t-image" style="width:30px;height:30px;border:0"></a></li>
                <li style="float:right"><a href="uwfoto_en.php"><img src="images/United-Kingdom-flag-icon.png" alt="UK_vlag" class="t-image" style="width:30px;height:30px;border:0"></a></li>

            </ul>
        </nav>
        <br>
        <br>
        <div id ="foto">
            <p> Alstublieft, uw foto.</p>
            <?php
            //kijkt of de opgegeven code voorkomt in de database, en of deze groter is dan 0.
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    $download = $row['path'];
                    echo "<img src='" . $row['path'] . "'>";
                }
            } else {
                //als er een foute code wordt ingevoerd dan:
                header("Location: index.php");
            }
            ?>
            <br>
            <!--Door de variabele download te gebruiken krijgt iedereen zijn persoonlijke foto -->
            <button><a href="<?php echo $download ?>" download="corendon.jpg">Download uw foto</a></button>  
        </div>
        <br><br><br><br>

        <div class="footer">
            <p><a href=http://www.corendon.nl/>www.corendon.nl</a> | Corendon Copyright© 2017 | <a href="tel:023-7510606">023-7510606</a></p>
        </div>



    </body>
</html>