<?php
$dbhost = "127.0.0.1";
$dbuser = "root";
$dbpass = "password";
$dbname = "cs157a";
$connection = mysqli_connect($dbhost, $dbuser, $dbpass, $dbname);

if(mysqli_connect_errno()){
    die("Database connection failed " .
        mysqli_connect_error() .
        "(".mysqli_connect_errno().")"
    );
}
$sql = "SELECT id, name, age FROM EMP";
$result = $connection->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - Name: " . $row["name"]. " " . $row["age"]. "<br>";
    }
} else {
    echo "0 results";
}

?>

    <!doctype html>

    <html>
    <head>
        <title>Conn</title>

    </head>

    <body>


    </body>

    </html>
<?php
mysqli_close($connection);

?>
