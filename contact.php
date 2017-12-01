<?php
include_once 'includes/dbconn.inc.php';

//ini_set('display_errors', true);
/* Data die in het contactformulier is ingevuld, wordt opgelagen in deze variabelen.
  de mysql_real... statement zorgt ervoor dat er geen malafide opdrachten kunnen
  worden uitgevoerd in de database door deze in het formulier in te vullen. (SQL injection) */
if (isset($_POST['submit'])) {
    $voornaam = mysqli_real_escape_string($conn, $_POST['voornaam']);
    $achternaam = mysqli_real_escape_string($conn, $_POST['achternaam']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $text = mysqli_real_escape_string($conn, $_POST['text']);
//declaratie van variabele die als template dient voor invoeren van contactformulier
//informatie
    $sql = "INSERT INTO formulieren (voornaam, achternaam, email, text)
            VALUES(?,?,?,?);";


    /* Door prepared statements te gebruiken wordt er een ander protocol gebruikt in
     * de database, waardoor de place holders eerst worden uitgevoerd als code, en de 
     * data later gestuurd wordt,en deze niet meer gelezen wordt als code. 
     * zo voorkom je wederom  "SQL injection" */

//declareert $conn als prepared statement
    $stmt = mysqli_stmt_init($conn);

//Voert de sql query uit als prepared statement, met vraagtekens als placeholder.
//als dit niet lukt, print hij een error.
    if (!mysqli_stmt_prepare($stmt, $sql)) {
        echo "SQL error";
    } else {
        //bind parameters (data) aan het statement zodat deze kan worden uitgevoerd.
        mysqli_stmt_bind_param($stmt, "ssss", $voornaam, $achternaam, $email, $text);

        //voert het prepared statement uit
        mysqli_stmt_execute($stmt);
    }
}
?>


<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="contact.css">
        <title>Fotokiosk</title>
    </head>
    <body>

        <img src="images/corendonTransparant.png" alt="Logo Corendon" style="width:262px;height:48px;">
        <br></br><br></br>
        <nav>
            <ul>
                <li><a href="index.php">Homepage</a></li>
                <li><a href="gallerij.php">Gallerij</a></li>
                <li><a class="active" href="contact.php">Contact</a></li>
                <li style="float:right"><a href="contact.php"><img src="images/Netherlands-Flag.png" alt="NL_vlag" class="t-image" style="width:30px;height:30px;border:0"></a></li>
                <li style="float:right"><a href="contact_en.php"><img src="images/United-Kingdom-flag-icon.png" alt="UK_vlag" class="t-image" style="width:30px;height:30px;border:0"></a></li>

            </ul>
        </nav>
        <br>
        <fieldset>
            <legend>Contactformulier</legend>
            <?php
//Wanneer het formulier nog niet verzonden is wordt deze weergegeven
            if (!isset($_POST['submit'])) {
                ?>
                <h3>Heeft u een vraag of opmerking?</h3>
                <form action="contact.php" method="POST">
                    Voornaam:<br>
                    <input type="text" name="voornaam" placeholder="Voornaam" required><br><br>
                    Achternaam:<br>
                    <input type="text" name="achternaam" placeholder="Achternaam" required><br><br>
                    E-mail:<br>
                    <input type="email" name="email" placeholder="E-mail" required /><br><br>
                    Uw vraag of opmerking:<br>
                    <textarea type="text" name="text" placeholder="Vul hier uw vraag of opmerking in" required style="height:200px;width:400px" ></textarea><br>
                    <input type="submit" name="submit" value="Verzenden">
                    <br>
                    <br><br><br><br>
                </form>
            <?php } else { ?>
                <!--Als het formulier is verzonden wordt onderstaande tekst getoont -->
                Wij hebben uw formulier in goede orde ontvangen <br> En komen zo snel mogelijk bij u terug
            <?php } ?>
        </fieldset>

        <div class="footer">
            <p><a href=http://www.corendon.nl/>www.corendon.nl</a> | Corendon Copyright© 2017 | <a href="tel:023-7510606">023-7510606</a></p>
        </div>



    </body>
</html>

<?php

// Import PHPMailer classes into the global namespace
// These must be at the top of your script, not inside a function
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if (isset($_POST['submit'])) {
//Load composer's autoloader
    require 'phpmailer/vendor/autoload.php';

    $mail = new PHPMailer(true);                              // Passing `true` enables exceptions
    try {
        //Server settings
        //$mail->SMTPDebug = 2;                                 // Enable verbose debug output
        $mail->isSMTP();                                      // Set mailer to use SMTP
        $mail->Host = 'smtp.live.com';  // Specify main and backup SMTP servers
        $mail->SMTPAuth = true;                               // Enable SMTP authentication
        $mail->Username = 'corendonfys@hotmail.com';                 // SMTP username
        $mail->Password = 'IT103@FYS';                           // SMTP password
        $mail->SMTPSecure = 'tls';                            // Enable TLS encryption, `ssl` also accepted
        $mail->Port = 25;                                    // TCP port to connect to
        //Recipients
        $mail->setFrom('corendonfys@hotmail.com', 'FYS');
        $mail->addAddress('corendonfys@hotmail.com', 'Corendon kieker');     // Add a recipient
        //$mail->addAddress('corendonfys@hotmail.com');               // Name is optional
        $mail->addReplyTo($email, $voornaam . "  " . $achternaam);
        //$mail->addCC('cc@example.com');
        //$mail->addBCC('bcc@example.com');
        //Attachments
        //$mail->addAttachment('/var/tmp/file.tar.gz');         // Add attachments
        //$mail->addAttachment('/tmp/image.jpg', 'new.jpg');    // Optional name
        //Content
        $mail->isHTML(true);                                  // Set email format to HTML
        $mail->Subject = 'Vraag of opmerking fotokieker';
        $mail->Body = nl2br( $_POST['text']);
        $mail->AltBody = $text;

        $mail->send();
    } catch (Exception $e) {
        echo 'Message could not be sent.';
        echo 'Mailer Error: ' . $mail->ErrorInfo;
    }
}