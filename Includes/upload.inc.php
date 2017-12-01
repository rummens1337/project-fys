<?php

include_once 'dbconn.inc.php';                  //maakt het mogelijk om variabelen uit dit bestand te gebruiken
//checkt of op verzenden is gedrukt, en voert mits dit zo is onderstaande code uit
if (isset($_POST['submit'])) {
    $file = $_FILES['file'];
    $fileName = $_FILES['file']['name'];        //de naam van de file
    $fileTmpName = $_FILES['file']['tmp_name']; //tijdelijke locatie van de file
    $fileSize = $_FILES['file']['size'];        //de grootte van de file
    $fileError = $_FILES['file']['error'];      //geeft aan of er een error is opgetreden
    $fileExt = explode('.', $fileName);         //haalt de filename uit elkaar na de . dus image.jpg wordt image en jpg
    $fileActualExt = strtolower(end($fileExt)); //zet de extensie in normale letters ( geen hoofdletters ) en wijst deze toe aan de variabele

    $id = range(111111, 999999);                //array met nummers 0 - 999999
    shuffle($id);                               //shuffelt de array
    $imageId = array_shift($id);                //wijst uniek id toe aan $imageid en verwijdert id uit array
    $allowed = array('jpg', 'jpeg', 'png', 'pdf'); //declaratie van array met extensies die zijn toegestaan

    if (in_array($fileActualExt, $allowed)) {   //checkt of de extensie van de file is toegestaan om te uploaden
        if ($fileError === 0) {                 //checkt of er een errror was
            if ($fileSize < 5000000) {           //checkt of de filesize is toegestaan
                $fileNameNew = $imageId . "." . $fileActualExt;             //verrandert de filenaam in bvb: 123456.jpg
                $fileDestination = '/var/www/html/uploads/' . $fileNameNew; ///var/www/html/uploads/123456.jpg
                $filenameDb = 'uploads/' . $fileNameNew;                     //het pad wat opgeslagen wordt in de database
                move_uploaded_file($fileTmpName, $fileDestination);         //verplaatst de tijdelijke foto naar nieuwe locatie   
                $sqlimage = ("INSERT INTO imagedb (uid, path) VALUES ('$imageId', '$filenameDb')");
                mysqli_query($conn, $sqlimage);                             //voert het pad naar de foto in de database in.
                //brengt de gebruiker terug naar index.php 
                echo $imageId;
                //header("Location: ../index.php?uploadsuccess");             
                //bericht als file te groot is    
            } else {
                echo "Your file is too big!";
            }
            //bericht als er een error was    
        } else {
            echo "There was an error uploading your file!";
        }
        //bericht als gebruiker verkeerde filetype wilde uploaden    
    } else {
        echo "You cannot upload files of this type!";
    }
}