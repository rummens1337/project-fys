<?php

include_once 'dbconn.inc.php';
error_reporting(E_ALL);
ini_set('display_errors', true);
/* Data die in het contactformulier is ingevuld, wordt opgelagen in deze variabelen.
  de mysql_real... statement zorgt ervoor dat er geen malafide opdrachten kunnen
  worden uitgevoerd in de database door deze in het formulier in te vullen. (SQL injection) */
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
    //brengt de gebruiker terug naar index.php
    header("Location: ../index.php");
