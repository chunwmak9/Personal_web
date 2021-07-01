

<html>
<body>

Welcome <?php echo $_POST["c"]; ?><br>
Your email address is: <?php echo $_POST["c"]; ?>

<?php
 $path = 'action_page.txt';
 if (isset($_POST['co'])) {
    $fh = fopen($path,"a+");
    $string = $_POST['co']."-".$_POST['co'];
    fwrite($fh,$string); // Write information to the file
    fclose($fh); // Close the file
 }
?>


</body>
</html>